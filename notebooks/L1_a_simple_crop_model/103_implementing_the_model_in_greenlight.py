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
# # Implementing the crop model in GreenLight

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
# ## Implementing the crop model in GreenLight

# %% [markdown] editable=true slideshow={"slide_type": ""}
# In this section, we will implement the crop model that we described in the previous section by using the [GreenLight modelling platform](https://github.com/davkat1/greenlight).  [GreenLight](https://github.com/davkat1/greenlight) has been originally developed as [an open-source model for greenhouses with a tomato crop](https://doi.org/10.1016/j.biosystemseng.2020.03.010). Since then, it has been expanded to be used as a modelling platform where [various model components can be combined](https://greenlight.readthedocs.io/en/latest/user/modifying_and_combining_models.html). GreenLight is therefore no longer a singular model, but allows to define and run models in a structured way, which will be used in this chapter.
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
# <dl>
#     <dt>- **Description:** A textual description of what the variable represents</dt>
#     <dt>- **Unit:** The units of the variables. For unitless variables, set the `unit` as `"-"`.</dt>
#     <dt>- **Type:**</dt>
#         <dd>- Variables defined by a differential equation have a type `"state"`</dd>
#         <dd>- Constant variables have a type `"const"`</dd>
#         <dd>- Variables that have velus that are given to the model, but are not constant, have a type `"input"`</dd>
#         <dd>- Variables that are calculated based on other variables have a type `"aux"`</dd>
#     <dt>- **Reference:** The goal of this field is to allow future users of the model to understand and check the choices made regarding the described variable. In this case, you may give the reference `"Stanghellini (2019)"`, and include the Equation where the variable is described.</dt>
# </dl>
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

# %% [markdown]
# ## Reorganizing the model equations

# %% [markdown]
# Before moving on, it is helpful to slightly reorganize the model equations:
#
# \begin{equation*}
# \mathrm{d}W/\mathrm{d}t = LUE \cdot \left( 1 - e^{-k \cdot LAI} \right) \cdot I
# \tag{2.25}
# \end{equation*}
#
# \begin{equation*}
# LAI_{t} = LAI_{t-1} + GR \cdot F_{leaves} \cdot SLA / 10000
# \tag{2.26}
# \end{equation*}
#
# Equation 2.26 can be rewritten as:
# \begin{equation*}
# LAI_{t} - LAI_{t-1} = GR \cdot F_{leaves} \cdot SLA / 10000
# \tag{2.26a}
# \end{equation*}
#
# And since $LAI_{t} - LAI_{t-1}$ is the difference in $LAI$ from one day to the next, the above is basically the same as:
# \begin{equation*}
# \frac{\mathrm{d}LAI}{\mathrm{d}t} = GR \cdot F_{leaves} \cdot SLA / 10000
# \tag{2.26b}
# \end{equation*}
#
# You have seen this in [Solution 1 from the previous page](102_variables_of_the_model.html#Solution-1), where it was stated that the equation for $LAI$ "may be considered a *difference equation* or a differential equation".
#
# However, in Equation 2.26, $GR$ is defined as the *crop growth rate (g m<sup>-2</sup> d<sup>-1</sup>)*. This variable is in fact the same as $\mathrm{d}W/\mathrm{d}t$. Equation 2.26b becomes therefore:
#
# \begin{equation*}
# \frac{\mathrm{d}LAI}{\mathrm{d}t} = \frac{\mathrm{d}W}{\mathrm{d}t} \cdot F_{leaves} \cdot SLA / 10000
# \tag{2.26c}
# \end{equation*}
#
# If you recall differentiation rules from calculus, this is equivalent to:
#
# \begin{equation*}
# \frac{\mathrm{d}LAI}{\mathrm{d}t} = \frac{\mathrm{d}W \cdot F_{leaves} \cdot SLA / 10000}{\mathrm{d}t} 
# \tag{2.26d}
# \end{equation*}
#
# We can then take the antiderivative, which gives (up to a constant):
#
# \begin{equation*}
# LAI = W \cdot F_{leaves} \cdot SLA / 10000
# \tag{2.26e}
# \end{equation*}
#
# To summarize: instead of using Equations 2.25 and 2.26 as above, we may use:
#
# \begin{equation*}
# \mathrm{d}W/\mathrm{d}t = LUE \cdot \left( 1 - e^{-k \cdot LAI} \right) \cdot I
# \tag{2.25}
# \end{equation*}
#
# \begin{equation*}
# LAI = W \cdot F_{leaves} \cdot SLA / 10000
# \tag{2.26e}
# \end{equation*}

# %% [markdown]
# ### Explaining the above in words

# %% [markdown]
# Equation 2.26 states that the rate of change in $LAI$ is equal to the rate of change of *total crop mass* $W$, multiplied by the fraction partitioned to the leaves $F_{leaves}$, multiplied by $SLA$ (and divided by 10,000 to get the right units). Considering the crop growth processes, this means that as the crop grows, a certain fraction $F_{leaves}$ goes to the leaves, and this growth in leaf mass can be translated to leaf area by using $SLA$.
#
# Rather than growth and rate of change, we can look at the state of the crop: the crop has a toal mass $W$, and $W \cdot F_{leaves}$ is the crop's *total leaf mass*, in g of dry weight per m<sup>2</sup> floor. By the same logic of Equation 2.26 (see also Equation 2.14 in pg. 34), the $LAI$ is equal to $W \cdot F_{leaves} \cdot SLA / 10000$.

# %% [markdown] editable=true slideshow={"slide_type": ""}
# ## Exercise 3: Defining the reorganized crop model in a dict

# %% [markdown] editable=true slideshow={"slide_type": ""}
# ```{exercise}
# :label: exercise-crop-definition-2
# :enumerated: true
#
# Considering the changes above, go back to the previous exercise and edit the `dict` you created. This time, use Equation 2.26e instead of Equation 2.26.
# ```

# %% editable=true slideshow={"slide_type": ""} tags=["remove-output"]
"""
Exercise 2: complete the crop definition dict using Equation 2.26e
"""

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
# ### Solution 3

# %% [markdown] editable=true slideshow={"slide_type": ""}
# ```{solution} exercise-crop-definition-1
# :label: solution-crop-definition-1
# :class: dropdown
#
# By using Equation 2.26e instead of 2.26, $LAI$ is no longer defined by a differential equation, meaning it is no longer a state. It is now calculated based on other variables, therefore it has a `type` of `"aux"`. Furthermore, the variable $GR$ is no longer used, so it is removed.
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
        "type": "aux",
        "reference": "Stanghellini (2019), Eq. 2.25"
    },
    "I": {
        "description": "Daily light sum",
        "unit": "MJ PAR per m2",
        "type": "input",
        "reference": "Stanghellini (2019), Eq. 2.25"
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
