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
#
# This book is based on **GreenLight v2.0.5**, and assumes that this is the version installed in the running system.

# %% [markdown]
# ## Defining models in GreenLight

# %% [markdown]
# Models are defined in GreenLight in a structure that is similar to what we've constructed in the previous chapter: using a [Python dictionary](https://docs.python.org/3/tutorial/datastructures.html#dictionaries) (`dict`) that defines the model variables. Like in the previous chapter, this is actually a dictionary of dictionaries. The *keys* of the model definition dictionary are the names of the variables. For each variable, the corresponding *value* is another dictionary, with the following *keys*:
# - `description` - a description of the variable
# - `unit` - the unit that the variable's values are in
# - `reference` - a reference describing where the variable definition came from
# - `definition` - a definition of the variable. This may be a single value, input data, or a calculation based on other variables
# - `type` - the type of variable, which allows GreenLight to know how to process the variable

# %% [markdown]
# ## Variable types in GreenLight

# %% [markdown]
# Variables in GreenLight have 5 possible types:
# - `const` - indicates that the variable stays constant throughout a model run
# - `input` - indicates that the values for the variable are provided as an input
# - `aux` - an auxiliary variable: a variable that is calculated based on other variables
# - `state` - a value that is defined by an ordinary differential equation
# - `function` - a function that works as a shorthand for repeated calculations
#
# In this chapter, we will focus only on the first 3 `type`s of variables: `const`, `input`, `aux`.

# %% [markdown]
# ## 3.2 Defining the tunnel model in GreenLight

# %% [markdown]
# ### 3.2.1 Example: some tunnel model variables in the GreenLight format
# In the code block below we start defining the tunnel model in a variable called `tunnel_def`, again following the text after Eq 3.9. We define: 
# - `tau` 
# - `iSun`
# - `fTunnelSky`
#
# Where:
# - The **description** is taken directly from the text under Eq. 3.9 (same as previous lesson)
# - The **unit** is also taken directly from the text under Eq. 3.9 (same as previous lesson)
# - The **reference** inidcates where the variable is describe. The text under Eq. 3.9 usually provides a good indication, but if more information was used (for example, for choosing the value for the variable), it is also included (same as previous lesson)
# - The **definition** is an estimate or example for a reasonable value. For example, for **𝜏**, Table 3.1 gives an indication (same as `value` in previous lesson)
# - The **type** for most values depends on the variable:
#   - Values that represent physical properties of the greenhouse which we don't expect to change during the calculation, will be set as `const`
#   - Values that represent weather variables that change through time will be set as `input`
#   - The variable `tTunnel` which will be calculated based on other variables will be set as `aux`
#
# **Note**: at the moment, GreenLight only supprts text strings as dictionary `keys`. Therefore, where before we defined, for example:
# ```
# "value": 0.8
# ```
#
# We now use `definition` instead of `value`, and we write `0.8` as a string, `"0.8"`:
# ```
# "definition": "0.8"
# ```
#

# %%
""" 
Example 3.2.1
Define a tunnel model for running with the GreenLight platform
"""
tunnel_def = {
    "tau": {
        "description": "Transmissivity (hemispherical) of the cover for sun radiation",
        "unit": "-",
        "reference": "Stanghellini et al. (2024), Eq. 3.2 & Table 3.1",
        "definition": "0.8",
        "type": "const"
    },
    "iSun": {
        "description": "Solar radiation",
        "unit": "W/m2",
        "reference": "Stanghellini et al. (2024), Eq. 3.2",
        "definition": "700",
        "type": "input"
    },
    "fTunnelSky": {
        "description": "View factor between tunnel and sky",
        "unit": "-",
        "reference": "Stanghellini et al. (2024), Eq. 3.5 & pg. 70",
        "definition": "0.5",
        "type": "const"
    }
}

# %% [markdown]
# ### 3.2.2 Exercise: completing the tunnel model variables in the GreenLight format
#
# In the following code block, complete the definition of `tunnel_def` as above, to include all variables described in Equation 3.9. 
#
# The exercise in the previous chapter may be used as a guide.
#
# **You may skip the variable `tTunnel` for now, we will deal with that one in the next step**.

# %%
""" 
Exercise 3.2.2
Define a tunnel model for running with the GreenLight platform
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
    "continue here...": ""
}

# %% [markdown]
# #### 3.2.2 Solution
#
# The following code block is a possible solution to **Exercise 3.2.2**

# %%
""" 
Solution 3.2.2
Define a tunnel model for running with the GreenLight platform
"""
tunnel_def = {
    "tau": {
        "description": "Transmissivity (hemispherical) of the cover for sun radiation",
        "unit": "-",
        "reference": "Stanghellini et al. (2024), Eq. 3.2 & Table 3.1",
        "definition": "0.8",
        "type": "const"
    },
    "iSun": {
        "name": "iSun",
        "description": "Solar radiation",
        "unit": "W/m2",
        "reference": "Stanghellini et al. (2024), Eq. 3.2",
        "definition": "700",
        "type": "input"
    },
    "fTunnelSky": {
        "description": "View factor between tunnel and sky",
        "unit": "-",
        "reference": "Stanghellini et al. (2024), Eq. 3.5 & pg. 70",
        "definition": "0.5",
        "type": "const"
    },
    "epsilonCover": {
        "description": "Emissivity of the cover, including effect of screen(s)",
        "unit": "-",
        "reference": "Stanghellini et al. (2024), Eq. 3.3 & Section 3.2.1",
        "definition": "1",
        "type": "const"
    },
    "alphaR": {
        "description": "Apparent transfer coefficient for thermal radiation",
        "unit": "-",
        "reference": "Stanghellini et al. (2024), Eq. 3.6 & paragraph following",
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
        "reference": "Stanghellini et al. (2024), Eq. 3.5 & pg. 70",
        "definition": "0.5",
        "type": "const"
    },
    "epsilonSoil": {
        "description": "Emissivity of the soil, including possible effect of mulch",
        "unit": "-",
        "reference": "Stanghellini et al. (2024), Eq. 3.3 & Section 3.2.1",
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
        "definition": "4",
        "type": "const"
    },
    "alphaSoil": {
        "description": "Heat transfer coefficient of the soil (including possible mulches)",
        "unit": "W/m2/K",
        "reference": "Stanghellini et al. (2024), Eq. 3.68",
        "definition": "4",
        "type": "const"
    }
}

# %% [markdown]
# ## 3.3 Defining `tTunnel` and adding it to the model definition

# %% [markdown]
# In the previous chapter, we solved an algebraic equation and found that in the tunnel model described by the textbook in Equation 3.9, 
#
# $$
# \begin{align}
# T_{tunnel} = &\\
# &\frac{ \tau I_{sun} + F_{tunnel,sky} \varepsilon_{cover} \alpha_R T_{sky} + \frac{A_{cover}}{A_{soil}} \alpha_{cover} T_{out} + F_{tunnel,soil} \varepsilon_{soil} \alpha_R T_{soil}  + \alpha_{soil} T_{soil}}{F_{tunnel,sky} \varepsilon_{cover} \alpha_R  + \frac{A_{cover}}{A_{soil}} \alpha_{cover} + F_{tunnel,soil} \varepsilon_{soil} \alpha_R +\alpha_{soil}}
# \end{align}
# $$
#
# In our implementation of the model then, `tTunnel` is a variable that is a defined by a calculation of other variables. In GreenLight, such variables have a `type` called `aux`.
#
# You may also recall from the previous chapter, that in the implementation of the interactive model, we defined:
#
# ```
# tTunnel = ( 
#             tau * iSun 
#             + fTunnelSky * epsilonCover * alphaR * tSky 
#             + aCoverOverSoil * alphaCover * tOut 
#             + tSoil * (fTunnelSoil * epsilonSoil * alphaR + alphaSoil)
#         ) / (
#             fTunnelSky * epsilonCover * alphaR 
#             + aCoverOverSoil * alphaCover 
#             + fTunnelSoil * epsilonSoil * alphaR 
#             + alphaSoil
#         )
# ```
#
# The same will be done here, with the above definition of `tTunnel` set as a string, under the `definition` attribute. To enhance readability, we will use backslashes that break up lines of code.
#
# In the following code block, the *key* `"tTunnel"` is added to the `tunnel_def` dictionary, with *value* holding the `definition` and `type` as explained above:

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
        "+ fTunnelSky * epsilonCover * alphaR * tSky " \
        "+ aCoverOverSoil * alphaCover * tOut " \
        "+ tSoil * (fTunnelSoil * epsilonSoil * alphaR + alphaSoil)" \
    ") / ( " \
        "fTunnelSky * epsilonCover * alphaR " \
        "+ aCoverOverSoil * alphaCover " \
        "+ fTunnelSoil * epsilonSoil * alphaR " \
        "+ alphaSoil " \
    ")"
    }

# %% [markdown]
# ## 3.4 Setting the model definition as GreenLight model

# %% [markdown]
# Before starting, we will import some packages which will be used later. Run the code block below, but there is no need to focus on the details there.

# %% [markdown]
# ## 3.1 Imports for Chapter 3

# %%
""" 
Imports needed for running the code
"""

# Ignore warnings during ODE solving
# Typically such warnings should be checked,
# but for the current exercise it is easier to just ignore them
import warnings
warnings.filterwarnings("ignore")

# For browsing for files in the operating system
import os

# For editing model output as DataFrames
import pandas as pd

# For displaying DataFrames
from IPython.display import display

# For making plots
import matplotlib.pyplot as plt

# For using the GreenLight platform
import greenlight


# %% [markdown]
# ## Setting up a `GreenLight` instance

# %% [markdown]
# GreenLight defines a `GreenLight` [class](https://docs.python.org/3/tutorial/classes.html), where every model is an instance of this class.
#
# The full list of attributes that `GreenLight` instances have is given in [the documentation of GreenLight](https://github.com/davkat1/GreenLight/blob/main/greenlight/core.py). For the current lesson, it is good to be aware of the following attributes:
# - `input_prompt` - this is model definition that is provided to the GreenLight instance. It is used to define the model and run it
# - `variables` - after the model has been run, this is a dictionary that contains all the model variables as *keys* and their definitions as *values*
# - `var_units` - after the model has been run, this is a dictionary that contains all the model variables as *keys* and their units as *values*
# - `var_descriptions` - after the model has been run, this is a dictionary that contains all the model variables as *keys* and their descriptions as *values*
# - `consts` - after the model has been run, this is a dictionary that contains as *keys* the model variables that have been set with a `"type": "const"`. The *values* of the dictionary are the variable definitions
# - `inputs` - after the model has been run, this is a dictionary that contains as *keys* the model variables that have been set with a `"type": "input"`. The *values* of the dictionary are the variable definitions
# - `aux` - after the model has been run, this is a dictionary that contains as *keys* the model variables that have been set with a `"type": "aux"`. The *values* of the dictionary are the variable definitions
# - `input_data` - after the model has been run, this is a pandas DataFrame which contains any input data provided to the model
# - `full_sol` - after the model has been run, this is a pandas DataFrame which contains the model results, i.e., the calculated values for all variables throughout the simulated period

# %% [markdown]
# In the following code block, we create a new instance of the class `GreenLight`, called `mdl`. When creating this instance (calling the constructor), we pass as the `input_prompt` argument the variable `tunnel_def` that we've defined above. This gives `mdl` our definition of the tunnel model as the model it should be running.

# %%
# Create a GreenLight instance called mdl,
# set the input_prompt of mdl as the
# tunnel model defined above
mdl = greenlight.GreenLight(
    input_prompt=tunnel_def
)

# %% [markdown]
# We can see that a new variable `mdl` has been created, and it has an [attribute](https://docs.python.org/3/tutorial/classes.html) called `input_prompt`, which contains our model definition:

# %%
# Display the input_prompt attribute of mdl
display(mdl.input_prompt)

# %% [markdown]
# ## 3.5 Running the model in GreenLight

# %% [markdown]
# Now that the model has been stored in a `GreenLight` instance, the instance can be run, which performs a model simulation:

# %%
# Run the simulation for mdl
mdl.run()

# %% [markdown]
# Running the code block above should generate some output, which shows how long the simulated period was (by default, 1 day), and some information about files that have been created by the simulation.

# %% [markdown]
# ## 3.6 Displaying model output in a table

# %% [markdown]
# Besides creating output files, the `mdl.run()` command also stored the model output in the `mdl` instance. We can access this stored output by using the code below.
#
# The solution (simulation result) of the model is stored in the attribute `full_sol`. This variable is a [pandas DataFrame](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html), which contains the calculated values of the model variables:

# %%
# Display the model solution
display(mdl.full_sol)

# %% [markdown]
# To provide more information, we can also include the variable descritions and units, which we've ensured to include in our model definition.
#
# The variable descriptions are stored in the attribute `var_descriptions` in the form of a dictionary:

# %%
# Display the variable descriptions
display(mdl.var_descriptions)

# %% [markdown]
# The variable units are stored in the attribute `var_units` in the form of a dictionary:

# %%
# Display the variable units
display(mdl.var_units)


# %% [markdown]
# To create one DataFrame which contains the model result, together with the description and unit of each variable, we may use the following function:

# %%
def display_table(full_sol):
    """
    Create a new DataFrame called output_df
    which contains variable names, descriptions, and units
    as well as model output.
    Then display this DataFrame

    :param full_sol: A full_sol attribute of a GreenLight instance, after the model has been run
    """
    
    # Make a copy of the model solution
    table_df = mdl.full_sol.copy()
    
    # Set the variable names, descriptions, and units
    # as a MultiIndex of the DataFrame
    table_df.columns = pd.MultiIndex.from_arrays(
        [
            # The original index in mdl.full_sol - the variable names
            table_df.columns,  
    
            # The variable descriptions
            # If there is no description, use "no_description"
            [mdl.var_descriptions.get(col, "no_description")          
             for col in table_df.columns],  
    
            # The variable units
            # If there is no unit, use "no_unit_defined"
            [mdl.var_units.get(col, "no_unit_defined")
             for col in table_df.columns],
        ],
        # Give names to the indexes
        names=["Variable", "Description", "Unit"]
    )
    
    # Display table_df
    display(
        table_df.style
          .format("{:.2f}")  # Limit numbers to 2 digits after the decimal
          .set_properties(**{"text-align": "left"})  # align left
          .set_table_styles([  # align headers to the left
              {"selector": "th", "props": [("text-align", "left")]}
          ])
    )

display_table(mdl.full_sol)

# %% [markdown]
# Some things to notice about the model output:
#
# First of all, we can see that a **Time** variable has been added to the model. GreenLight always simulates the model through time, and by default, the modelled simulation period is 1 day. We can see that no unit for **Time** has been defined, which in GreenLight means that the default time unit, seconds, is used. The output is given in 1 hour intervals (3600 s). We can see that 1 day has been simulated by the fact that 24 rows have been generated.
#
# Another obvious thing in the model output is that all rows are the same: the values for **iSun**, **tSky**, **tOut**, and **tSoil** are constant, which results in a constant value for **tTunnel** (similar to what we have seen in the previous chapter). In the next section we will change that.
#
# Lastly, we can also see that the generated output table does not contain all variables. We do not see in this table the variables which we've defined as constants, with `"type": "const"`. In order to see the constants, we may do the following:

# %%
# Display the constants stored in mdl
display(mdl.consts)


# %% [markdown]
# ## 3.7 Displaying model output in a graph

# %% [markdown]
# It is often more informative to display simulation results in a graphs rather than a table. Since we will want to do this often, we will define a function `display_graphs` that creates multiple graphs from the model simulation results. The explanation about the function is provided in the documentation inside the code block below:

# %%
def display_graphs(full_sol, vars_to_plot, title, ylabel, line_style):
    """
    Display multiple graphs generated from a model solution full_sol

    :param full_sol: A full_sol attribute of a GreenLight instance, after the model has been run
    :chosen_vars: A list of variable names in full_sol to be displayed in the graph
    :title: The title to show on top of the graph
    :ylabel: The label to show on the y axis
    :line_style: The style of the lines. 
                 Use '-' for full lines, '--' for dashed, 
                 '-o' for full with circles showing the values  
    """
    # Create a new matplotlib figure
    plt.figure(figsize=(10, 6))

    # Plot each variable in the graph
    for var in vars_to_plot:
        plt.plot(full_sol["Time"], full_sol[var], line_style, label=var)

    # Add axis labels, title, legend, grid 
    plt.xlabel("Time (s)")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.show()


# %% [markdown]
# We can use the function above to display some graphs of the simulation result:

# %%
# Graph the simulated temperatures
display_graphs(mdl.full_sol, ["tTunnel", "tOut",  "tSoil", "tSky"],"Temperatures", "°C", '-o')

# Graph the solar radiation
display_graphs(mdl.full_sol, ["iSun"],"Radiation", "W/m2", '-o')

# %% [markdown]
# These graphs show constant values in time, like we saw in the [output table](#3.6-Displaying-model-output-in-a-table). That will change soon.

# %% [markdown]
# ## 3.8 Adding variable weather input

# %% [markdown]
# As mentioned above, the model simulation is not very interesting if the weather inputs are constant. In the following exercise, we will use a weather data file as an input to the model.
#
# The file `input\example_weather.csv` is included with this course. The following code block loads and displays it:

# %%
# Point to the location of the weather file, using the local operating system logic
weather_file = os.path.abspath(os.path.join("input", "example_weather.csv"))

# Load the file contents as a DataFrame and display it
display(pd.read_csv(weather_file))

# %% [markdown]
# You can see that the weather file contains exactly the information we need as input: **iSun**, **tOut**, **tSky**, and **tSoil**. It also contains a variable **Time**, with unit `s` (seconds), which starts at 0 and continues in 300 second (5 minute intervals). The last row has a Time value of 9590100 seconds. A day has 60x60x24 = 86400 seconds. The last row represents a measurement between second 9590100 and 9590400. The data therefore represents 9590400/86400 = 111 days.

# %% [markdown]
# ## About this weather dataset

# %% [markdown]
# ~~
# TO DO TODO TODO
# # To do

# %% [markdown]
# ## Before running the new model

# %% [markdown]
# Before running the model with the input weather data, we will make some technical modifications which will help us in the next steps.
#
# First, we will set an `options` variable which will define some simulation settings: 
# - Run the model from time point `0` to time point `16*86400`, so that only the first 16 days of input data will be read
# - Ensure that the model calculates the values at every 5 minutes (300 seconds), and creates an output with a 5 minute interval (this will be useful later)

# %%
# Set model options
options = {
    "options": {
        "t_start":"0",  # Start reading the input data at time point 0
        "t_end": str(16 * 86400),  # Stop reading the input data at day 16 (86400 = seconds in a day)
        "t_eval": "300",  # Calculate variables in 5 minute intervals
        "output_step": "300"  # Create output with 5 minute intervals
    }
}

# %% [markdown]
# The next modification is a small workaround related to the limitations of GreenLight. Typically, GreenLight expects at least one variable with `"type": "state"`. This ensures that the model run follows the time units, and reads the input data correctly. For now, we will just add another variable to `tunnel_def`, which we will call `dummy`:

# %%
tunnel_def["dummy"] = {
        "description": "Dummy variable",
        "unit": "-",
        "reference": "Used to get the model going",
        "type": "state",
        "definition": "0",
        "init": "0"
    }

# %% [markdown]
# ## Running the model with variable input data

# %% [markdown]
# With the above, we can create a new instance of the class `GreenLight`, but we will add `weather_file` and `options` to the input prompt:

# %%
# Create a new instance of GreenLight
# input_prompt includes weather_file and options
mdl_2 = greenlight.GreenLight(
    input_prompt=[tunnel_def, weather_file, options], 
    )

# Display the input_prompt attribute of mdl_2
display(mdl_2.input_prompt)

# %%
# Run the new model
mdl_2.run()

# %% [markdown]
# After running the above code block, we see several things:
# 1. We see that the model loaded data from the file `example_weather.csv`, with an indication of where that file was
# 2. We see that the simulated time was (almost) 16 days
# 3. We see that some output files were generated

# %% [markdown]
# ## Displaying the results of the model with variable weather data

# %% [markdown]
# We can use the functions we've defined earlier to display the results of the new simulation:

# %%
# Graph the simulated temperatures
display_graphs(mdl_2.full_sol, ["tTunnel", "tOut",  "tSoil", "tSky"],"Temperatures", "°C", '-')

# Graph the solar radiation
display_graphs(mdl_2.full_sol, ["iSun"],"Radiation", "W/m2", '-')

# %% [markdown]
# ### 3.8.1 Exercise: modifying the weather file

# %% [markdown]
# Find the weather file `input\example_weather.csv`. Create a copy of this file, and fill the data points with a dataset of your choosing. For example, try to search online for weather data from where you are right now. Then, try to run a simulation with your weather dataset.
#
# You will most likely find that it is difficult to get data for **tSky** and **tSoil**. For **tSky**, you can use the values for **tOut** minus 20 °C, which is a reasonable rough estimate. For **tSoil**, you can use a constant value, of the average outdoor air temperature throughout the whole year. Or use the same values as in `input\example_weather.csv`.

# %% [markdown]
# ## Reflection

# %% [markdown]
# Before moving on, take a moment to reflect on the previous exercise?
# - How was the process of finding the dataset that you wanted?
# - How was it to format the dataset to the same format as `input\example_weather.csv`?
# - How was the process of including the new dataset in the simulation? Did you succeed?
# - How does `tTunnel` behave in your simulation, compared to the one with the example weather data? Is it colder? hotter? Does it behave in unexpected ways?

# %% [markdown]
# ## Summary

# %% [markdown]
# ~~
# TO DO TODO TODO
# # To do

# %% [markdown]
# ## Before moving on

# %% [markdown]
# Before moving on, let us repeat the simulation above, but run it only for the last day:

# %%
# Set model options
options = {
    "options": {
        "t_start":str(15 * 86400),  # Start reading the input data at day 15
        "t_end": str(16 * 86400),  # Stop reading the input data at day 16 (86400 = seconds in a day)
        "t_eval": "300",  # Calculate variables in 5 minute intervals
        "output_step": "300"  # Create output with 5 minute intervals
    }
}

# Create a new instance of GreenLight
# input_prompt includes weather_file and options
mdl_3 = greenlight.GreenLight(
    input_prompt=[tunnel_def, weather_file, options], 
    )

mdl_3.run()

# Graph the simulated temperatures
display_graphs(mdl_3.full_sol, ["tTunnel"],"tTunnel", "°C", '-')

# %% [markdown]
# We can see something interesting happening around the middle of the day: `tTunnel` goes from almost 25 °C to less than 10 °C, in a very short time span. This seems a little strange, and not likely to happen in a real greenhouse. In the next chapter, we will see why this happens in this simulation, and how this model behaviour may be improved

# %%
"""
Maybe not needed 
"""
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
