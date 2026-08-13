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
# # 3. Implementing the "tunnel" model in the GreenLight platform

# %% [markdown]
# In the previous chapters, we've implemented an interactive model of a greenhouse "tunnel" (a theoretical greenhouse with no ventilation, no crop, and cover temperature equal to air temperature). The calculation we've made was **static**, in the sense that it represented the tunnel greenhouse during a single moment: the outdoor weather conditions (solar radiation, outdoor air temperature, sky temperature, soil temperature) were provided as single values.
#
# The static approach was quite limited, since in practice, outdoor conditions are constantly changing, and it is interesting to see the behaviour of the greenhouse through time. We will do this in the current chapter, and we will use the [GreenLight modelling platform](https://github.com/davkat1/greenlight) for that.

# %% [markdown]
# ## What is GreenLight?

# %% [markdown]
# [GreenLight](https://github.com/davkat1/greenlight) has been originally developed as [an open-source model for greenhouses with a tomato crop](https://doi.org/10.1016/j.biosystemseng.2020.03.010). Since then, it has been expanded to be used as a modelling platform where [various model components can be combined](https://github.com/davkat1/GreenLight/blob/main/docs/modifying_and_combining_models.md). GreenLight is therefore no longer a singular model, but allows to define and run models in a structured way, which will be used in this chapter.

# %% [markdown]
# ## Defining models in GreenLight

# %% [markdown]
# Models are defined in GreenLight in a structure that is similar to what we've constructed in the previous chapter. Models are defined using a [Python dictionary](https://docs.python.org/3/tutorial/datastructures.html#dictionaries) (`dict`) that defines the model variables. Like in the previous chapter, we use a dictionary of dictionaries. The *keys* of the model definition dictionary are the names of the variables. For each variable, the corresponding dictionary *value* is its own dictionary, with the following *keys*:
# - **description** - a description of the variable
# - **unit** - the unit that the variable's values are in
# - **reference** - a reference describing where the variable definition came from
# - **definition** - a definition of the variable. This may be a single value, input data, or a calculation based on other variables
# - **type** - the type of variable, see more information below

# %% [markdown]
# ## 3.2 Defining the tunnel model in GreenLight

# %% [markdown]
# ### 3.2.1 Example: some tunnel model variables in the GreenLight format
# In the code block below we start defining `tunnel_def`, again following the text after Eq 3.9. We define: 
# - `tau` 
# - `iSun`
# - `fTunnelSky`
#
# Where:
# - The **description** is taken directly from the text under Eq. 3.9 (same as previous lesson)
# - The **reference** is taken from the text under Eq. 3.9. If no reference is given, we refer simply to Eq. 3.9 (same as previous lesson)
# - The **definition** is an estimate or example for a reasonable value. For example, for **𝜏**, Table 3.1 gives an indication (same as `value` in previous lesson)
# - **type** - ~~~add some information about this here

# %%
""" 
Example 3.2.1
Define tunnel model for running with the GreenLight platform
"""
tunnel_def = {
    "tau": {
        "description": "Transmissivity (hemispherical) of the cover for sun radiation",
        "unit": "-",
        "reference": "Stanghellini et al. (2024), Eq. 3.2",
        "definition": "0.7",
        "type": "const"
    },
    "iSun": {
        "description": "Solar radiation",
        "unit": "W/m2",
        "reference": "Stanghellini et al. (2024), Eq. 3.9",
        "definition": "700",
        "type": "input"
    },
    "fTunnelSky": {
        "description": "View factor between tunnel and sky",
        "unit": "-",
        "reference": "Stanghellini et al. (2024), Eq. 3.5",
        "definition": "0.5",
        "type": "const"
    }
}

# %% [markdown] jupyter={"source_hidden": true}
# ### 3.2.2 Exercise: completing the tunnel model variables in the GreenLight format
#
# In the following code block, complete the definition of `tunnel_def` as above, to include all variables described in Equation 3.9. 
#
# **You may skip the variable `tTunnel` for now, we will deal with that one in the next step**.

# %%
""" 
Exercise 3.2.2
Define tunnel model for running with the GreenLight platform
"""
tunnel_def = {
    "tau": {
        "description": "Transmissivity (hemispherical) of the cover for sun radiation",
        "unit": "-",
        "reference": "Stanghellini et al. (2024), Eq. 3.2",
        "definition": "0.7",
        "type": "const"
    },
    "iSun": {
        "description": "Solar radiation",
        "unit": "W/m2",
        "reference": "Stanghellini et al. (2024), Eq. 3.9",
        "definition": "700",
        "type": "input"
    },
    "fTunnelSky": {
        "description": "View factor between tunnel and sky",
        "unit": "-",
        "reference": "Stanghellini et al. (2024), Eq. 3.5",
        "definition": "0.5",
        "type": "const"
    },
    "continue here...":
}

# %% [markdown]
# #### 3.2.2 Solution
#
# The following code block is a possible solution to **Exercise 3.2.2**

# %%
""" 
Solution 3.2.1
Define tunnel model for running with the GreenLight platform
"""
tunnel_def = {
    "tau": {
        "description": "Transmissivity (hemispherical) of the cover for sun radiation",
        "unit": "-",
        "reference": "Stanghellini et al. (2024), Eq. 3.2",
        "definition": "0.7",
        "type": "const"
    },
    "iSun": {
        "description": "Solar radiation",
        "unit": "W/m2",
        "reference": "Stanghellini et al. (2024), Eq. 3.9",
        "definition": "700",
        "type": "input"
    },
    "fTunnelSky": {
        "description": "View factor between tunnel and sky",
        "unit": "-",
        "reference": "Stanghellini et al. (2024), Eq. 3.5",
        "definition": "0.5",
        "type": "const"
    },
    "epsCover": {
        "description": "Emissivity of the cover, including effect of screen(s)",
        "unit": "-",
        "reference": "Stanghellini et al. (2024), Eq. 3.3",
        "definition": "1",
        "type": "const"
    },
    "alphaR": {
        "description": "Apparent transfer coefficient for thermal radiation",
        "unit": "-",
        "reference": "Stanghellini et al. (2024), Eq. 3.6",
        "definition": "6",
        "type": "const"
    },
    "tSky": {
        "description": "Apparent temperature of the sky (depends, among other things, on cloudiness)",
        "unit": "°C",
        "reference": "Stanghellini et al. (2024), Eq. 3.9",
        "definition": "0",
        "type": "input"
    },
    "tOut": {
        "description": "Temperature of the air outside the greenhouse",
        "unit": "°C",
        "reference": "Stanghellini et al. (2024), Eq. 3.9",
        "definition": "30",
        "type": "input"
    },
    "tSoil": {
        "description": "Temperature of the soil surface",
        "unit": "°C",
        "reference": "Stanghellini et al. (2024), Eq. 3.9",
        "definition": "35",
        "type": "input"
    },
    "fTunnelSoil": {
        "description": "View factor between tunnel and soil",
        "unit": "-",
        "reference": "Stanghellini et al. (2024), Eq. 3.5",
        "definition": "0.5",
        "type": "const"
    },
    "epsSoil": {
        "description": "Emissivity of the soil, including possible effect of mulch",
        "unit": "-",
        "reference": "Stanghellini et al. (2024), Eq. 3.3",
        "definition": "1",
        "type": "const"
    },
    "aCoverOverSoil": {
        "description": "Surface area of cover per unit surface area of soil",
        "unit": "-",
        "reference": "Stanghellini et al. (2024), Eq. 3.7. This variable is used to represent aCover divided by aSoil",
        "definition": "1.2",
        "type": "const"
    },
    "alphaCover": {
        "description": "Heat transfer coefficient of the cover material (including possible screens)",
        "unit": "W/m2/K",
        "reference": "Stanghellini et al. (2024), Eq. 3.7",
        "definition": "6",
        "type": "const"
    },
    "alphaSoil": {
        "description": "Heat transfer coefficient of the soil (including possible mulches)",
        "unit": "W/m2/K",
        "reference": "Stanghellini et al. (2024), Eq. 3.68",
        "definition": "5",
        "type": "const"
    }
}

# %% [markdown]
# ## 3.3 Defining `tTunnel` and adding it to the model definition

# %% [markdown]
# - we define tTunnel based on the previous calculation \ algebraic solution
# - Explain what happens below

# %%
"""
Add the variable tTunnel to the tunnel model definition tunnel_def
"""
tunnel_def["tTunnel"] = {
        "description": "Temperature of the unventilated greenhouse",
        "unit": "°C",
        "reference": "Stanghellini et al. (2024), Eq. 3.9 (rearranged to isolate tTunnel)",
        "type": "aux",
        "definition": "(" \
        "tau * iSun " \
        "+ fTunnelSky * epsCover * alphaR * tSky " \
        "+ aCoverOverSoil * alphaCover * tOut " \
        "+ tSoil * (fTunnelSoil * epsSoil * alphaR + alphaSoil)" \
    ") / ( " \
        "fTunnelSky * epsCover * alphaR " \
        "+ aCoverOverSoil * alphaCover " \
        "+ fTunnelSoil * epsSoil * alphaR " \
        "+ alphaSoil " \
    ")"
    }

# %% [markdown]
# ## 3.1 Imports for Chapter 3

# %% [markdown]
# The following code block defines imports that will be used later in this notebook. There's no need to read through this code, simply run it and move to the next section

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
# ## 3.4 Setting the model definition as GreenLight model

# %% [markdown]
# Explanation of the code below

# %%
mdl = greenlight.GreenLight(
    base_path=os.getcwd(), 
    input_prompt=tunnel_def, 
    output_path=os.path.join("output", "output.csv")
)

# %% [markdown]
# ## 3.5 Running the model in GreenLight

# %% [markdown]
# Explanation of the code below

# %%
mdl.run()

# %% [markdown]
# ## 3.6 Displaying model output in a table

# %% [markdown]
# Explanation of the code below

# %%
output_df = mdl.full_sol.copy()

output_df.columns = pd.MultiIndex.from_arrays(
    [
        output_df.columns,
        [mdl.var_descriptions.get(col, "no_description") 
         for col in output_df.columns],
        [mdl.var_units.get(col, "no_unit_defined")
         for col in output_df.columns],
    ],
    names=["Variable", "Description", "Unit"]
)

display(
    output_df.style
      .format("{:.2f}")
      .set_properties(**{"text-align": "left"})
      .set_table_styles([
          {"selector": "th", "props": [("text-align", "left")]}
      ])
)

# %%
"""
Load simulation result
"""
output_df = pd.read_csv(os.path.join("output", "output.csv"), header=[0,1,2], low_memory=False)

display(
    output_df.style
      .hide(axis="index")
      .format("{:.2f}")
      .set_properties(**{"text-align": "left"})
      .set_table_styles([
          {"selector": "th", "props": [("text-align", "left")]}
      ])
)

# %% [markdown]
# Explanation of the output above

# %% [markdown]
# ## 3.7 Displaying model output in a graph

# %% [markdown]
# Explanation of the code below

# %%
"""
Make graphs
"""

def display_output(output_df, chosen_vars, titles, ylabels, line_style):
    for vars_to_plot, title, ylabel in zip(chosen_vars, titles, ylabels):
        plt.figure(figsize=(10, 6))
        
        for var in vars_to_plot:
            plt.plot(output_df["Time"], output_df[var], line_style, label=var)
        
        plt.xlabel("Time (s)")
        plt.ylabel(ylabel)
        plt.title(title)
        plt.legend()
        plt.grid(True)
        plt.show()

def model_table(mdl):
    display(pd.DataFrame(mdl.variables.items(), columns=["Variable", "Definition"])
            .style
                .hide(axis="index")
                .set_properties(**{"text-align": "left", "font-family": "monospace"})
                .set_table_styles([
                    {"selector": "th", "props": [("text-align", "left")]}
              ])
        )

display_output(output_df, [["tTunnel", "tOut",  "tSoil", "tSky"], ["iSun"]], ["Temperatures", "Radiation"], ["°C", "W/m2"], '-o')
model_table(mdl)

# %% [markdown]
# Explanation of the output above

# %% [markdown]
# ## 3.8 Adding variable weather input

# %% [markdown]
# Explain what's happening here, also document where the weather data is coming from

# %%
# New model
options = {
    "options": {
        "t_start":"0",
        "t_end": str(16 * 24 * 60 * 60),
        "output_step": "300",
        "t_eval": "300"
    }
}

tunnel_def["dummy"] = {
        "description": "Dummy variable",
        "unit": "-",
        "reference": "Used to get the model going",
        "type": "state",
        "definition": "0",
        "init": "0"
    }

mdl_2 = greenlight.GreenLight(
    base_path=os.getcwd(), 
    input_prompt=[tunnel_def, os.path.join("input", "example_weather.csv"), options], 
    output_path=os.path.join("output", "output_2.csv")
)
mdl_2.run()

# %%
"""
Make graphs
"""

# Load simulation result
output_2 = pd.read_csv(os.path.join("output", "output_2.csv"), header=[0,1,2], low_memory=False)

display_output(output_2, [["tTunnel", "tOut",  "tSoil", "tSky"], ["iSun"]], ["Temperatures", "Radiation"], ["°C", "W/m2"], '-')
model_table(mdl_2)

# %% [markdown]
# ### 3.8.1 Exercise: modifying the weather file

# %% [markdown]
# - Make a new weather file, modify it, run the sim with it

# %% [markdown]
# ## Reflection

# %% [markdown]
# To do

# %% [markdown]
# ## Next step

# %% [markdown]
# - Explain why this isn't good enough
# - Save the def file for future use
