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
# # 1.5 Defining relations between variables

# %% [markdown] editable=true slideshow={"slide_type": ""}
# ## What we've done so far

# %% [markdown] editable=true slideshow={"slide_type": ""}
# At [the end of the previous section](104_some_model_adjustments.ipynb#solution-3), we've defined the variables of our model, based on Eq. 2.25 (pg. 49) and Eq. 2.26 (pg. 50) of [the course textbook](https://doi.org/10.1163/9789004697041) (with some modifications). For each variable, we've provided:
# - A description (what the variable represents, in words)
# - Units
# - Type (`state`, `const`, `aux`, or `input`)
# - A reference
#
# The definition we've arrived at can be summarized by the following table:
#
# | Variable     | Description                                         | Unit                                       | Type      |
# | :----------- |:----------------------------------------------------|:-------------------------------------------|:----------|
# | $W$          | Crop dry mass                                       | g/m<sup>2</sup>                            | `state`   |
# | $LUE$        | Light use efficiency                                | g crop weight per MJ PAR                   | `const`   |
# | $k$          | Light extinction coefficient                        | -                                          | `const`   |
# | $LAI$        | Leaf area index                                     | m<sup>2</sup> leaf per m<sup>2</sup> floor | `aux`     |
# | $I$          | Daily light sum                                     | MJ PAR per m<sup>2</sup> per day           | `input`   |
# | $F_{leaves}$ | Fraction of crop dry mass partitioned to the leaves |  -                                         | `aux`     |
# | $SLA$        | Specific leaf area                                  | cm<sup>2</sup>/g                           | `const`   |
#
# What's missing from this table is how each variable is defined. For example, `LUE` is constant (`const`), but what is its constant value? `LAI` is defined by other variables (`aux`), but how? This is information that the model needs

# %% [markdown]
# ## Exercise 4: finding the variable definitions

# %% [markdown]
# ```{exercise}
# :label: exercise-crop-model-definitions
# :enumerated: true
#
# Considering Eq. 2.25 and 2.26e from [the previous section](104_some_model_adjustments.ipynb#A-look-at-the-equations-defining-the-crop-model), complete the **Definition** column in the table below.
#
# For `state` variables, the definition is the ordinary differential equation (ODE) defining them. For `const` variables, the definition is the value chosen as constants. Variables of type `input` don't need a definition (the values will be provided). Variables of type `aux` are defined by a mathematical expression which includes other variables.
#
# Add an **Explanation** in the last column to justify your choice. You will see that like in [Exercise 1](102_variables_of_the_model.ipynb#Exercise-1), finding and choosing a definition requires some searching and some creative choices.
#
# **Note:** in order to simplify the model at this point, it is convenient to treat $F_{leaves}$ as a constant for now. In this way, the model may represent a leafy crop such as lettuce, or a young fruiting crop which is still in the vegetative stage. A dynamically changins $F_{leaves}$ can be considered at a later stage.
# ```

# %% [markdown]
# | Variable     | Description                                         | Unit                                       | Type      | Definition | Explanation |
# | :----------- |:----------------------------------------------------|:-------------------------------------------|:----------|:-----------|:------|
# | $W$          | Crop dry mass                                       | g/m<sup>2</sup>                            | `state`   | $\mathrm{d}W/\mathrm{d}t = LUE \cdot \left( 1 - e^{-k \cdot LAI} \right) \cdot I$ | Eq. 2.25 |
# | $LUE$        | Light use efficiency                                | g crop weight per MJ PAR                   | `const`   | 4.3 | See pg. 49 of the textbook: this is a typical middle value |
# | $k$          | Light extinction coefficient                        | -                                          | `const`   | Complete here... | Complete here... |
# | $LAI$        | Leaf area index                                     | m<sup>2</sup> leaf per m<sup>2</sup> floor | `aux`     | ... | ... |
# | $I$          | Daily light sum                                     | MJ PAR per m<sup>2</sup> per day           | `input`   |  |  |
# | $F_{leaves}$ | Fraction of crop dry mass partitioned to the leaves |  -                                         | `const`     | ... | ... (we treat this variable as a constant for now) |
# | $SLA$        | Specific leaf area                                  | cm<sup>2</sup>/g                           | `const`   | ... | ... |

# %% [markdown]
# ### Some hints for Exercise 4

# %% [markdown]
# :::{admonition} Some hints for Exercise 4
# :class: note, dropdown
#
# - Regarding $k$, have a look at the textbook Section 2.2.4 for some common values
# - For $LAI$, see [the previous section of this course](04_some_model_adjustments.ipynb)
# - For $F_{leaves}$, see Section 2.2.10 of the course textbook. You may also consider a vegetative crop which has mostly leaves
# - For $SLA$, see Section 2.2.10 of the course textbook
# ::

# %% [markdown]
# ## Solution 4

# %% [markdown]
# ```{solution} exercise-crop-model-definitions
# :label: solution-crop-model-definitions
# :class: dropdown
#
# A possible choice for variable definitions and explanations may be the following:
#
# | Variable     | Description                                         | Unit                                       | Type      | Definition | Explanation |
# | :----------- |:----------------------------------------------------|:-------------------------------------------|:----------|:-----------|:------|
# | $W$          | Crop dry mass                                       | g/m<sup>2</sup>                            | `state`   | $\mathrm{d}W/\mathrm{d}t = LUE \cdot \left( 1 - e^{-k \cdot LAI} \right) \cdot I$ | Eq. 2.25 |
# | $LUE$        | Light use efficiency                                | g crop weight per MJ PAR                   | `const`   | 4.3 | See pg. 49 of the textbook: this is a typical middle value |
# | $k$          | Light extinction coefficient                        | -                                          | `const`   | 0.7 | See pg. 39:  "For many greenhouse crops, k has a value between 0.6 and 0.8" |
# | $LAI$        | Leaf area index                                     | m<sup>2</sup> leaf per m<sup>2</sup> floor | `aux`     | $ W \cdot F_{leaves} \cdot SLA / 10000 $ | See Eq. 2.26e in the previous Section |
# | $I$          | Daily light sum                                     | MJ PAR per m<sup>2</sup> per day           | `input`   |  |  |
# | $F_{leaves}$ | Fraction of crop dry mass partitioned to the leaves |  -                                         | `aux`     | 0.8 | Choice for a vegetative crop with mostly leaves |
# | $SLA$        | Specific leaf area                                  | cm<sup>2</sup>/g                           | `const`   | 250 | See Table 2.1 (pg. 50) of the textbook. 250 is a middle value for a tomato crop |
#     
# ```

# %%
