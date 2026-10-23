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
# # Variables of the model

# %% [markdown]
# In this exercise you will read the model equations and lay out what variables the model includes and what is the relation between them. As in this entire lesson we focus on Eq. 2.25 (pg. 49) and Eq. 2.26 (pg. 50) of [the course textbook](https://doi.org/10.1163/9789004697041). 

# %% [markdown]
# ## Exercise 1

# %% [markdown]
# ```{exercise}
# :label: exercise-crop-model-variables
# :enumerated: true
#
# Examine Eq. 2.25 and Eq. 2.26 in the course textbook (pp. 49-50), and write down the following:
# - Which variables are used in these equations?
# - For each variable:
#     - What is it called in the equations?
#     - What does it represent?
#     - What units is it in?
#     - Is it a constant value, or does it evolve through time?
#     - Is it an input (the values should be given to the model), calculated based on other variables, or calculated using a differential equation?
# ```

# %% [markdown]
# :::{note} ⏱️ Time estimate
# :icon: false
# 20 minutes to 1 hour
# :::

# %% [markdown]
# ### Note on differential equations

# %% [markdown]
# :::{note} Note on differential equations
# :class: dropdown
#
# ```{figure} ../../Figures/Parabolic_trajectory.svg
# ---
# width: 100%
# align: center
# ---
# **Figure 2.1.** Differential of a parabola.<br>
# Image in the public domain, https://commons.wikimedia.org/wiki/File:Parabolic_trajectory.svg
# ```
#
# If the concept of differential equations is unfamiliar to you, at this point it is sufficient to note that in Eq. 2.25, the notation $\mathrm{d}W/\mathrm{d}t$ indicates "the rate of change of $W$ as time ($t$) passes". Thus, $\mathrm{d}W/\mathrm{d}t$ indicates the *derivative* (or *differential*) of $W$ with respect to $t$. Another notation for this concept which you may have seen in the past is $y'$. In this case the derived variable is $W$, so the corresponding notation would be $W'$. 
#
# What this means in practice is that the right hand side of Eq. 2.25: 
# $$\mathrm{d}W/\mathrm{d}t = LUE \cdot \left( 1 - e^{-k \cdot LAI} \right) \cdot I$$
# is *the rate of change of $W$*. Thus, if $LUE \cdot \left( 1 - e^{-k \cdot LAI} \right) \cdot I = $ 1 g m<sup>-2</sup> d<sup>-1</sup>, then $W$ grows at a rate of 1 g m<sup>-2</sup> d<sup>-1</sup>.
#
# For more information, see [Ordinary differential equation on Wikipedia](https://en.wikipedia.org/wiki/Ordinary_differential_equation) and this chapter from [Python Programming and Numerical Methods - A Guide for Engineers and Scientists](https://pythonnumericalmethods.studentorg.berkeley.edu/notebooks/chapter22.00-ODE-Initial-Value-Problems.html).
# :::

# %% [markdown]
# ## Solution 1

# %% [markdown]
# ```{solution} exercise-crop-model-variables
# :label: solution-crop-model-variables
# :enumerated: true
# :class: dropdown
#
# **<span style="font-size: 1.2em">The variables in Eq. 2.25 are:</span>**
# - $W$, representing **crop growth rate**
#     - Its unit is g m<sup>-2</sup>
#     - Its value evolves through time
#     - It is calculated based on other variables, using a differential equation
# **Note:** The unit of $\mathrm{d}W/\mathrm{d}t$, which is the rate of change of $W$, is g m<sup>-2</sup> d<sup>-1</sup>. Thus the unit of $W$ itself does not include the time factor d<sup>-1</sup> ("per day"). <br><br>
#
# - $LUE$, representing **light use efficiency**
#     - Its unit is g MJ<sup>-1</sup> PAR
#     - "Equation 2.25 assumes a constant LUE" (pg. 49). Our goal here is to create a simple crop model, so we will stick to this assumption. However, see the discussion on pg. 49 for other possible approaches
#     - As a constant value, it should be given to the model<br><br>
#
# - $k$, representing **light extinction coefficient**
#     - It is unitless: note that "$\left( 1 - e^{-k \cdot LAI} \right)$ represents the fraction of intercepted light". As a fraction it is a unitless value. This implies that $e^{-k \cdot LAI}$ and since we may consider $LAI$ as unitless (m<sup>2</sup> leaves per m<sup>2</sup> floor, resulting in $m^{2}/m^{2} = 1$), then $k$ must also be unitless
#     - Consider the text below Eq. 2.17, pg. 39: "k is not strictly constant [...] however, applying a constant k value provides an accurate enough estimation [...]". Again, since we would like to have a simple model, a constant value is currently sufficient
#     - As a constant value, it should be given to the model<br><br>
#
# - $LAI$, representing **leaf area index**
#     - See pg. 38: its unit is m<sup>2</sup> leaves per m<sup>2</sup> ground area, which we may consider as unitless ($m^{2}/m^{2} = 1$)
#     - Its value evolves through time
#     - It is calculated based on other variables, see Eq. 2.26. This equation describeds the difference between "$LAI$ on day $t$ and day $t-1$, so it may be considered a *difference equation* or a differential equation<br><br>
#
# - $I$, representing **daily light sum**
#     - Its unit is g MJ<sup>-1</sup> PAR m<sup>-2</sup>
#     - Its value evolves in time, and should be given to the model<br><br>
#
# **<span style="font-size: 1.2em">The variables in Eq. 2.26 are:</span>**
# - $LAI$, see above<br><br>
#
# - $GR$, representing **crop growth rate**
#     - Its unit is g m<sup>-2</sup> d<sup>-1</sup>
#     - Its value evolves through time
#     - It is calculated based on other variables. In fact, this is precisely the value $\mathrm{d}W/\mathrm{d}t$<br><br>
#
# - $F_{leaves}$, representing **fraction partitioned to the leaves**
#     - As a fraction, it is unitless
#     - Its value evolves through time: a vegetative crop (for example, young tomato plant with no flowers) has a high $F_{leaves}$, while a mature crop with many fruit has a lower $F_{leaves}$
#     - This variable depends on other variables, see for example pg. 52<br><br>
#     
# - $SLA$, representing **specific leaf area**
#     - Its unit is cm<sup>2</sup> g<sup>-1</sup>
#     - Its value evolves through time: a vegetative crop (for example, young tomato plant with no flowers) has a high $F_{leaves}$, while a mature crop with many fruit has a lower $F_{leaves}$
#     - See pg. 50: "[SLA] varies between crop species [...] as well as with plant age, season and environmental conditions [...], but it is nonetheless often taken as a constant"
# ```

# %% [markdown]
# ## Reflection

# %% [markdown]
# Take a moment to reflect on the last exercise: how was it to list and describe all the variables of a simple (2 equations) model? Was it straightforward? Or did it require some detective work? Did you need the help of the provided solution? Does the solution require creativity or inventiveness?

# %% [markdown]
# :::{note} ⏱️ Time estimate
# :icon: false
# It is useful to spend 5-10 minutes on this reflection, and really write down some conclusions.
# :::
