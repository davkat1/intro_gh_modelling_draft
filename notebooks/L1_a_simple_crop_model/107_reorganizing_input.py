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
# # 1.7 Reorganizing the model input

# %% [markdown]
# ## Live code in this page

# %% [markdown]
# This page uses **live code**. Click the rocket button (🚀) at the top of this page, above the title, then choose "▶ Live Code". The loading may take some time so it is good to start the Live Code before reading on. The Live Code engine is ready when you see a text under the page's title, stating something like "Launching from mybinder.org: **ready**.
#
# **Note:** Code that you edit in the live code blocks is not saved. Any changes you make to the code blocks is lost once you move on from the page. Therefore, if you want to keep your work, save a copy of it in a local document.
#
# The code block below defines some imports and functions that will be helpful in the current page. It is run automatically when you run the "▶ Live Code" button. You may have a look at it if you like, but that is not neccesary for this course.

# %% editable=true slideshow={"slide_type": ""} tags=["remove-output", "hide-input", "thebe-init"]
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
# ## Some unit analysis

# %% [markdown] editable=true slideshow={"slide_type": ""}
# Before moving on, let's have another look at Equation 2.25:
#
# \begin{equation*}
# \mathrm{d}W/\mathrm{d}t = LUE \cdot \left( 1 - e^{-k \cdot LAI} \right) \cdot I
# \tag{2.25}
# \end{equation*}
#
# The unit for $\mathrm{d}W/\mathrm{d}t$ is **g per m<sup>2</sup>** per day (see [the course textbook](https://doi.org/10.1163/9789004697041), pg. 49): $$\frac{\textrm{g crop weight}}{\textrm{m}^2 \textrm{day}}$$
#
# The unit for $W$ is **g/m<sup>2</sup>**, which means that the unit for the time variable $t$ is **day**.
#
# Considering the units on the left hand side of Equation 2.25:
# - $LUE$ is in **g crop weight per MJ PAR**:
# $$
# \frac{\textrm{g crop weight}}{\textrm{MJ PAR}}
# $$
# - $LAI$ and $k$ are unitless, which means $\left( 1 - e^{-k \cdot LAI} \right)$ is unitless
# - $I$ is in **MJ PAR per m<sup>2</sup> per day**:
# $$
# \frac{\textrm{MJ PAR}}{\textrm{m}^2 \textrm{day}}
# $$
#
# The units for Equation 2.25 are therefore:
# $$
# \frac{\textrm{g crop weight}}{\textrm{m}^2 \textrm{day}} = \frac{\textrm{g crop weight}}{\textrm{MJ PAR}} \cdot \textrm{(unitless)} \cdot \frac{\textrm{MJ PAR}}{\textrm{m}^2 \textrm{day}}
# $$

# %% [markdown]
# ## Why this is inconvenient

# %% [markdown]
# There are several reasons why the choice of units above is inconvenient:
#
# 1. In [GreenLight](https://github.com/davkat1/greenlight), the time unit is always **second**, and not **day**. That fact alone means that some  modifications are needed.
# 2. Using a **daily** value for PAR radiation means that we can only use the model in cases where we know in advance how much radiation is received in a day. We cannot use the model for live calculations based on real-time measurements, since the daily PAR sum is only known at the end of the day.
# 3. It is difficult to integrate such a crop model with a greenhouse model, which is one of our goals. The greenhouse climate can change very fast, so a time unit of seconds is a reasonable choice. It is useful to have the same time unit for all model components.
# 4. Typical weather data records solar radiation in **W/m<sup>2</sup>**. It is sensible to use units that are comparable to the type of data we may come across

# %% [markdown]
# ### Changing the unit of the input

# %% [markdown] editable=true slideshow={"slide_type": ""}
# Instead of $I$, which is in **MJ PAR per m<sup>2</sup> per day**, we may use $I_W$, which is in **J PAR per m<sup>2</sup> per second**. 
#
# Since **J per second** (joule per second) is the same as **W** (watt), the unit of $I_W$ is in fact **W PAR per m<sup>2</sup>**. 
#
# If $I_W$ is in **W PAR per m<sup>2</sup> = J PAR per m<sup>2</sup> per second**, then $1/1,000,000\cdot I_W$ is in **MW PAR per m<sup>2</sup> = MJ PAR per m<sup>2</sup> per second**. 
#
# We can therefore have the following unit breakdown:
#
# \begin{equation*}
# \mathrm{d}W/\mathrm{d}t_s = LUE \cdot \left( 1 - e^{-k \cdot LAI} \right) \cdot \left( \frac{1}{1000000} \cdot I_W \right)  
# \tag{2.25a}
# \end{equation*}
#
# with the units:
# $$
# \frac{\textrm{g crop weight}}{\textrm{m}^2 \textrm{s}} = \frac{\textrm{g crop weight}}{\textrm{MJ PAR}}  \cdot \textrm{(unitless)} \cdot \frac{\textrm{MJ PAR}}{\textrm{m}^2 \textrm{s}}
# $$
#
# In the above: 
# - We've replaced $t$ (which is in **days**) with $t_s$ (which is in **seconds**)
# - And we've replaced $I$ (which is in **MJ PAR per m<sup>2</sup> per day**) with $\frac{1}{1000000} \cdot I_W$ (which is in **MJ PAR per m<sup>2</sup> per second = **MW PAR per m<sup>2</sup>**
#
# This means that instead of the input variable $I$, which is in **MJ PAR per m<sup>2</sup> per day**, we now have an input variable $I_W$, which is in **W PAR per m<sup>2</sup>**

# %% [markdown] editable=true slideshow={"slide_type": ""}
# ## Exercise 6: Adjusting the input unit

# %% [markdown] editable=true slideshow={"slide_type": ""}
# ```{exercise}
# :label: exercise-crop-model-adjust-input
# :enumerated: true
#
# Adjust the crop model definition from [section 106](106_defining_the_model_in_greenlight.html#solution-5), replacing the input variable `I` with an input variable `Iw`, as above
# ```

# %% editable=true slideshow={"slide_type": ""} tags=["remove-output"]
"""
Exercise 6: replace the definition of the input variable I with a definition of I_W, as above
"""

crop_definition = {
    "W": {
        "description": "Crop dry mass",
        "unit": "g/m2",
        "type": "state",
        "reference": "Stanghellini (2019), Eq. 2.25",
        "definition": "LUE * ( 1 - exp(-k*LAI) ) * I",  
        "init": "75"  
    },
    "LUE": {
        "description": "Light use efficiency",
        "unit": "g crop weight per MJ PAR",
        "type": "const",
        "reference": "Stanghellini (2019), Eq. 2.25",
        "definition": "4.3"  
    },
    "k": {
        "description": "Light extinction coefficient",
        "unit": "-",
        "type": "const",
        "reference": "Stanghellini (2019), Eq. 2.25",
        "definition": "0.7"  
    },
    "LAI": {
        "description": "Leaf area index",
        "unit": "m2 leaf per m2 floor",
        "type": "aux",
        "reference": "Stanghellini (2019), Eq. 2.25",
        "definition": "W * fLeaves * SLA / 10000"  
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
        "definition": "0.8" 
    },
    "SLA": {
        "description": "Specific leaf area",
        "unit": "cm2/g",
        "type": "const",
        "reference": "Stanghellini (2019), Eq. 2.26",
        "definition": "250"  
    }   
 }

# Display the above dict
display_dict(crop_definition)

# %% [markdown] editable=true slideshow={"slide_type": ""}
# ### Solution 6

# %% [markdown] editable=true slideshow={"slide_type": ""}
# ```{solution} exercise-crop-model-adjust-input
# :label: solution-crop-model-adjust-input
# ```

# %% editable=true slideshow={"slide_type": ""} tags=["hide-input", "remove-output"]
"""
Exercise 6: replace the definition of the input variable I with a definition of Iw, as above
"""

crop_definition = {
    "W": {
        "description": "Crop dry mass",
        "unit": "g/m2",
        "type": "state",
        "reference": "Stanghellini (2019), Eq. 2.25",
        "definition": "LUE * ( 1 - exp(-k*LAI) ) * 1/1000000 * Iw",  # I is replaced by 1/1000000 * Iw
        "init": "75"  
    },
    "LUE": {
        "description": "Light use efficiency",
        "unit": "g crop weight per MJ PAR",
        "type": "const",
        "reference": "Stanghellini (2019), Eq. 2.25",
        "definition": "4.3"  
    },
    "k": {
        "description": "Light extinction coefficient",
        "unit": "-",
        "type": "const",
        "reference": "Stanghellini (2019), Eq. 2.25",
        "definition": "0.7"  
    },
    "LAI": {
        "description": "Leaf area index",
        "unit": "m2 leaf per m2 floor",
        "type": "aux",
        "reference": "Stanghellini (2019), Eq. 2.25",
        "definition": "W * fLeaves * SLA / 10000"  
    },
    "Iw": {  # I is replaced by Iw
        "description": "PAR intensity",  # This variable is instanenous, rather than daily, values
        "unit": "W PAR per m2",  # The unit is now W PAR per m2
        "type": "input",
        "reference": "Stanghellini (2019), Eq. 2.25, adjusting I (in MJ/m2/day) to Iw (in W/m2)"  # Add information in reference
    },
    "fLeaves": {
        "description": "Fraction of crop dry mass partitioned to the leaves",
        "unit": "-",
        "type": "const",
        "reference": "Stanghellini (2019), Eq. 2.26",
        "definition": "0.8" 
    },
    "SLA": {
        "description": "Specific leaf area",
        "unit": "cm2/g",
        "type": "const",
        "reference": "Stanghellini (2019), Eq. 2.26",
        "definition": "250"  
    }   
 }

# Display the above dict
display_dict(crop_definition)

# %% editable=true slideshow={"slide_type": ""}
