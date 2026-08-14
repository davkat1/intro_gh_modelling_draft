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
# # 2. Interactive greenhouse "tunnel" model

# %% [markdown]
# ![Tunnel image by Richard Webb](../Figures/geograph-4408046-by-Richard-Webb.jpg)<br>
# **Figure 2.1.** A tunnel greenhouse.<br>
# Image copyright Richard Webb, CC BY-SA 2.0, https://www.geograph.org.uk/reuse.php?id=4408046

# %% [markdown]
# ## 2.1 In this lesson

# %% [markdown]
# In this lesson, you will be implementing the greenhouse "tunnel" model described in Chapter 3 of [the course textbook](https://doi.org/10.1163/9789004697041). You will create an **interactive model with sliders**, where users can choose values for various model parameters and inputs, and see how those values influence the model result.

# %% [markdown]
# ### 2.1.2 What you'll learn

# %% [markdown]
# By the end of this lesson, you will be able to:
# - Implement your own model: from a text description in a book to an interactive tool
# - Analyze the textbook's tunnel model, pointing out which parameters and inputs influence the model result, and to what extent
# - Expand an existing model and add new components to it

# %% [markdown]
# ## 2.2 The greenhouse "tunnel" model

# %% [markdown]
# Section 3.4 (pp. 69-71) of [the course textbook](https://doi.org/10.1163/9789004697041) describes a simplified greenhouse: without ventilation, without a crop, and with the cover temperature equal to the indoor air temperature. This is a theoretical greenhouse, since almost all greenhouses will have at least some ventilation, and the cover temperature is often different from the air temperature. The textbook chooses to call this theoretical greenhouse a "tunnel", where the authors most likely have something like [Figure 2.1](#2.-Interactive-greenhouse-"tunnel"-model) in mind. Nevertheless, [tunnel greenhouses](https://en.wikipedia.org/wiki/Polytunnel) (also called polytunnels or hoophouses), often do have controllable ventilation, like for instance in [this image](../Figures/Interior_of_a_Hoop_House_on_the_Farm_at_Saint_Joe's,_Superior_Township,_Michigan.JPG) ([Image](https://commons.wikimedia.org/wiki/File:Interior_of_a_Hoop_House_on_the_Farm_at_Saint_Joe%27s,_Superior_Township,_Michigan.JPG) copyright Dwight Burdette, CC BY 3.0). 
#
# See also Section 1.2 (pp. 19-21) of the course textbook.

# %% [markdown]
# ### 2.2.1 Exercise: background reading

# %% [markdown]
# As prearation for this lesson, read Chapter 3 (pp. 54-73) of [the course textbook](https://doi.org/10.1163/9789004697041). This will provide theoretical background on all the various components of the "tunnel" model, which you will implement in this lesson

# %% [markdown]
# ## 2.3 Creating an interactive model: defining the variables

# %% [markdown]
# ### 2.3.1 Defining the tunnel model variables

# %% [markdown]
# In order to create an interactive model, we will take the following steps:
# 1. We will create a [Python dictionary](https://docs.python.org/3/tutorial/datastructures.html#dictionaries) (`dict`) that defines the model variables, as described in the textbook after **Equation 3.9** (pg. 70). We will call this dictionary `model_vars`
# 2. `model_vars` will be defined as a dictionary of dictionaries: each variable will be an entry in the dictionary `model_vars`, with the *key* as the variable name, and the *value* as a dictionary
# 3. The *values* of `model_vars` will include the available information we have about each of the variables in our model, specifically:
#     - **Description:** a description about what the variable is
#     - **Reference:** a reference to the place in the textbook where the variable is described
#     - **Value:** a starting value for the variable in the interactive model
#     - **Unit:** the unit in which the variable is expressed
#     - **Min:** a minimum value for the variable in the interactive model
#     - **Max:** a maximum value for the variable in the interactive model
#     - **Step:** the step size which the interactive model will allow for the variable

# %% [markdown]
# ### 2.3.2 Example: some tunnel model variables

# %% [markdown]
# In the code block below we start defining `model_vars`, following the text after **Equation 3.9** in the textbook. We define: 
# - **𝜏** (Greek letter tau), which we write in code as `tau`
# - $I_{sun}$ , which we write in code as `iSun`
# - $F_{tunnel,sky}$ , which we write in code as `fTunnelSky`
#
# Where:
# - The **description** is taken directly from the text under Eq. 3.9
# - The **unit** is also taken directly from the text under Eq. 3.9
# - The **reference** inidcates where the variable is describe. The text under Eq. 3.9 usually provides a good indication, but if more information was used (for example, for choosing the value for the variable), it is also included
# - The **value** is an estimate or example for a reasonable value. For example, for **𝜏**, Table 3.1 in the textbook gives an indication
# - The **min** and **max** are a choice of a reasonable or interesting range of values to consider for the variable. The interactive model we will create will allow changing the variable with values between **min** and **max**. Therefore, the exact choice here is not very important, as long as it gives values that are interesting to test later
# - **step** is a choice of a reasonable step size that the model will allow. For example, a value of 5 and a step size of 0.1, means value like 4.9 and 5.1 will be used, but not 4.91 and 5.11.

# %%
""" 
Example 2.3.2
Define tunnel model variables to be used in sliders 
"""
model_vars = {
    "tau": {
        "description": "Transmissivity (hemispherical) of the cover for sun radiation",
        "unit": "-",
        "reference": "Stanghellini et al. (2024), Eq. 3.2 & Table 3.1",
        "value": 0.8,
        "min": 0,
        "max": 1,
        "step": 0.01
    },
    "iSun": {
        "name": "iSun",
        "description": "Solar radiation",
        "unit": "W/m2",
        "reference": "Stanghellini et al. (2024), Eq. 3.2",
        "value": 700,
        "min": 0,
        "max": 1500,
        "step": 10
    },
    "fTunnelSky": {
        "description": "View factor between tunnel and sky",
        "unit": "-",
        "reference": "Stanghellini et al. (2024), Eq. 3.5 & pg. 70",
        "value": 0.5,
        "min": 0,
        "max": 1,
        "step": 0.01
    }
}

# %% [markdown]
# #### 2.3.2.1 Why are we doing this?

# %% [markdown]
# You might ask, why are we including so much information in our model definition, including a description, unit, and a reference? The reason is that we want to create model components (which can, for example, eventually become publishable shared files) that are as complete as possible. You will see in the following sections how a model (like the one described in the textbook) often contains many implicit choices. We want, as much as possible, to make these choices explicit, so that future users (including our future selves) will be able to understand why choices were made, so that any modification or extension will also be based on informed reasoning.

# %% [markdown]
# #### 2.3.2.2 A note about notation

# %% [markdown]
# As we are in the process of taking a model that is described in a book and implementing it in code, it is clear that certain notations that are useful in printed text are not so easy to use in code. For example, it is [not recommended](https://peps.python.org/pep-0008/#source-file-encoding) to use symbols such as the Greek letter 𝜏 in Python variable names. There is also no standard way to include subscripts ($I_{sun}$), superscripts ($I^{sun}$), or commas ($F_{a,b}$) in Python variable names.
#
# Therefore, we must choose a (preferably consistent) method to convert $printed$ variable names to variable names `in_code`. We use the following conventions:
# - Variable names are written using [`mixedCase`](https://peps.python.org/pep-0008/#descriptive-naming-styles)
# - A subscript, superscript, or comma is considered as a word separator
# - Greek letters are written out in full
#
# **Examples:**
# - $\tau$ -> `tau`
# - $I_{sun}$ -> `iSun`
# - $F_{tunnel,sky}$ -> `fTunnelSky`
# - $\varepsilon_{cover}$ -> `epsilonCover`

# %% [markdown]
# ### 2.3.3 Exercise: completing the tunnel model variables
#
# In the following code block, complete the definition of `model_vars` as above, to include all variables described in Equation 3.9.
#
# **Be sure to check that you have defined *all* the variables of Equation 3.9!**

# %%
""" 
Exercise 2.3.3
Define tunnel model variables to be used in sliders 
Complete this code block 
"""
model_vars = {
    "tau": {
        "description": "Transmissivity (hemispherical) of the cover for sun radiation",
        "unit": "-",
        "reference": "Stanghellini et al. (2024), Eq. 3.2 & Table 3.1",
        "value": 0.8,
        "min": 0,
        "max": 1,
        "step": 0.01
    },
    "iSun": {
        "name": "iSun",
        "description": "Solar radiation",
        "unit": "W/m2",
        "reference": "Stanghellini et al. (2024), Eq. 3.2",
        "value": 700,
        "min": 0,
        "max": 1500,
        "step": 10
    },
    "fTunnelSky": {
        "description": "View factor between tunnel and sky",
        "unit": "-",
        "reference": "Stanghellini et al. (2024), Eq. 3.5 & pg. 70",
        "value": 0.5,
        "min": 0,
        "max": 1,
        "step": 0.01
    },
    "Continue here...": ""
}

# %% [markdown]
# ### 2.3.4 Some hints to help with Exercise 2.3.3

# %% [markdown]
# Use the following blocks to help you in the process of completing Exercise 2.3.3. You may, of course, choose to first struggle on your own, but the following can give some direction in case you are lost.

# %% [markdown]
# #### 2.3.4.1 $\varepsilon_{cover}$ (`epsilonCover`) and $\varepsilon_{soil}$ (`epsilonSoil`)

# %% [markdown]
# The text under Equation 3.9 leads you to Equation 3.3, but that is not very helpful in determining a value for these variables. Check Section 3.2.1 of the textbook for the ranges of values for emissivity, and the emissivity of "most materials". You may search online for typical emissivity values for various materials. If you're unsure, consider that many materials in the greenhouse are often wet (due to irrigation or condensation).
#
# Note that $\varepsilon_{soil}$ is not included in the list below Equation 3.9. This is variable represents the emissivity of the soil.

# %% [markdown]
# #### 2.3.4.2 $\alpha_{R}$ (`alphaR`)

# %% [markdown]
# In the textbook, under Equation 3.6, we read that "a very first rule of thumb is that the net radiation energy exchanged between two things at 'terrestrial' temperatures is about 6 W/m2 for each degree difference in temperature". This quote refers to a reasonable estimate for $\alpha_R$

# %% [markdown]
# #### 2.3.4.3 $A_{cover}$ (`aCover`) and $A_{soil}$ (`aSoil`)

# %% [markdown]
# The explanations under Equation 3.7 in the textbook are somewhat lacking. $A_{soil}$, "the surface of the soil" (m<sup>2</sup>), represents the land area of the greenhouse. $A_{cover}$, "the surface of the cover" (m<sup>2</sup>), is the surface area of the cover, i.e., the area of the roof and side walls of a greenhouse. Thus, for a greenhouse with a land area of 1 ha, $A_{soil}$ would be $10000$ $\textrm{m}^2$. The value of $A_{cover}$ would be larger, as it includes the 10000 m<sup>2</sup> of roof above the greenhouse, plus more area of the side walls. The roof area itself can also be larger than the land area, for example in the typical [Venlo-type greenhouse](../Figures/Greenhouses_in_Bemmel,_Lingewaard.jpg) ([Image](https://commons.wikimedia.org/wiki/File:Greenhouses_in_Bemmel,_Lingewaard.jpg) in the public domain). 
#
# Note that in Equation 3.9, $A_{cover}$ and $A_{soil}$ always appear as a ratio. Therefore, it could be simpler to lump these two variables into one, for instance `aCoverOverSoil`. The unit of this lumped variable is m<sup>2</sup> cover per m<sup>2</sup> soil, which is equivalent to a unitless variable. A reasonable value for this variable is 1.2, and it cannot be below 1. 

# %% [markdown]
# #### 2.3.4.4 $\alpha_{cover}$ (`alphaCover`) and $\alpha_{soil}$ (`alphaSoil`)

# %% [markdown]
# The textbook gives very little information on these variable after Equations 3.7 and 3.8. It mentions that $\alpha_{cover}$ depends on wind, and that it is somehow related to the U coefficient (Section 8.1.1 in the textbook). However, it points out that the U coefficient accounts for "both heat" (presumably, convective and conductive), "and thermal radiation losses", while $\alpha_{cover}$ likely does not include thermal radiation losses, since those depend on $T_{sky}$ and not $T_{out}$. The textbook also warns: "The U coefficient is an average overall heat transfer coefficient, and should not be used for calculating the temperature in the greenhouse at a given time". Nevertheless, we currently want to construct a rather general model, so average values are fine for our purposes.
#
# A look at Section 8.1.1 (pp. 167-168) of the textbook shows that the U coefficient may have values such as 9.26 or 6.83 W m<sup>-2</sup> K<sup>-1</sup>. The U coefficient includes radiative, conductive, and convective transfers, while $\alpha_{cover}$ includes only conductive and convective transfers. Therefore, $\alpha_{cover}$ may be in the range of 3-5 W m<sup>-2</sup> K<sup>-1</sup>. 
#
# Since there is little information about $\alpha_{soil}$, we may assume it takes values in a similar range as $\alpha_{cover}$. For the sake of our interactive model, we may consider larger ranges, say, 0-10 W m<sup>-2</sup> K<sup>-1</sup>

# %% [markdown]
# #### 2.3.4.5 $F_{tunnel,sky}$ (`fTunnelSky`) and $F_{tunnel,soil}$ (`fTunnelSoil`)

# %% [markdown]
# As explained in Section 3.2.2 of the textbook, the view factor is a fraction, with a value between 0 and 1. The text below Equation 3.9 states directly that the values for $F_{tunnel,sky}$ and $F_{tunnel,soil}$ are both 0.5. As explained in Section 3.2.2, the sum of all view factors for one point (in this case, the tunnel) must be 1. A choice of $F_{tunnel,sky} = F_{tunnel,soil} = 0.5$ fits with this concept.
#
# However, the choice above depends on what we precisely mean by "the tunnel" here. Air emits very little thermal radiation, so it is actually the cover of the greenhouse which should probably be considered. If that is the case, one could say that the radiation towards the sky is coming from "the external side of the cover", and radiation towards the soil is coming from "the internal side of the cover". Seeing it this way, one may choose $F_{tunnel,sky} = F_{tunnel,soil} = 1$.
#
# A different reasoning could say that for each m<sup>2</sup> of soil, there are actually 2 m<sup>2</sup> of cover that is exchanging solar radiation - the outer (top) side of the cover, and the inner (bottom) side of the cover. In this case, the view factor is still 0.5, but it should be multiplied by a factor 2. In effect, this fits with considering the view factors as having values of $F_{tunnel,sky} = F_{tunnel,soil} = 1$.
#
# The above is an interesting discussion, but the most important question is **what is the influence of the choice above on the model results?** Since we are building an interactive model, we can allow the view factors to vary between 0.5 (or even 0) and 1, and see how that influences the model.

# %% [markdown]
# #### 2.3.4.5 $T_{out}$ (`tOut`), $T_{sky}$ (`tSky`), $T_{soil}$ (`tSoil`), and $T_{tunnel}$ (`tTunnel`)

# %% [markdown]
# The choice for $T_{out}$ can be based on your local climate: any range of outdoor air temperatures you may experience can be reasonable here. 
#
# For $T_{sky}$ you may use the text on pg. 67 of the textbook, which states "On a clear, cold night there can easily be a difference of 50 °C between a greenhouse and the upper layers of the atmosphere". Based on this, one can also allow $T_{sky}$ to be 50 °C coulder than the outdoor air.
#
# For $T_{soil}$ the textbook on pg. 68 states that the soil "is usually colder than the greenhouse air during the day and warmer at night". Thus, assuming that the greenhouse air can be about 20 °C warmer than the outdoor air during the day, and about 10 °C colder than the outdoor air at night, the soil temperature may be anywehere between 10 °C less and 20 °C more than the outdoor air temperature.
#
# As for $T_{tunnel}$, the interactive model we will construct will display $T_{tunnel}$ as the result, depending on the other variables. Therefore, the  choice of values for $T_{tunnel}$ are not so important. However, based on the previous paragraph, a range which goes about 10 °C lower and 20 °C higher than the range for the outdoor temperatures would be a reasonable choice.

# %% [markdown]
# ### 2.3.5 Complete solution for Exercise 2.3.3

# %% [markdown]
# The following code block is a possible solution to **Exercise 2.3.3**:

# %%
""" 
Solution for Exercise 2.3.3
Define tunnel model variables to be used in sliders 
"""
model_vars = {
    "tau": {
        "description": "Transmissivity (hemispherical) of the cover for sun radiation",
        "unit": "-",
        "reference": "Stanghellini et al. (2024), Eq. 3.2 & Table 3.1",
        "value": 0.8,
        "min": 0,
        "max": 1,
        "step": 0.01
    },
    "iSun": {
        "name": "iSun",
        "description": "Solar radiation",
        "unit": "W/m2",
        "reference": "Stanghellini et al. (2024), Eq. 3.2",
        "value": 700,
        "min": 0,
        "max": 1500,
        "step": 10
    },
    "fTunnelSky": {
        "description": "View factor between tunnel and sky",
        "unit": "-",
        "reference": "Stanghellini et al. (2024), Eq. 3.5 & pg. 70",
        "value": 0.5,
        "min": 0,
        "max": 1,
        "step": 0.01
    },
    "epsilonCover": {
        "description": "Emissivity of the cover, including effect of screen(s)",
        "unit": "-",
        "reference": "Stanghellini et al. (2024), Eq. 3.3 & Section 3.2.1",
        "value": 1,
        "min": 0,
        "max": 1,
        "step": 0.01
    },
    "alphaR": {
        "description": "Apparent transfer coefficient for thermal radiation",
        "unit": "-",
        "reference": "Stanghellini et al. (2024), Eq. 3.6 & paragraph following",
        "value": 6,
        "min": 4,
        "max": 10,
        "step": 0.1
    },
    "tTunnel": {
        "description": "Temperature of the unventilated greenhouse",
        "unit": "°C",
        "reference": "Stanghellini et al. (2024), Eq. 3.9",
        "value": 25,
        "min": -50,
        "max": 50,
        "step": 1
    },
    "tSky": {
        "description": "Apparent temperature of the sky (depends, among other things, on cloudiness)",
        "unit": "°C",
        "reference": "Stanghellini et al. (2024), Eq. 3.9",
        "value": 0,
        "min": -50,
        "max": 50,
        "step": 1
    },
    "tOut": {
        "description": "Temperature of the air outside the greenhouse",
        "unit": "°C",
        "reference": "Stanghellini et al. (2024), Eq. 3.9",
        "value": 30,
        "min": -50,
        "max": 50,
        "step": 1
    },
    "tSoil": {
        "description": "Temperature of the soil surface",
        "unit": "°C",
        "reference": "Stanghellini et al. (2024), Eq. 3.9",
        "value": 35,
        "min": -50,
        "max": 50,
        "step": 1
    },
    "fTunnelSoil": {
        "description": "View factor between tunnel and soil",
        "unit": "-",
        "reference": "Stanghellini et al. (2024), Eq. 3.5 & pg. 70",
        "value": 0.5,
        "min": 0,
        "max": 1,
        "step": 0.01
    },
    "epsilonSoil": {
        "description": "Emissivity of the soil, including possible effect of mulch",
        "unit": "-",
        "reference": "Stanghellini et al. (2024), Eq. 3.3 & Section 3.2.1",
        "value": 1,
        "min": 0,
        "max": 1,
        "step": 0.01
    },
    "aCoverOverSoil": {
        "description": "Surface area of cover per unit surface area of soil",
        "unit": "-",
        "reference": "Stanghellini et al. (2024), Eq. 3.7. This variable is used to represent aCover divided by aSoil",
        "value": 1.2,
        "min": 0,
        "max": 5,
        "step": 0.1
    },
    "alphaCover": {
        "description": "Heat transfer coefficient of the cover material (including possible screens)",
        "unit": "W/m2/K",
        "reference": "Stanghellini et al. (2024), Eq. 3.7",
        "value": 4,
        "min": 0,
        "max": 10,
        "step": 0.1
    },
    "alphaSoil": {
        "description": "Heat transfer coefficient of the soil (including possible mulches)",
        "unit": "W/m2/K",
        "reference": "Stanghellini et al. (2024), Eq. 3.68",
        "value": 4,
        "min": 0,
        "max": 20,
        "step": 0.1
    }
}

# %% [markdown]
# ### 2.3.6 Reflection: defining the tunnel model variables

# %% [markdown]
# Before moving forward, stop to reflect on the following questions:
# - How was the experience of converting the equation from a textbook to code?
# - Were all variables clearly defined in the textbook?
# - Was it easy to choose representative values and ranges?
# - Did you need to check the provided solution to fill in values?
# - Do you agree with the choices made in the provided solution?

# %% [markdown]
# #### 2.3.6.1 Some notes on defining the tunnel model variables

# %% [markdown]
# You may have noticed the following:
# - It is not easy to find "reasonable" values, or ranges of values, for each variable. This typically requires some very careful reading, or consultation with an expert
# - Some notational choices in the textbook can be quite confusing, for example the unit "K or °C" is slightly ambiguous
# - In the list of variables under Equation 3.9, the text $F_{a,b}$ means that $a$ and $b$ can be replaced by other names, e.g., $F_{tunnel,soil}$. However, the text $A_{cover,soil}$ seems to mean something else, and in fact, it should more appropriately read $A_{cover},$ $A_{soil}$
# - 

# %% [markdown]
# ## 2.4 Creating an interactive model: defining the calculation of $T_{tunnel}$

# %% [markdown]
# Until now, we have defined the various variables included in the greenhouse tunnel model: for each variable we've set a name, description, unit, initial value, range, and step size. We have not yet described the relationship between all those variables.
#
# In the interactive model that we will create, our goal will be to show how the temperature of the tunnel, `tTunnel`, is influenced by all the other variables. For this, we must first figure out how this influence is defined in the model. 
#
# **Equation 3.9** in the course textbook defines a relation between ingoing and outgoing energy fluxes in the tunnel greenhouse. **Equation 3.10** is a restructuring of **Equation 3.9**, which describes the difference between the tunnel temperature and the outdoor temperature. Unfortunately, none of these equations provide a straightforward description of how $T_{tunnel}$ is influenced by other factors. For this, some algebra is needed.

# %% [markdown]
# ### 2.4.1 Exercise: algebraically solving for $T_{tunnel}$
#
# This is an exercise in algebra:
#
# **Solve Equation 3.9 for $T_{tunnel}$.** 
#
# In other words, rearrange Equation 3.9 so that $T_{tunnel}$ is isolated.
#
# If you're unfamiliar (or out of practice) with solving equations in algebra, then an elementary algebra course or primer might help, such as OpenStax's [Elementary Algebra 2e](https://openstax.org/details/books/elementary-algebra-2e).

# %% [markdown]
# #### 2.4.1 Solution

# %% [markdown]
# We start with Equation 3.9:
#
# $$
# \begin{align}
# \tau I_{sun} &= F_{tunnel,sky} \varepsilon_{cover} \alpha_R \left( T_{tunnel} - T_{sky} \right) + \frac{A_{cover}}{A_{soil}} \alpha_{cover} \left( T_{tunnel} - T_{out} \right)\\
# &+F_{tunnel,soil} \varepsilon_{soil} \alpha_R \left( T_{tunnel} - T_{soil} \right) +\alpha_{soil} \left( T_{tunnel} - T_{soil} \right)\\
# \end{align}
# $$
#
# Expand the brackets:
#
# $$
# \begin{align}
# \tau I_{sun} &= F_{tunnel,sky} \varepsilon_{cover} \alpha_R T_{tunnel} - F_{tunnel,sky} \varepsilon_{cover} \alpha_R T_{sky} + \frac{A_{cover}}{A_{soil}} \alpha_{cover} T_{tunnel} - \frac{A_{cover}}{A_{soil}} \alpha_{cover} T_{out} \\
# &+F_{tunnel,soil} \varepsilon_{soil} \alpha_R T_{tunnel} - F_{tunnel,soil} \varepsilon_{soil} \alpha_R T_{soil} +\alpha_{soil} T_{tunnel} - \alpha_{soil} T_{soil} \\
# \end{align}
# $$
#
# Consolidate the coefficients of $T_{tunnel}$ :
#
# $$
# \begin{align}
# \tau I_{sun} &= T_{tunnel} \left( F_{tunnel,sky} \varepsilon_{cover} \alpha_R  + \frac{A_{cover}}{A_{soil}} \alpha_{cover} + F_{tunnel,soil} \varepsilon_{soil} \alpha_R +\alpha_{soil} \right) \\
# & - F_{tunnel,sky} \varepsilon_{cover} \alpha_R T_{sky} - \frac{A_{cover}}{A_{soil}} \alpha_{cover} T_{out} - F_{tunnel,soil} \varepsilon_{soil} \alpha_R T_{soil}  - \alpha_{soil} T_{soil} \\
# \end{align}
# $$
#
# Rearrange to isolate the term with $T_{tunnel}$ :
#
# $$
# \begin{align}
# \tau I_{sun} + F_{tunnel,sky} \varepsilon_{cover} \alpha_R T_{sky} + \frac{A_{cover}}{A_{soil}} \alpha_{cover} T_{out} + F_{tunnel,soil} \varepsilon_{soil} \alpha_R T_{soil}  + \alpha_{soil} T_{soil} \\
# = T_{tunnel} \left( F_{tunnel,sky} \varepsilon_{cover} \alpha_R  + \frac{A_{cover}}{A_{soil}} \alpha_{cover} + F_{tunnel,soil} \varepsilon_{soil} \alpha_R +\alpha_{soil} \right) \\
# \end{align}
# $$
#
# Finally, isolating $T_{tunnel}$ :
#
# $$
# \begin{align}
# T_{tunnel} = &\\
# &\frac{ \tau I_{sun} + F_{tunnel,sky} \varepsilon_{cover} \alpha_R T_{sky} + \frac{A_{cover}}{A_{soil}} \alpha_{cover} T_{out} + F_{tunnel,soil} \varepsilon_{soil} \alpha_R T_{soil}  + \alpha_{soil} T_{soil}}{F_{tunnel,sky} \varepsilon_{cover} \alpha_R  + \frac{A_{cover}}{A_{soil}} \alpha_{cover} + F_{tunnel,soil} \varepsilon_{soil} \alpha_R +\alpha_{soil}}
# \end{align}
# $$

# %% [markdown]
# ## 2.5 Setting up the interactive model

# %% [markdown]
# This section converts the model variables that we've defined until now into an interactive model, where the influence of each variable on the output `tTunnel` will be immediately seen. The bulk of the content below is an implementation in Python of the interactive sliders, using [Jupyter Widgets](https://ipywidgets.readthedocs.io/) and [IPython](https://ipython.readthedocs.io/). 
#
# Since our focus is on the model itself and not so much the implementation, most of the code below can be simply run, but there is no need to analyze it deeply. Some exercises will help guide you to focus on what is relevant for our purposes.

# %% [markdown]
# ### 2.5.1 Imports

# %% [markdown]
# The following code block imports packages and modules that are used in the following code blocks.

# %%
""" 
Imports needed for running the following code
"""
import ipywidgets as widgets
from IPython.display import display, Math, HTML


# %% [markdown]
# ### 2.5.2 Defining the calculation of `tTunnel`

# %% [markdown]
# The code below defines the calculation of `tTunnel`, as a function of all other model variables.

# %%
""" 
Define the calculation of tTunnel
"""
def calc_tTunnel(tau, iSun, fTunnelSky, epsilonCover, alphaR, 
            tSky, tOut, tSoil, fTunnelSoil, epsilonSoil, aCoverOverSoil, 
            alphaCover, alphaSoil):
    tTunnel = ( 
            tau * iSun 
            + fTunnelSky * epsilonCover * alphaR * tSky 
            + aCoverOverSoil * alphaCover * tOut 
            + tSoil * (fTunnelSoil * epsilonSoil * alphaR + alphaSoil)
        ) / (
            fTunnelSky * epsilonCover * alphaR 
            + aCoverOverSoil * alphaCover 
            + fTunnelSoil * epsilonSoil * alphaR 
            + alphaSoil
        )
    return tTunnel


# %% [markdown]
# ### 2.5.3 Exercise: calculation of `tTunnel`

# %% [markdown]
# Confirm that the definition of `tTunnel` above matches the calculation of $T_{tunnel}$ that was defined in [Section 2.4](#2.4-Creating-an-interactive-model:-defining-the-calculation-of-$T_{tunnel}$).

# %% [markdown]
# ### 2.5.4 Setting up the interactive model

# %% [markdown]
# The code below uses [Jupyter Widgets](https://ipywidgets.readthedocs.io/) and [IPython](https://ipython.readthedocs.io/) to create an interactive model which displays how `tTunnel` is influenced by the other variables. Run the code, but the details may be skipped.

# %%
""" 
Set up the interactive model
"""

# Create header row, showing the titles:
# "Variable", "Value", "Unit", "Description",
#   and "Reference"
header = widgets.HBox([
    widgets.HTML(
        "<b>Variable</b>",
        layout=widgets.Layout(width="150px")
    ),
    widgets.HTML(
        "<b>Value</b>",
        layout=widgets.Layout(width="300px")
    ),
    widgets.HTML(
        "<b>Unit</b>",
        layout=widgets.Layout(width="100px")
    ),
    widgets.HTML(
        "<b>Description</b>",
        layout=widgets.Layout(width="250px")
    ),
    widgets.HTML(
        "<b>Reference</b>",
        layout=widgets.Layout(width="200px")
    )
])


# Create variable rows. For each variable,
# display the variable name, a slider to
# select the value, then the unit, description,
# and reference
# Note that the code below uses the dictionary
# model_vars, which was defined earlier in this 
sliders = {}
rows = []
for name, var in model_vars.items():
    slider = widgets.FloatSlider(
        value=var["value"],
        min=var["min"],
        max=var["max"],
        step=var["step"],
        continuous_update=True,
        layout=widgets.Layout(width="300px")
    )

    sliders[name] = slider

    row = widgets.HBox([
        widgets.HTML(
            f"<code><b>{name}</b></code>",
            layout=widgets.Layout(width="150px")
        ),
        slider,
        widgets.HTML(
            var["unit"],
            layout=widgets.Layout(width="100px")
        ),
        widgets.HTML(
            var["description"],
            layout=widgets.Layout(width="250px")
        ),
        widgets.HTML(
            f"<i>{var['reference']}</i>",
            layout=widgets.Layout(width="200px")
        )
    ])

    # Do not make a slider for tTunnel
    if name != "tTunnel":
        rows.append(row)


# Get the widgets output
result = widgets.Output()

# Calculate the value of tTunnel
def calculate():

    values = {
        name: slider.value
        for name, slider in sliders.items()
    }

    tau = values["tau"]
    iSun = values["iSun"]
    fTunnelSky = values["fTunnelSky"]
    epsilonCover = values["epsilonCover"]
    alphaR = values["alphaR"]
    tSky = values["tSky"]
    tOut = values["tOut"]
    tSoil = values["tSoil"]
    fTunnelSoil = values["fTunnelSoil"]
    epsilonSoil = values["epsilonSoil"]
    aCoverOverSoil = values["aCoverOverSoil"]
    alphaCover = values["alphaCover"]
    alphaSoil = values["alphaSoil"]
    

    tTunnel = calc_tTunnel(tau, iSun, fTunnelSky, epsilonCover, alphaR, 
            tSky, tOut, tSoil, fTunnelSoil, epsilonSoil, aCoverOverSoil, 
            alphaCover, alphaSoil)

    return tTunnel


def update(*args):

    tTunnel = calculate()
    
    # Display result
    with result:
        result.clear_output()
        display(HTML(f"<big><strong><code>tTunnel:</strong></code> {tTunnel:0.2f} °C</big>"))


# Connect sliders
for slider in sliders.values():
    slider.observe(update, names="value")
update()

# Function for displaying everything
def display_tTunnel_widget():
    display(
        widgets.VBox(
            [header]
            + rows
            + [
                widgets.HTML("<hr>"),
                result
            ]
        )
    )


# %% [markdown]
# ## 2.6 Running the interactive model

# %% [markdown]
# Running the following code block will run and displays the interactive model. Depending on your screen resolution, it may be hard to see all model variables at the same time. Therefore, the following may help:
# - Set your browser view to full screen mode with the keyboard key F11
# - Zoom out in your browser by using the keyboard combination **Ctrl+Minus key**
# - To set the zoom back to standard setting, use the keyboard combination **Ctrl+0**

# %%
display_tTunnel_widget()

# %% [markdown]
# ### 2.6.1 Exercise: analyzing the tunnel model
# Use the interactive model above to analyze the tunnel model you created:
# - What is the highest and lowest value that you can reach for `tTunnel`?
#     - How can you reach such a value, what are the mechanisms in the model that allow it?
#     - Are these values realistic, in the sense that they can be achieved in a real greenhouse?
# - For each variable, is it positively related with `tTunnel` (an increase in the variable results in an increase in `tTunnel`) or negatively related?
#     - For the question above, does the answer depend on the values of other variables?
#     - Are there variables that do not have a strictly positive or negative relation with `tTunnel`? Can you explain why?
# - Are there variables that have a stronger influence on `tTunnel` than others? Which are the most influential variables?
# - Are the relations you've found line with what you expect from a real greenhouse?

# %% [markdown]
# ## 2.7 Going further: expanding the model to include ventilation

# %% [markdown]
# In Chapter 5 of the textbook (Section 5.3, pg. 107), the tunnel model is expanded to include ventilation. See if you can repeat the above exercise, but add the influence of ventilation as described in Section 5.3.

# %% [markdown]
# ## 2.8 Next steps: towards a dynamic model

# %% [markdown]
# You may have noticed that the interactive model we've created in this chapter is **static**: the weather variables, for example, represent a single moment in time: a single solar radiation value, a single outdoor temperature value. In practice, these variables change, and the greenhouse temperature changes along with it. Moreover, the model is based on a **steady-state assumption** (see pg. 69 of the textbook). The assumption here is that the energy entering the greenhouse is equal to the energy leaving it. In other words, the *dynamics*, or how fast or slow the greenhouse reacts to changes in the outside conditions, is also not included in the model we've built so far. In the following chapters, we will implement the model using varying weather inputs and considering the dynamics. For this, we will use the [GreenLight modelling platform](https://github.com/davkat1/greenlight).

# %%
