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
#

# %% [markdown]
# Outline
# - Eq 3.9 textbook
# - Textbook chapter 3
# - We will make a slider thingie
# - Recommend to have the TOC on the side

# %% [markdown]
# ## 2.1 Imports for Chapter 2

# %% [markdown]
# The following code block defines imports that will be used later in this notebook. There's no need to read through this code, simply run it and move to the next section

# %%
""" 
Imports needed for running the code
"""
import ipywidgets as widgets
from IPython.display import display, Math


# %% [markdown]
# ## 2.2 Defining the tunnel model variables

# %% [markdown]
# - Create a Python dictionary (`dict`) that defines the variables, we will call this dictionary `sliders_vars`
# - `sliders_vars` is a dictionary of dictionaries
# - Each variable will be an entry in the dictionary `sliders_vars`, with the key as the variable name, and the value as a dictionary
# - For each value, we define:
#     - Description
#     - Unit
#     - Reference
#     - Value
#     - Min
#     - Max
#     - Step

# %% [markdown]
# ### 2.2.1 Example: some tunnel model variables
# In the code block below we start defining `sliders_vars`, following the text after Eq 3.9. We define: 
# - **𝜏** (Greek letter tau), which we write in code as `tau`
# - $I_{sun}$ , which we write in code as `iSun`
# - $F_{tunnel,sky}$ , which we write in code as `fTunnelSky`
#
# Where:
# - The **description** is taken directly from the text under Eq. 3.9
# - The **reference** is taken from the text under Eq. 3.9. If no reference is given, we refer simply to Eq. 3.9
# - The **value** is an estimate or example for a reasonable value. For example, for **𝜏**, Table 3.1 gives an indication
# - The **min** and **max** values are values that will be displayed in the sliders. We choose values that are reasonabl or interesting to consider
# - **step** is the step size that the slider allows. For example, a value of 5 and a step size of 0.1, means value like 4.9 and 5.1 will be used, but not 4.91 and 5.11.
#
# **Note**: ~~~something about converting equations like $I_{sun}$ to code like `iSun`

# %%
""" 
Example 2.2.1
Define tunnel model variables to be used in sliders 
"""
sliders_vars = {
    "tau": {
        "description": "Transmissivity (hemispherical) of the cover for sun radiation",
        "unit": "-",
        "reference": "Stanghellini et al. (2024), Eq. 3.2",
        "value": 0.8,
        "min": 0,
        "max": 1,
        "step": 0.01
    },
    "iSun": {
        "name": "iSun",
        "description": "Solar radiation",
        "unit": "W/m2",
        "reference": "Stanghellini et al. (2024), Eq. 3.9",
        "value": 700,
        "min": 0,
        "max": 1500,
        "step": 10
    },
    "fTunnelSky": {
        "description": "View factor between tunnel and sky",
        "unit": "-",
        "reference": "Stanghellini et al. (2024), Eq. 3.5",
        "value": 0.5,
        "min": 0,
        "max": 1,
        "step": 0.01
    }
}

# %% [markdown]
# ### 2.2.2 Exercise: completeing the tunnel model variables
#
# In the following code block, complete the definition of `sliders_vars` as above, to include all variables described in Equation 3.9.
#
# **Be sure to check that you have defined *all* the variables of Equation 3.9!**

# %%
""" 
Exercise 2.2.2
Define tunnel model variables to be used in sliders 
"""
sliders_vars = {
    "tau": {
        "description": "Transmissivity (hemispherical) of the cover for sun radiation",
        "unit": "-",
        "reference": "Stanghellini et al. (2024), Eq. 3.2",
        "value": 0.8,
        "min": 0,
        "max": 1,
        "step": 0.01
    },
    "iSun": {
        "name": "iSun",
        "description": "Solar radiation",
        "unit": "W/m2",
        "reference": "Stanghellini et al. (2024), Eq. 3.9",
        "value": 700,
        "min": 0,
        "max": 1500,
        "step": 10
    },
    "fTunnelSky": {
        "description": "View factor between tunnel and sky",
        "unit": "-",
        "reference": "Stanghellini et al. (2024), Eq. 3.5",
        "value": 0.5,
        "min": 0,
        "max": 1,
        "step": 0.01
    },
    "continue here...": 
}

# %% [markdown]
# #### 2.2.2 Solution
#
# The following code block is a possible solution to **Exercise 2.2.2**

# %%
""" 
Solution for Exercise 2.2.2
Define tunnel model variables to be used in sliders 
"""
sliders_vars = {
    "tau": {
        "description": "Transmissivity (hemispherical) of the cover for sun radiation",
        "unit": "-",
        "reference": "Stanghellini et al. (2024), Eq. 3.2",
        "value": 0.8,
        "min": 0,
        "max": 1,
        "step": 0.01
    },
    "iSun": {
        "name": "iSun",
        "description": "Solar radiation",
        "unit": "W/m2",
        "reference": "Stanghellini et al. (2024), Eq. 3.9",
        "value": 700,
        "min": 0,
        "max": 1500,
        "step": 10
    },
    "fTunnelSky": {
        "description": "View factor between tunnel and sky",
        "unit": "-",
        "reference": "Stanghellini et al. (2024), Eq. 3.5",
        "value": 0.5,
        "min": 0,
        "max": 1,
        "step": 0.01
    },
    "epsCover": {
        "description": "Emissivity of the cover, including effect of screen(s)",
        "unit": "-",
        "reference": "Stanghellini et al. (2024), Eq. 3.3",
        "value": 1,
        "min": 0,
        "max": 1,
        "step": 0.01
    },
    "alphaR": {
        "description": "Apparent transfer coefficient for thermal radiation",
        "unit": "-",
        "reference": "Stanghellini et al. (2024), Eq. 3.6",
        "value": 6,
        "min": 0,
        "max": 20,
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
        "reference": "Stanghellini et al. (2024), Eq. 3.5",
        "value": 0.5,
        "min": 0,
        "max": 1,
        "step": 0.01
    },
    "epsSoil": {
        "description": "Emissivity of the soil, including possible effect of mulch",
        "unit": "-",
        "reference": "Stanghellini et al. (2024), Eq. 3.3",
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
        "value": 6,
        "min": 0,
        "max": 20,
        "step": 0.1
    },
    "alphaSoil": {
        "description": "Heat transfer coefficient of the soil (including possible mulches)",
        "unit": "W/m2/K",
        "reference": "Stanghellini et al. (2024), Eq. 3.68",
        "value": 5,
        "min": 0,
        "max": 20,
        "step": 0.1
    }
}


# %% [markdown]
# ### 2.2.3 Reflection: constructing the tunnel model
#
# Before moving forward, stop to reflect on the following questions:
# - How was the experience of converting the equation from a textbook to code?
# - Were all variables clearly defined in the textbook?
# - Was it easy to choose representative values and ranges?

# %% [markdown]
# ## 2.3 Defining calculation of `tTunnel`

# %% [markdown]
# - The goal is to see what happens to tTunnel when other things change
# - Need to calculate tTunnel

# %% [markdown]
# ### 2.3.1 Exercise: algebraically solving for `tTunnel`
#
# This is an exercise in algebra:
#
# **Solve Equation 3.9 for $T_{tunnel}$.**
#
# In other words, rearrange Equation 3.9 so that $T_{tunnel}$ is isolated.
#
# ~~ links to how this can be done

# %% [markdown]
# #### 2.3.1 Solution
#
#

# %% [markdown]
# We start with Eqaution 3.9:
#
# $$
# \begin{align}
# \tau I_{sun} &= F_{tunnel,sky} \varepsilon_{cover} \alpha_R \left( T_{tunnel} - T_{sky} \right) + \frac{A_{cover}}{A_{soil}} \alpha_{cover} \left( T_{tunnel} - T_{out} \right)\\
# &+F_{tunnel,soil} \varepsilon_{soil} \alpha_R \left( T_{tunnel} - T_{soil} \right) +\alpha_{soil} \left( T_{tunnel} - T_{soil} \right)\\
# \end{align}
# $$
#
# ~~ to do

# %% [markdown]
# ## 2.4 Setting up the interactive model
#
#
#

# %% [markdown]
# Explain code below, stress that the Python details are not very important

# %%
# Define calculation of tTunnel
def calc_tTunnel(tau, iSun, fTunnelSky, epsCover, alphaR, 
            tSky, tOut, tSoil, fTunnelSoil, epsSoil, aCoverOverSoil, 
            alphaCover, alphaSoil):
    tTunnel = ( 
            tau * iSun 
            + fTunnelSky * epsCover * alphaR * tSky 
            + aCoverOverSoil * alphaCover * tOut 
            + tSoil * (fTunnelSoil * epsSoil * alphaR + alphaSoil)
        ) / (
            fTunnelSky * epsCover * alphaR 
            + aCoverOverSoil * alphaCover 
            + fTunnelSoil * epsSoil * alphaR 
            + alphaSoil
        )
    return tTunnel


# Define displayed equation
equation_latex = r"""
\texttt{tTunnel} =
\frac{
\texttt{tau} \times \texttt{iSun}
+
\texttt{fTunnelSky}\times\texttt{epsCover}\times\texttt{alphaR}\times\texttt{tSky}
+
\texttt{aCoverOverSoil}\times\texttt{alphaCover}\times\texttt{tOut}
+
\mathrm{tSoil}\times
\left(
\texttt{fTunnelSoil}\times\texttt{epsSoil}\times\texttt{alphaR}
+
\texttt{alphaSoil}
\right)
}{
\texttt{fTunnelSky}\times\texttt{epsCover}\times\texttt{alphaR}
+
\texttt{aCoverOverSoil}\times\texttt{alphaCover}
+
\texttt{fTunnelSoil}\times\texttt{epsSoil}\times\texttt{alphaR}
+
\texttt{alphaSoil}
}
"""

# Define dynamic display
def dynamic_display(tau, iSun, fTunnelSky, epsCover, alphaR, 
            tSky, tOut, tSoil, fTunnelSoil, epsSoil, aCoverOverSoil, 
            alphaCover, alphaSoil):
    numerator = (
        tau*iSun
        + fTunnelSky*epsCover*alphaR*tSky
        + aCoverOverSoil*alphaCover*tOut
        + tSoil*(fTunnelSoil*epsSoil*alphaR + alphaSoil)
    )

    denominator = (
        fTunnelSky*epsCover*alphaR
        + aCoverOverSoil*alphaCover
        + fTunnelSoil*epsSoil*alphaR
        + alphaSoil
    )

    tTunnel = calc_tTunnel(tau, iSun, fTunnelSky, epsCover, alphaR, 
            tSky, tOut, tSoil, fTunnelSoil, epsSoil, aCoverOverSoil, 
            alphaCover, alphaSoil)

    substituted_equation = rf"""
        =
        \frac{{
        {tau:.2f}\times{iSun:.0f}
        +
        {fTunnelSky:.2f}\times{epsCover:.2f}\times{alphaR:.1f}\times{tSky:.0f}
        +
        {aCoverOverSoil:.1f}\times{alphaCover:.1f}\times{tOut:.0f}
        +
        {tSoil:.0f}\times
        \left(
        {fTunnelSoil:.2f}\times{epsSoil:.2f}\times{alphaR:.1f}
        +
        {alphaSoil:.2f}
        \right)
        }}
        {{
        {fTunnelSky:.2f}\times{epsCover:.2f}\times{alphaR:.1f}
        +
        {aCoverOverSoil:.1f}\times{alphaCover:.1f}
        +
        {fTunnelSoil:.2f}\times{epsSoil:.2f}\times{alphaR:.1f}
        +
        {alphaSoil:.2f}
        }}
        =
        \frac{{{numerator:.2f}}}{{{denominator:.2f}}}
        =
        {{{tTunnel:.1f}}}\,^\circ\mathrm{{C}}
        
        """
    return substituted_equation


# %% [markdown]
# Explain code below, stress that it can be skipped

# %%
# Create header row
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
        "<b>Description</b>",
        layout=widgets.Layout(width="250px")
    ),
    widgets.HTML(
        "<b>Unit</b>",
        layout=widgets.Layout(width="100px")
    ),
    widgets.HTML(
        "<b>Reference</b>",
        layout=widgets.Layout(width="200px")
    )
])


# Create parameter rows
sliders = {}
rows = []

for name, var in sliders_vars.items():
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
            var["description"],
            layout=widgets.Layout(width="250px")
        ),
        widgets.HTML(
            var["unit"],
            layout=widgets.Layout(width="100px")
        ),
        widgets.HTML(
            f"<i>{var['reference']}</i>",
            layout=widgets.Layout(width="200px")
        )
    ])

    rows.append(row)


# Calculate tTunnel
result = widgets.Output()

def calculate():

    values = {
        name: slider.value
        for name, slider in sliders.items()
    }

    tau = values["tau"]
    iSun = values["iSun"]
    fTunnelSky = values["fTunnelSky"]
    epsCover = values["epsCover"]
    alphaR = values["alphaR"]
    tSky = values["tSky"]
    tOut = values["tOut"]
    tSoil = values["tSoil"]
    fTunnelSoil = values["fTunnelSoil"]
    epsSoil = values["epsSoil"]
    aCoverOverSoil = values["aCoverOverSoil"]
    alphaCover = values["alphaCover"]
    alphaSoil = values["alphaSoil"]
    

    tTunnel = calc_tTunnel(tau, iSun, fTunnelSky, epsCover, alphaR, 
            tSky, tOut, tSoil, fTunnelSoil, epsSoil, aCoverOverSoil, 
            alphaCover, alphaSoil)

    return tTunnel, values


def update(*args):

    tTunnel, values = calculate()

    tau = values["tau"]
    iSun = values["iSun"]
    fTunnelSky = values["fTunnelSky"]
    epsCover = values["epsCover"]
    alphaR = values["alphaR"]
    tSky = values["tSky"]
    tOut = values["tOut"]
    tSoil = values["tSoil"]
    fTunnelSoil = values["fTunnelSoil"]
    epsSoil = values["epsSoil"]
    aCoverOverSoil = values["aCoverOverSoil"]
    alphaCover = values["alphaCover"]
    alphaSoil = values["alphaSoil"]

    substituted_equation = dynamic_display(tau, iSun, fTunnelSky, epsCover, alphaR, 
            tSky, tOut, tSoil, fTunnelSoil, epsSoil, aCoverOverSoil, 
            alphaCover, alphaSoil)

    with result:
        result.clear_output()

        # General equation
        display(Math(equation_latex))

        display(widgets.HTML("<br><br>"))

        # Numerical equation
        display(Math(substituted_equation))


# Connect sliders
for slider in sliders.values():
    slider.observe(update, names="value")
update()

# Display everything
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
# ## 2.5 Interactive greenhouse "tunnel" model

# %% [markdown]
# The following code block displays the sliders widget
#
# Depending on your screen resolution, it may be hard to see everything so:
# - zoom out in your browser
# - go for zen mode
# - gor for full screen
# - click on the left hand side of the display (collapse output)

# %%
display_tTunnel_widget()

# %% [markdown]
# ### 2.5.1 Exercise: analyzing the tunnel model
# - For each variable, does it go together with tTunnel (incerase -> increase) or the other way around
# - Is this in line with what you expect
# - Are there variables that have a stronger influence than others?
# - Are there variables that have an optimum behaviour
# - Do the answers above (for each variable) depend on the values of other variables?

# %% [markdown]
# ## Next step

# %% [markdown]
# Just describe the next step
