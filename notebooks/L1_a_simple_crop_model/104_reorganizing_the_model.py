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
# # 1.4 Reorganizing the model equations

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


# %% [markdown]
# ## A look at the equations defining the crop model

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
# You have seen this in [Solution 1 in this lesson](102_variables_of_the_model.ipynb#Solution-1), where it was stated that the equation for $LAI$ "may be considered a *difference equation* or a differential equation".
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
Exercise 3: complete the crop model definition dict using Equation 2.25 and 2.26e
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
display_dict(crop_definition)

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
"""
Solution to exercise 3: a crop model definition dict using Equation 2.25 and 2.26e
"""

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
display_dict(crop_definition)
