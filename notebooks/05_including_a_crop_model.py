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
# # Including a crop model

# %%
""" 
Imports needed for running the code
"""
# Ignore warnings during ODE solving
# Typically such warnings should be checked,
# but for the current exercise it is not important
import warnings
warnings.filterwarnings("ignore")

import os

from IPython.display import display
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import greenlight

# %% [markdown]
# ## In this lesson

# %% [markdown]
# In this lesson we will construct a simple crop model, based on a small part of Chapter 2 in [the course textbook](https://doi.org/10.1163/9789004697041). Since the goal here is to create a very simple model, we will focus on only two equations: Eq. 2.25 (pg. 49) and Eq. 2.26 (pg. 50). We will see that even with such a small model, the translation from a description in literature to a running, functioning model, is not so straightforward.

# %% [markdown]
# ### Exercise

# %% [markdown]
# Examine Eq. 2.25 and Eq. 2.26 in the course textbook (pp. 49-50), and write down the following:
# - Which variables are used in these equations?
# - For each variable:
#     - What is it called in the equations?
#     - What does it represent?
#     - What unit is it in?
#     - Is it a constant value, or does it evolve through time?
#     - Is it an input (the values should be given to the model), calculated based on other variables, or calculated using a differential equation?

# %% [markdown]
# #### Note on differential equations

# %% [markdown]
# *Add image: https://commons.wikimedia.org/wiki/File:Parabolic_trajectory.svg*
#
# If the concept of differential equations is unfamiliar to you, at this point it is sufficient to note that in Eq. 2.25, the notation $\mathrm{d}W/\mathrm{d}t$ indicates "the rate of change of $W$ as time ($t$) passes". Thus, $\mathrm{d}W/\mathrm{d}t$ indicates the *derivative* (or *differential*) of $W$ with respect to $t$. Another notation for this concept which you may have seen in the past is $y'$. In this case the derived variable is $W$, so the corresponding notation would be $W'$. 
#
# What this means in practice is that the right hand side of Eq. 2.25: 
# $$\mathrm{d}W/\mathrm{d}t = LUE \cdot \left( 1 - e^{-k \cdot LAI} \right) \cdot I$$
# is *the rate of change of $W$*. Thus, if $LUE \cdot \left( 1 - e^{-k \cdot LAI} \right) \cdot I = $ 1 g m<sup>-2</sup> d<sup>-1</sup>, then $W$ grows at a rate of 1 g m<sup>-2</sup> d<sup>-1</sup>.
#
# For more information, see [Ordinary differential equation on Wikipedia](https://en.wikipedia.org/wiki/Ordinary_differential_equation) and this chapter from [Python Programming and Numerical Methods - A Guide for Engineers and Scientists](https://pythonnumericalmethods.studentorg.berkeley.edu/notebooks/chapter22.00-ODE-Initial-Value-Problems.html).

# %% [markdown]
# ### Solution

# %% [markdown]
# #### The variables in Eq. 2.25 are:
# - $W$, representing **crop growth rate**
#     - Its unit is g m<sup>-2</sup>
#     - Its value evolves through time
#     - It is calculated based on other variables, using a differential equation
# **Note:** The unit of $\mathrm{d}W/\mathrm{d}t$, which is the rate of change of $W$, is g m<sup>-2</sup> d<sup>-1</sup>. Thus the unit of $W$ itself does not include the time factor d<sup>-1</sup> ("per day"). <br><br>
#
# - $LUE$, representing **light use efficiency**
#     - Its unit is g MJ<sup>-1</sup> PAR
#     - "Equation 2.25 assumes a constant LUE" (pg. 49). Our goal here is to create a simple crop model, so we will stick to this assumption. However, see the discussion on pg. 49 for other possible approaches
#     - As a constant value, it should be given to the model<br><br>
#
# - $k$, representing **light extinction coefficient**
#     - It is unitless: note that "$\left( 1 - e^{-k \cdot LAI} \right)$ represents the fraction of intercepted light". As a fraction it is a unitless value. This implies that $e^{-k \cdot LAI}$ and since we may consider $LAI$ as unitless (m<sup>2</sup> leaves per m<sup>2</sup> floor, resulting in $m^{2}/m^{2} = 1$), then $k$ must also be unitless
#     - Consider the text below Eq. 2.17, pg. 39: "k is not strictly constant [...] however, applying a constant k value provides an accurate enough estimation [...]". Again, since we would like to have a simple model, a constant value is currently sufficient
#     - As a constant value, it should be given to the model<br><br>
#
# - $LAI$, representing **leaf area index**
#     - See pg. 38: its unit is m<sup>2</sup> leaves per m<sup>2</sup> ground area, which we may consider as unitless ($m^{2}/m^{2} = 1$)
#     - Its value evolves through time
#     - It is calculated based on other variables, see Eq. 2.26. This equation describeds the difference between "$LAI$ on day $t$ and day $t-1$, so it may be considered a *difference equation* or a differential equation<br><br>
#
# - $I$, representing **daily light sum**
#     - Its unit is g MJ<sup>-1</sup> PAR m<sup>-2</sup>
#     - Its value evolves in time, and should be given to the model<br><br>
#
# #### The variables in Eq. 2.26 are:
# - $LAI$, see above<br><br>
#
# - $GR$, representing **crop growth rate**
#     - Its unit is g m<sup>-2</sup> d<sup>-1</sup>
#     - Its value evolves through time
#     - It is calculated based on other variables. In fact, this is precisely the value $\mathrm{d}W/\mathrm{d}t$<br><br>
#
# - $F_{leaves}$, representing **fraction partitioned to the leaves**
#     - As a fraction, it is unitless
#     - Its value evolves through time: a vegetative crop (for example, young tomato plant with no flowers) has a high $F_{leaves}$, while a mature crop with many fruit has a lower $F_{leaves}$
#     - This variable depends on other variables, see for example pg. 52<br><br>
#     
# - $SLA$, representing **specific leaf area**
#     - Its unit is cm<sup>2</sup> g<sup>-1</sup>
#     - Its value evolves through time: a vegetative crop (for example, young tomato plant with no flowers) has a high $F_{leaves}$, while a mature crop with many fruit has a lower $F_{leaves}$
#     - See pg. 50: "[SLA] varies between crop species [...] as well as with plant age, season and environmental conditions [...], but it is nonetheless often taken as a constant"

# %% [markdown]
# ### Reflection

# %% [markdown]
# Take a moment to reflect on the last exercise: how was it to list and describe all the variables of a simple (2 equations) model? Was it straightforward? Or did it require some detective work? Did you need the help of the provided solution? Does the solution require creativity and inventiveness?

# %%

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
         "definition": "I",
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
         "reference": "Stanghellini (2019), Box 2.26. " \
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

crop_mdl = greenlight.GreenLight(
    base_path=os.getcwd(), 
    input_prompt=[crop_definition, os.path.join("input", "example_weather.csv"), options], 
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
