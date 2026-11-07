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
# # 1.8 Running the model in GreenLight

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
from urllib.request import urlretrieve
import greenlight

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
# ## What we have so far

# %% [markdown] editable=true slideshow={"slide_type": ""}
# At the end of the previous section, we've finished defining the simple crop model in a Python dict. Run the code block below to load this dict into the variable `crop_definition`.

# %% editable=true slideshow={"slide_type": ""} tags=["remove-output"]
"""
Solution to Exercise 6: replace the definition of the input variable I with a definition of Iw, as above
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

# %% [markdown] editable=true slideshow={"slide_type": ""}
# ## Getting input data

# %% [markdown] editable=true slideshow={"slide_type": ""}
# The crop model we've defined requires **input data**. Specifically, we've defined the **input variable `Iw`** which is the **PAR intensity above the crop**, in **W/m<sup>2</sup>**. In the following code block, we download the required input data and place it where the engine running the code blocks can access it. You can find more information about this input data [here](https://github.com/davkat1/intro_gh_modelling_draft/tree/main/notebooks/input).

# %% editable=true slideshow={"slide_type": ""} tags=["remove-output"]
"""
Download input data for the crop model from https://github.com/davkat1/intro_gh_modelling_draft/tree/main/notebooks/input/Crop_model_input_Bleiswijk_from_20091020.csv
And place it under the current working directory
"""

# Download the file from github
url = "https://raw.githubusercontent.com/davkat1/intro_gh_modelling_draft/refs/heads/main/notebooks/input/Crop_model_input_Bleiswijk_from_20091020.csv"
urlretrieve(url,"input/Crop_model_input_Bleiswijk_from_20091020.csv")

# Load the data to a DataFrame and show it
input_df = pd.read_csv("input/Crop_model_input_Bleiswijk_from_20091020.csv", header=[0, 1, 2])
display(input_df)
