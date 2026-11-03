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
# # 1.3 Defining the crop model in a Python dictionary

# %% [markdown] editable=true slideshow={"slide_type": ""}
# ## Using live code in this page

# %% [markdown] editable=true slideshow={"slide_type": ""}
# In this page we will be using **live code** for the first time in this course. To start, click the rocket button (🚀) at the top of this page, above the title. Then choose "▶ Live Code". The loading may take some time so it is good to start the Live Code before reading on, so it is ready when you need it.
#
# If the Live Code fails to load for whatever reason, you can try clicking the rocket button (🚀) and choosing **Binder** instead.
#
# The material in this page contains **editable Python code blocks**. Once the Live Code engine is ready (you should see a text under the page's title, stating something like "Launching from mybinder.org: **ready**), all code blocks become editable. Simply click anywhere on the text in the code block, edit in, and then click *run*. As a first try, you may try the code below.

# %% editable=true slideshow={"slide_type": ""} tags=["remove-output"]
"""
Editable code block for testing
"""

out_text = "Hi! I'm <...enter whatever you would like here...>!"

print(out_text)

# %% [markdown] editable=true slideshow={"slide_type": ""}
# ## Towards implementing the crop model in GreenLight

# %% [markdown] editable=true slideshow={"slide_type": ""}
# The main goal of this lesson is to implement the crop model that we described in the previous section by using the [GreenLight modelling platform](https://github.com/davkat1/greenlight).  [GreenLight](https://github.com/davkat1/greenlight) has been originally developed as [an open-source model for greenhouses with a tomato crop](https://doi.org/10.1016/j.biosystemseng.2020.03.010). Since then, it has been expanded to be used as a modelling platform where [various model components can be combined](https://greenlight.readthedocs.io/en/latest/user/modifying_and_combining_models.html). GreenLight is therefore no longer a singular model, but allows to define and run models in a structured way, which will be used in this chapter.
#
# This course is based on **GreenLight v2.0.7**.

# %% [markdown]
# ## Defining models in GreenLight

# %% [markdown]
# Models are defined in GreenLight using a [Python dictionary](https://docs.python.org/3/tutorial/datastructures.html#dictionaries) (`dict`) that defines the model variables. Each variable is itself defined using a dictionary, so the model definition is in fact a dictionary of dictionaries. The *keys* of the model definition dictionary are the names of the variables. For each variable, the corresponding *value* is another dictionary, with the following *keys*:
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
# In this course, we will focus only on the first 4 `type`s of variables: `const`, `input`, `aux`, and `state`.

# %% [markdown] editable=true slideshow={"slide_type": ""}
# ## Exercise 2: Defining the crop model in a dict

# %% [markdown] editable=true slideshow={"slide_type": ""}
# ```{exercise}
# :label: exercise-crop-definition-1
# :enumerated: true
#
# Go back to [Solution 1 from the previous page](../102_variables_of_the_model.html#Solution-1) and create a model definition dictionary which implements the information there. Follow the example in the next code block, and complete it with the rest of the variables. For now, fill only the keys `desription`, `unit`, `type`, and `reference`, by using the following considerations:
# - **Description:** A textual description of what the variable represents
# - **Unit:** The units of the variables. For unitless variables, set the `unit` as `"-"`.
# - **Type:**
#   - Variables defined by a differential equation have a type `"state"`
#   - Constant variables have a type `"const"`
#   - Variables that have velus that are given to the model, but are not constant, have a type `"input"`
#   - Variables that are calculated based on other variables have a type `"aux"`
# - **Reference:** The goal of this field is to allow future users of the model to understand and check the choices made regarding the described variable. In this case, you may give the reference `"Stanghellini (2019)"`, and include the Equation where the variable is described.
#
# ```

# %% editable=true slideshow={"slide_type": ""} tags=["remove-output"]
"""
Exercise 2: complete the crop definition dict with description, unit, type, and reference
"""

# Method for displaying dicts in a friendly way ("pretty print")
from pprint import pprint

crop_definition = {
    "W": {
        "description": "Crop dry mass",
        "unit": "g/m2",
        "type": "state",
        "reference": "Stanghellini (2019), Eq. 2.25."
    },
    "LUE": {
        "description": "Light use efficiency",
        "unit": "g crop weight per MJ PAR",
        "type": "const",
        "reference": "Stanghellini (2019), Eq. 2.25"
    },
    "Continue here...": {
        
    }
}

# Display the above dict
pprint("crop_definition dict:")
pprint(crop_definition)

# %% [markdown] editable=true slideshow={"slide_type": ""}
# ### Solution 2

# %% [markdown] editable=true slideshow={"slide_type": ""}
# ```{solution} exercise-crop-definition-1
# :label: solution-crop-definition-1
# ```

# %% editable=true slideshow={"slide_type": ""} tags=["hide-input", "remove-output"]
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
        "type": "state",
        "reference": "Stanghellini (2019), Eq. 2.25"
    },
    "I": {
        "description": "Daily light sum",
        "unit": "MJ PAR per m2",
        "type": "input",
        "reference": "Stanghellini (2019), Eq. 2.25"
    },
    "GR": {
        "description": "Crop growth rate",
        "unit": "g/m2/d",
        "type": "aux",
        "reference": "Stanghellini (2019), Eq. 2.26"
    },
    "fLeaves": {
        "description": "Fraction of crop dry mass partitioned to the leaves",
        "unit": "-",
        "type": "aux",
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
pprint("crop_definition dict:")
pprint(crop_definition)
