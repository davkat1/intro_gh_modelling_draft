# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.18.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Implementing the crop model in GreenLight

# %% [markdown]
# ## Reminder: what is GreenLight?

# %% [markdown]
# [GreenLight](https://github.com/davkat1/greenlight) has been originally developed as [an open-source model for greenhouses with a tomato crop](https://doi.org/10.1016/j.biosystemseng.2020.03.010). Since then, it has been expanded to be used as a modelling platform where [various model components can be combined](https://greenlight.readthedocs.io/en/latest/user/modifying_and_combining_models.html). GreenLight is therefore no longer a singular model, but allows to define and run models in a structured way, which will be used in this chapter.
#
# This course is based on **GreenLight v2.0.7**.

# %% [markdown]
# ### Defining models in GreenLight

# %% [markdown]
# Models are defined in GreenLight using a [Python dictionary](https://docs.python.org/3/tutorial/datastructures.html#dictionaries) (`dict`) that defines the model variables. Each variable is itself defined using a dictionary, so the model definition is in fact a dictionary of dictionaries. The *keys* of the model definition dictionary are the names of the variables. For each variable, the corresponding *value* is another dictionary, with the following *keys*:
# - `description` - a description of the variable
# - `unit` - the unit that the variable's values are in
# - `reference` - a reference describing where the variable definition came from
# - `definition` - a definition of the variable. This may be a single value, input data, or a calculation based on other variables
# - `type` - the type of variable, which allows GreenLight to know how to process the variable

# %% [markdown]
# ### Variable types in GreenLight

# %% [markdown]
# Variables in GreenLight have 5 possible types:
# - `const` - indicates that the variable stays constant throughout a model run
# - `input` - indicates that the values for the variable are provided as an input
# - `aux` - an auxiliary variable: a variable that is calculated based on other variables
# - `state` - a value that is defined by an ordinary differential equation
# - `function` - a function that works as a shorthand for repeated calculations
#
# In this course, we will focus only on the first 4 `type`s of variables: `const`, `input`, `aux`, and `state`.

# %% [markdown]
# ## Reminder: using live code in this page

# %% [markdown]
# In this page we will be using **live code** for the first time in this course. To start, click the rocket button (🚀) at the top of this page, above the title. Then choose "▶ Live Code". The loading may take some time so it is good to start the Live Code before reading on, so it is ready when you need it.
#
# If the Live Code fails to load for whatever reason, you can try clicking the rocket button (🚀) and choosing **Binder** instead.
#
# The material in this page contains **editable Python code blocks**. Once the Live Code engine is ready (you should see a text under the page's title, stating something like "Launching from mybinder.org: **ready**), all code blocks become editable. Simply click anywhere on the text in the code block, edit in, and then click *run*. As a first try, you may try the code below.

# %%
"""
Editable code block for testing
"""

out_text = "Hi! I'm <...enter whatever you would like here...>!"

print(out_text)

# %% [markdown]
# ## Implementing the model in GreenLight

# %% [markdown]
# We will first [import](https://docs.python.org/3/reference/import.html) some modules that will be used during this section. Run the code block below.

# %%
""" 
Imports needed for running the code in this section
"""

import os

from IPython.display import display
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from urllib.request import urlretrieve

# The GreenLight package for defining and running dynamic models
import greenlight

# %% [markdown]
# Next, we will define a crop model as we did in the previous section. In the code block below, we define a dictionary similar to [Soultion 3 in the previous section](

# %%
crop_definition = {
    "W": {
        "description": "Crop dry mass",
        "unit": "g/m2",
        "definition": "LUE * (1 - exp(-k*LAI)) * I * 1e-6",
        "type": "state",
        "init": "75",
        "reference": "Stanghellini (2019), Eq. 2.25. " \
                    "Note that in Eq. 2.5 (Stanghellini 2019), dW/dt is given in g/m2/day. " \
                    "However, solar light is expressed there as I, in MJ/m2/day. " \
                    "Here we use I instead in W/m2 = J/m2/s (see reference for I). " \
                    "This is multiplied by 1e-6, to convert to MW/m2 = MJ/m2/s. " \
                    "Thus we use I*1e-6 which is in MJ/m2/s, instead of MJ/m2/day. " \
                    "Therefore the unit for dW/dt becomes g/m2/s instead of g/m2/day. " \
                    "The default time unit in GreenLight is s, so W is automatically in g/m2." \
                    "The initial value of 75 g/m2 is based on Fig. 2.13 (Stanghellini 2019)" \
                    "As a reasonable value for a small crop"
    },
     "LUE": {
         "description": "Light use efficiency",
         "unit": "g crop weight per MJ PAR",
         "definition": "4.3",
         "type": "const",
         "reference": "Stanghellini (2019), pg. 49. 4.3 is chosen as a middle value, see Fig. 2.13"
    },
     "k": {
         "description": "Light extinction coefficient",
         "unit": "-",
         "definition": "0.7",
         "type": "const",
         "reference": "Stanghellini (2019), pg. 49. " \
                      "The value of 0.7 is based on Stanghellini (2019), pg. 39: " \
                      "'For many greenhouse crops, k has a value between 0.6 and 0.8'"
    },
     "I": {
         "description": "Light intensity",
         "unit": "W/m2",
         "definition": "0.5*iSun",
         "type": "input",
         "reference": "Stanghellini (2019), pg. 49. " \
                      "Since the default time unit in GreenLight is seconds, " \
                      "It is more convenient to use I in J/m2/s = W/m2 instead of MJ/m2/day. "\
                      "This is adjusted in the definition of W, see there"
    },
    "LAI": {
        "description": "Leaf area index",
        "unit": "m2 leaf per m2 floor",
        "definition": "W * fLeaves * SLA / 10000",
        "type": "aux",
        "reference": "Stanghellini (2019), Eq. 2.26. " \
                     "Note that according to the Eq., the LAI growth rate is equal to " \
                     "crop growth rate times fLeaves * SLA / 10000. " \
                     "Therefore LAI is equal to crop dry mass times the same factor" 
    },
     "fLeaves": {
         "description": "Fraction of crop dry mass partitioned to the leaves",
         "unit": "-",
         "definition": "0.8",
         "type": "const",
         "reference": "Stanghellini (2019), Eq. 2.26. " \
                      "The value of 0.8 is chosen to represent a young vegetative crop"
    },
     "SLA": {
         "description": "Specific leaf area",
         "unit": "cm2/g",
         "definition": "250",
         "type": "const",
         "reference": "Stanghellini (2019), Eq 2.26. " \
                      "The value of 250 is a middle value for tomato, "\
                      "See Stanghellini (2019), Table 2.1"
    }   
 }

n_days = 100

options = {
    "options": {
        "t_start":"0",
        "t_end": str(n_days * 24 * 60 * 60),
        "output_step": "300",
        "t_eval": "300"
    }
}

url = "https://raw.githubusercontent.com/davkat1/intro_gh_modelling_draft/refs/heads/main/notebooks/input/example_weather.csv"
urlretrieve(url,"example_weather.csv")

crop_mdl = greenlight.GreenLight(
    base_path=os.getcwd(), 
    input_prompt=[crop_definition, os.path.join("example_weather.csv"), options], 
    output_path=os.path.join("output", "crop_output.csv")
)
crop_mdl.run()



# %%
# Load simulation result
crop_output = pd.read_csv(os.path.join("output", "crop_output.csv"), header=[0,1,2], low_memory=False)

# Display
def display_output(output_df, chosen_vars, titles, ylabels, line_style):
    axes = []
    
    for vars_to_plot, title, ylabel in zip(chosen_vars, titles, ylabels):
        fig = plt.figure(figsize=(10, 6))
        ax = fig.add_subplot(111)
        
        for var in vars_to_plot:
            ax.plot(output_df["Time"], output_df[var], line_style, label=var)
        
        ax.set_xlabel("Time (s)")
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        ax.legend()
        ax.grid(True)
        axes.append(ax)
        plt.show()

    return axes
    
axes = display_output(crop_output, [["W"], ["iSun"]], ["", ""], ["", ""], '-o')

# %%
display(crop_output)

# %%
import numpy as np

fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111)
ax.plot(1 - np.exp(-0.7*crop_output["LAI"]))

# %%
# Group rows into blocks of 288
groups = np.arange(len(crop_output)) // 288

daily_iSun = crop_output['iSun'].groupby(groups).sum()
daily_W = crop_output['W'].groupby(groups).agg(
    lambda x: x.iloc[-1] - x.iloc[0]
)

# Plot both daily values
fig, ax1 = plt.subplots(figsize=(12, 5))

days = np.arange(1, len(daily_iSun) + 1)

ax1.plot(days, daily_iSun, color='blue')
ax1.set_xlabel('Day')
ax1.set_ylabel('Daily sum of iSun', color='blue')

ax2 = ax1.twinx()
ax2.plot(days, daily_W, color='orange')
ax2.set_ylabel('Daily difference of W', color='orange')

plt.title('Daily sum of iSun and daily difference of W')
fig.tight_layout()
plt.show()

# %%

import ipywidgets as widgets
import matplotlib.pyplot as plt
import pandas as pd

from IPython.display import display, clear_output

# --------------------------------------------------
# 1. Define the input sliders
# --------------------------------------------------

slider_1 = widgets.FloatSlider(
    value=75,
    min=0,
    max=250,
    step=0.1,
    description='Initial value for W:',
    continuous_update=False
)

slider_2 = widgets.FloatSlider(
    value=200,
    min=0,
    max=1000,
    step=1,
    description='Iw',
    continuous_update=False
)

slider_3 = widgets.IntSlider(
    value=4.3,
    min=0,
    max=20,
    step=0.01,
    description='LUE',
    continuous_update=False
)


# --------------------------------------------------
# 2. Define the buttons
# --------------------------------------------------

run_button = widgets.Button(
    description='Run model',
    button_style='success',
    icon='play'
)

delete_button = widgets.Button(
    description='Delete latest curve',
    button_style='danger',
    icon='trash'
)


# --------------------------------------------------
# 3. Set up the plot
# --------------------------------------------------

fig, ax = plt.subplots(figsize=(10, 5))

ax.set_xlabel('Time')
ax.set_ylabel('Model output')
ax.set_title('Model trajectories')
ax.grid(True, alpha=0.3)

# Store the curves and their labels
curves = []


# --------------------------------------------------
# 4. Function to run the model
# --------------------------------------------------
import copy

def run_model(button):

    # Read slider values
    p1 = slider_1.value
    p2 = slider_2.value
    p3 = slider_3.value

    crop_definition_new = copy.deepcopy(crop_definition)
    crop_definition_new["W"]["init"] = str(p1)
    crop_definition_new["Iw"]["definition"] = str(p2)
    crop_definition_new["LUE"]["definition"] = str(p3)
    
    # Create a new model
    model = greenlight.GreenLight(input_prompt=crop_definition_new)

    # Run the model
    model.run()

    # Read the output file
    data = pd.read_csv(model.output_file)

    # Extract time and output
    time = data['time']
    values = data['value']

    # Add a new curve
    line, = ax.plot(
        time,
        values,
        label=f'Run {len(curves)+1}: '
              f'p1={p1}, p2={p2}, p3={p3}'
    )

    curves.append(line)

    # Update legend and display
    ax.legend(loc='best')
    fig.canvas.draw_idle()


# --------------------------------------------------
# 5. Function to delete the latest curve
# --------------------------------------------------

def delete_latest(button):

    if curves:

        # Remove the most recent curve
        line = curves.pop()
        line.remove()

        # Update legend
        ax.legend(loc='best')

        fig.canvas.draw_idle()


# --------------------------------------------------
# 6. Connect buttons to functions
# --------------------------------------------------

run_button.on_click(run_model)
delete_button.on_click(delete_latest)


# --------------------------------------------------
# 7. Display the interface
# --------------------------------------------------

controls = widgets.VBox([
    widgets.HTML('<h3>Model parameters</h3>'),
    slider_1,
    slider_2,
    slider_3,
    widgets.HBox([
        run_button,
        delete_button
    ])
])

display(controls)
display(fig)

