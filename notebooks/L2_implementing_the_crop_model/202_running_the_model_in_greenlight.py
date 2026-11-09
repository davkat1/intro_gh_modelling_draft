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
# # 2.2 Running the model in GreenLight

# %% [markdown]
# ## Live code in this page

# %% [markdown] editable=true slideshow={"slide_type": ""}
# This page uses **live code**. Click the rocket button (🚀) at the top of this page, above the title, then choose "▶ Live Code". The loading may take some time so it is good to start the Live Code before reading on. The Live Code engine is ready when you see a text under the page's title, stating something like "**Launching from mybinder.org: `ready`**.
#
# **Note:** Code that you edit in the live code blocks is not saved. Any changes you make to the code blocks is lost once you move on from the page. Therefore, if you want to keep your work, save a copy of it in a local document.
#
# The code block below defines some imports and functions that will be helpful in the current page. It is run automatically when you run the "▶ Live Code" button. You may have a look at it if you like, but that is not necessary for this course.

# %% editable=true slideshow={"slide_type": ""} tags=["remove-output", "hide-input", "thebe-init"]
import pandas as pd

def display_dict(d, dict_type="nested"):
    """
    Below, some dictionaries will be define in the standard
    GreenLight format for describing models.
    This functions displays such dictionaries in a nicely
    readable format
    """
    if dict_type == "nested":
        df = pd.DataFrame.from_dict(d, orient="index")
        df.index.name = "Variable"
    elif dict_type == "flat":
        df = pd.DataFrame.from_dict(d, orient="index", columns=[""])
    display(df)


# %% [markdown] editable=true slideshow={"slide_type": ""}
# ## What we have so far

# %% [markdown] editable=true slideshow={"slide_type": ""}
# At the end of the previous section, we've finished defining the simple crop model in a Python dict. Run the code block below to load this dict into the variable `crop_definition`.

# %% editable=true slideshow={"slide_type": ""} tags=["remove-output"]
"""
Solution to Exercise 6: complete the crop definition dict with description, unit, type, definition, and reference
"""

crop_definition = {
    "W": {
        "description": "Crop dry mass",
        "unit": "g/m2",
        "type": "state",
        "definition": "LUE * ( 1 - exp(-k*LAI) ) * (1/1000000 * Iw)",  # The expression for dW/dT (for states, the definition is the right hand sand of the ODE)
        "init": "75",
        "reference": "Stanghellini (2019), Eq. 2.25. I (MJ/m2/day) is replaced by Iw (W/m2). See also Figure 2.13 there: 75 g/m2 dry mass is a reasonable value for a small crop"
    },
    "LUE": {
        "description": "Light use efficiency",
        "unit": "g crop weight per MJ PAR",
        "type": "const",
        "definition": "4.3",
        "reference": "Stanghellini (2019), Eq. 2.25. See also pg. 49 there: 4.3 is a typical middle value"
    },
    "k": {
        "description": "Light extinction coefficient",
        "unit": "-",
        "type": "const",
        "definition": "0.7",
        "reference": "Stanghellini (2019), Eq. 2.25. See also pg. 39 there: 'For many greenhouse crops, k has a value between 0.6 and 0.8'"
    },
    "LAI": {
        "description": "Leaf area index",
        "unit": "m2 leaf per m2 floor",
        "type": "aux",
        "definition": "W * F_leaves * SLA / 10000",
        "reference": "Stanghellini (2019), Eq. 2.26. "
    },
    "Iw": {
        "description": "Solar PAR radiation",
        "unit": "W PAR per m2",
        "type": "input",
        "definition": "50",
        "reference": "Stanghellini (2019), Eq. 2.25. I (MJ/m2/day) has been replaced by Iw (W/m2). The value of 50 W/m2 is given as an example"
    },
    "F_leaves": {
        "description": "Fraction of crop dry mass partitioned to the leaves",
        "unit": "-",
        "type": "const",
        "definition": "0.8",
        "reference": "Stanghellini (2019), Eq. 2.26. 0.8 is chosen to represent a vegetative crop with mostly leaves"
    },
    "SLA": {
        "description": "Specific leaf area",
        "unit": "cm2/g",
        "type": "const",
        "definition": "250",
        "reference": "Stanghellini (2019), Eq. 2.26. 250 is a middle value for a tomato crop (see Table 2.1, pg. 50 in Stanghellini 2019)"
    }   
 }

# Display the above dict
display_dict(crop_definition)

# %% [markdown]
# ## Running the model in GreenLight

# %% [markdown]
# The code block below loads the crop model definition `dict` that we've created, `crop_definition`, onto a new GreenLight object. This is done by using a Python class constructor - a method that creates a new instance of a class, in this case, an instance of the class `GreenLight`.
#
# In this code, we give `crop_definition` as the `input_prompt` argument for the `GreenLight` constructor. This sets our model definition in the new `GreenLight` instance, called `crop_mdl`.
#
# Then, the method `run()` is called for `crop_mdl`, and the model runs.

# %% tags=["remove-output"]
"""
Load the crop model definition to a GreenLight object, and then run it
"""

# Import the GreenLight package
import greenlight

# Create a new GreenLight object. Provide the dict crop_definition as input prompt
crop_mdl = greenlight.GreenLight(input_prompt=crop_definition)

# Run the model
crop_mdl.run()

# %% [markdown]
# If all went well, the model run printed out some text, which mentioned that some files were saved once the run was complete. At this moment we don't need to use these files, since the model result is also stored in the object `crop_mdl`.
#
# The code blocks below show some of the information that is stored in `crop_mdl`.

# %% tags=["remove-output"]
"""
Display some of the information that is stored in crop_mdl
"""

print("\ncrop_mdl.variables:")
display_dict(crop_mdl.variables, "flat")

print("\ncrop_mdl.var_descriptions:")
display_dict(crop_mdl.var_descriptions, "flat")

print("\ncrop_mdl.var_units:")
display_dict(crop_mdl.var_units, "flat")

print("\ncrop_mdl.var_refs:")
display_dict(crop_mdl.var_refs, "flat")

# %% tags=["remove-output"]
"""
Display the model result in a table
"""

print("\ncrop_mdl.full_sol")
display(crop_mdl.full_sol)

# %% [markdown]
# ## Displaying the model results in a graph

# %% [markdown]
# Now that we have seen that some model results have been generated, it is convenient to be able to show some graphs. The following code block creates a graph for each variable that is not a constant.

# %%
"""
Generate a graph for each variable of the model that is not a constant
"""
# %matplotlib widget
import matplotlib.pyplot as plt

for var in crop_mdl.variables.keys():
    if var not in crop_mdl.consts.keys():
        plt.figure()
        plt.plot(
            crop_mdl.full_sol["Time"],
            crop_mdl.full_sol[var]
        )
        plt.title(crop_mdl.var_descriptions[var])
        plt.ylabel(var + " (" + crop_mdl.var_units[var] + ")")
        plt.xlabel("Time (s)")
        plt.grid()
        plt.show()

# %% editable=true slideshow={"slide_type": ""}
import traceback
import ipywidgets as widgets
import pandas as pd

from IPython.display import display, clear_output

slider_names = [
    "W init",
    "Iw",
    "LUE"
]


output = widgets.Output()

# --------------------------------------------------
# 1. Define the input sliders
# --------------------------------------------------

slider_1 = widgets.FloatSlider(
    value=75,
    min=0,
    max=250,
    step=0.1,
    description=slider_names[0],
    continuous_update=False
)

slider_2 = widgets.FloatSlider(
    value=200,
    min=0,
    max=1000,
    step=1,
    description=slider_names[1],
    continuous_update=False
)

slider_3 = widgets.IntSlider(
    value=4.3,
    min=0,
    max=20,
    step=0.01,
    description=slider_names[2],
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

    try:
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
        data = model.full_sol
        
        
        # Add a new curve
        line, = ax.plot(
            data.iloc[:, 0]/3600,
            data.iloc[:, 1],
            label=f"Run {len(curves)+1} - " +
                f"{slider_names[0]}: {p1}, " +
                f"{slider_names[1]}: {p2}, " +
                f"{slider_names[2]}: {p3} "
            
        )
        
        curves.append(line)
        
        ax.legend()

        display(fig)


    except Exception as e:
        traceback.print_exc()


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
display(output)


# %%
