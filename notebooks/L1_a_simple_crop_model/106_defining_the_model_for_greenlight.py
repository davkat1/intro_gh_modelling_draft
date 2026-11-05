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

# %% [markdown] editable=true slideshow={"slide_type": ""}
# # 1.6 Defining the model for GreenLight

# %% [markdown] editable=true slideshow={"slide_type": ""}
# ## Live code in this page

# %% [markdown] editable=true slideshow={"slide_type": ""}
# This page uses **live code**. Click the rocket button (🚀) at the top of this page, above the title, then choose "▶ Live Code". The loading may take some time so it is good to start the Live Code before reading on. The Live Code engine is ready when you see a text under the page's title, stating something like "Launching from mybinder.org: **ready**.
#
# **Note:** Code that you edit in the live code blocks is not saved. Any changes you make to the code blocks is lost once you move on from the page. Therefore, if you want to keep your work, save a copy of it in a local document.
#
# The code block below defines some imports and functions that will be helpful in the current page. It is run automatically when you run the "▶ Live Code" button. You may have a look at it if you like, but that is not neccesary for this course.

# %% editable=false slideshow={"slide_type": ""} tags=["remove-output", "hide-input", "thebe-init"]
import pandas as pd

def display_dict(d):
    """
    Below, some dictionaries will be define in the standard
    GreenLight format for describing models.
    This functions displays such dictionaries in a nicely
    readable format
    """
    df = pd.DataFrame.from_dict(d, orient="index")
    df.index.name = "Variable"
    display(df)


# %% [markdown] editable=true slideshow={"slide_type": ""}
# ## Going back to the model definition dict

# %% [markdown]
# In [Part 4 of this lesson](104_some_model_adjustments.ipynb#Solution-3) we've defined a Python dictionary which describes the crop model as we've defined it up to that point:

# %% editable=true slideshow={"slide_type": ""} tags=["remove-output"]
"""
From Lesson 1 part 4:
Solution to exercise 3: a crop model definition dict using Equation 2.25 and 2.26e
"""
# Method for displaying dicts in a friendly way ("pretty print")
from pprint import pprint

crop_definition = {
    "W": {
        "description": "Crop dry mass",
        "unit": "g/m2",
        "type": "state",
        "reference": "Stanghellini (2019), Eq. 2.25"
    },
    "LUE": {
        "description": "Light use efficiency",
        "unit": "g crop weight per MJ PAR",
        "type": "const",
        "reference": "Stanghellini (2019), Eq. 2.25"
    },
    "k": {
        "description": "Light extinction coefficient",
        "unit": "-",
        "type": "const",
        "reference": "Stanghellini (2019), Eq. 2.25"
    },
    "LAI": {
        "description": "Leaf area index",
        "unit": "m2 leaf per m2 floor",
        "type": "aux",
        "reference": "Stanghellini (2019), Eq. 2.25"
    },
    "I": {
        "description": "Daily light sum",
        "unit": "MJ PAR per m2 per day",
        "type": "input",
        "reference": "Stanghellini (2019), Eq. 2.25"
    },
    "fLeaves": {
        "description": "Fraction of crop dry mass partitioned to the leaves",
        "unit": "-",
        "type": "const",  # See previous Section: we treat fLeaves as constant for now
        "reference": "Stanghellini (2019), Eq. 2.26"
    },
    "SLA": {
        "description": "Specific leaf area",
        "unit": "cm2/g",
        "type": "const",
        "reference": "Stanghellini (2019), Eq. 2.26"
    }   
 }

# Display the above dict
display_dict(crop_definition)

# %% [markdown] editable=true slideshow={"slide_type": ""}
# ## Adding variable definitions to the dictionary

# %% [markdown] editable=true slideshow={"slide_type": ""}
# The description above does not include the variable definitions which were added in [Section 5 of this lesson](105_defining_relations_between_variables.html#solution-4). These can be added by the `definition` field of each variable as it is used in GreenLight.

# %% [markdown]
# ### The definition field in GreenLight

# %% [markdown] editable=true slideshow={"slide_type": ""}
# In GreenLight model descriptions, variables should have a `definition` field which describes how the variable is derived. The `definition` field works as follows:
# 1. The `definition` is always defined with a string, even if it represents a number. So use for example `"definition": "6"` and not `"definition": 6`.
# 2. For `const` variables, the `definition` should be simply a number (example: `"definition": "6"`)
# 3. For `aux` variables, the `definition` is a mathematical expression involving other variables (example: `"definition": "1-exp(-k*LAI)"`)
# 4. For `input` variables, no definition is needed since the values should be provided as a data file. A constant value (like in `const`) can be provided as a default, in case no data is available.
# 5. For `state` variables, the `definition` is a mathematical expression describing the ordinary differential equation (ODE) defining the model (see example below)

# %% [markdown]
# ### Initial values for states

# %% [markdown]
# In order for the model to run in GreenLight, `state` variables need some more information. They need an **initial value**, which indicates their value at the start of the model run. This initial value is defined by a field called `init`, and its value is given as a string which represent a value. So for example, a state variable with `"init": "0"` will start the model run with a value of 0.

# %% [markdown] editable=true slideshow={"slide_type": ""}
# ## Exercise 5: Adding the variable definitions to the model descriptions

# %% [markdown] editable=true slideshow={"slide_type": ""}
# ```{exercise}
# :label: exercise-crop-model-definitions-greenlight
# :enumerated: true
#
# Using the information you've added in [the previous section](105_defining_relations_between_variables.html#solution-4), complete the `definition` fields for the variables of the crop model. You can do this by editing and the running the code block below.
# ```

# %% editable=true slideshow={"slide_type": ""} tags=["remove-output"]
"""
Exercise 5: complete the crop definition dict with definitions for each variable
"""

crop_definition = {
    "W": {
        "description": "Crop dry mass",
        "unit": "g/m2",
        "type": "state",
        "reference": "Stanghellini (2019), Eq. 2.25",
        "definition": "LUE * ( 1 - exp(-k*LAI) ) * I",  # The expression for dW/dT
        "init": "75"  # See Figure 2.13 in Stanghellini (2019): 75 g/m2 dry mass is a reasonable value for a small crop
    },
    "LUE": {
        "description": "Light use efficiency",
        "unit": "g crop weight per MJ PAR",
        "type": "const",
        "reference": "Stanghellini (2019), Eq. 2.25",
        "definition": "4.3"  # See pg. 49 of the textbook - this is a typical middle value
    },
    "k": {
        "description": "Light extinction coefficient",
        "unit": "-",
        "type": "const",
        "reference": "Stanghellini (2019), Eq. 2.25",
        "definition": "Complete here..."  # Add any extra information as a comment
    },
    "LAI": {
        "description": "Leaf area index",
        "unit": "m2 leaf per m2 floor",
        "type": "aux",
        "reference": "Stanghellini (2019), Eq. 2.25",
        "definition": "..."  # ...
    },
    "I": {
        "description": "Daily light sum",
        "unit": "MJ PAR per m2 per day",
        "type": "input",
        "reference": "Stanghellini (2019), Eq. 2.25"
    },
    "fLeaves": {
        "description": "Fraction of crop dry mass partitioned to the leaves",
        "unit": "-",
        "type": "const",
        "reference": "Stanghellini (2019), Eq. 2.26",
        "definition": "..."  # ...
    },
    "SLA": {
        "description": "Specific leaf area",
        "unit": "cm2/g",
        "type": "const",
        "reference": "Stanghellini (2019), Eq. 2.26",
        "definition": "..."  # ...
    }   
 }

# Display the above dict
display_dict(crop_definition)

# %% [markdown] editable=true slideshow={"slide_type": ""}
# ### Solution 5

# %% [markdown] editable=true slideshow={"slide_type": ""}
# ```{solution} exercise-crop-model-definitions-greenlight
# :label: solution-crop-model-definitions-greenlight
# ```

# %% editable=true slideshow={"slide_type": ""} tags=["hide-input", "remove-output"]
"""
Solution to Exercise 5: complete the crop definition dict with definitions for each variable
"""

crop_definition = {
    "W": {
        "description": "Crop dry mass",
        "unit": "g/m2",
        "type": "state",
        "reference": "Stanghellini (2019), Eq. 2.25",
        "definition": "LUE * ( 1 - exp(-k*LAI) ) * I",  # The expression for dW/dT
        "init": "75"  # See Figure 2.13 in Stanghellini (2019): 75 g/m2 dry mass is a reasonable value for a small crop
    },
    "LUE": {
        "description": "Light use efficiency",
        "unit": "g crop weight per MJ PAR",
        "type": "const",
        "reference": "Stanghellini (2019), Eq. 2.25",
        "definition": "4.3"  # See pg. 49 of the textbook - this is a typical middle value
    },
    "k": {
        "description": "Light extinction coefficient",
        "unit": "-",
        "type": "const",
        "reference": "Stanghellini (2019), Eq. 2.25",
        "definition": "0.7"  # See pg. 39 of the textbook: “For many greenhouse crops, k has a value between 0.6 and 0.8”
    },
    "LAI": {
        "description": "Leaf area index",
        "unit": "m2 leaf per m2 floor",
        "type": "aux",
        "reference": "Stanghellini (2019), Eq. 2.25",
        "definition": "W * fLeaves * SLA / 10000"  # See Eq 2.26e, Lesson 1.4 of this course
    },
    "I": {
        "description": "Daily light sum",
        "unit": "MJ PAR per m2 per day",
        "type": "input",
        "reference": "Stanghellini (2019), Eq. 2.25"
    },
    "fLeaves": {
        "description": "Fraction of crop dry mass partitioned to the leaves",
        "unit": "-",
        "type": "const",
        "reference": "Stanghellini (2019), Eq. 2.26",
        "definition": "0.8"  # Chosen for a vegetative crop with mostly leaves
    },
    "SLA": {
        "description": "Specific leaf area",
        "unit": "cm2/g",
        "type": "const",
        "reference": "Stanghellini (2019), Eq. 2.26",
        "definition": "250"  # See Table 2.1 (pg. 50) of the textbook - 250 is a middle value for a tomato crop
    }   
 }

# Display the above dict
display_dict(crop_definition)

# %% editable=true slideshow={"slide_type": ""}
