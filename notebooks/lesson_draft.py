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
# Outline
# 1. Excel exercise of simple model - interactive formula
# 2. Build the exercise in GreenLight
#
#

# %% [markdown]
# ## Code

# %%
import ipywidgets as widgets
from IPython.display import display, Math


# Define model variables
parameters = [
    {
        "name": "tau",
        "description": "Transmissivity (hemispherical) of the cover for sun radiation",
        "unit": "-",
        "reference": "Stanghellini et al. (2024), Eq. 3.2",
        "value": 0.7,
        "min": 0,
        "max": 1,
        "step": 0.01
    },
    {
        "name": "iSun",
        "description": "Solar radiation",
        "unit": "W/m2",
        "reference": "Stanghellini et al. (2024), Eq. 3.9",
        "value": 700,
        "min": 0,
        "max": 1500,
        "step": 10
    },
    {
        "name": "fTunnelSky",
        "description": "View factor between tunnel and sky",
        "unit": "-",
        "reference": "Stanghellini et al. (2024), Eq. 3.5",
        "value": 0.5,
        "min": 0,
        "max": 1,
        "step": 0.01
    },
    {
        "name": "epsCover",
        "description": "Emissivity of the cover, including effect of screen(s)",
        "unit": "-",
        "reference": "Stanghellini et al. (2024), Eq. 3.3",
        "value": 1,
        "min": 0,
        "max": 1,
        "step": 0.01
    },
    {
        "name": "alphaR",
        "description": "Apparent transfer coefficient for thermal radiation",
        "unit": "-",
        "reference": "Stanghellini et al. (2024), Eq. 3.6",
        "value": 6,
        "min": 0,
        "max": 20,
        "step": 0.1
    },
    {
        "name": "tSky",
        "description": "Apparent temperature of the sky (depends, among other things, on cloudiness)",
        "unit": "°C",
        "reference": "Stanghellini et al. (2024), Eq. 3.9",
        "value": 0,
        "min": -50,
        "max": 50,
        "step": 1
    },
    {
        "name": "tOut",
        "description": "Temperature of the air outside the greenhouse",
        "unit": "°C",
        "reference": "Stanghellini et al. (2024), Eq. 3.9",
        "value": 30,
        "min": -50,
        "max": 50,
        "step": 1
    },
    {
        "name": "tSoil",
        "description": "Temperature of the soil surface",
        "unit": "°C",
        "reference": "Stanghellini et al. (2024), Eq. 3.9",
        "value": 35,
        "min": -50,
        "max": 50,
        "step": 1
    },
    {
        "name": "fTunnelSoil",
        "description": "View factor between tunnel and soil",
        "unit": "-",
        "reference": "Stanghellini et al. (2024), Eq. 3.5",
        "value": 0.5,
        "min": 0,
        "max": 1,
        "step": 0.01
    },
    {
        "name": "epsSoil",
        "description": "Emissivity of the soil, including possible effect of mulch",
        "unit": "-",
        "reference": "Stanghellini et al. (2024), Eq. 3.3",
        "value": 1,
        "min": 0,
        "max": 1,
        "step": 0.01
    },
    {
        "name": "aCoverOverSoil",
        "description": "Surface area of cover per unit surface area of soil",
        "unit": "-",
        "reference": "Stanghellini et al. (2024), Eq. 3.7. This variable is used to represent aCover divided by aSoil",
        "value": 1.2,
        "min": 0,
        "max": 5,
        "step": 0.1
    },
    {
        "name": "alphaCover",
        "description": "Heat transfer coefficient of the cover material (including possible screens)",
        "unit": "W/m2/K",
        "reference": "Stanghellini et al. (2024), Eq. 3.7",
        "value": 6,
        "min": 0,
        "max": 20,
        "step": 0.1
    },
    {
        "name": "alphaSoil",
        "description": "Heat transfer coefficient of the soil (including possible mulches)",
        "unit": "W/m2/K",
        "reference": "Stanghellini et al. (2024), Eq. 3.68",
        "value": 5,
        "min": 0,
        "max": 20,
        "step": 0.1
    },
]

# Define displayed equation
equation_latex = r"""
tTunnel =
\frac{
\tau \times \mathrm{iSun}
+
\mathrm{fTunnelSky}\times\mathrm{epsCover}\times\mathrm{alphaR}\times\mathrm{tSky}
+
\mathrm{aCoverOverSoil}\times\mathrm{alphaCover}\times\mathrm{tOut}
+
\mathrm{tSoil}\times
\left(
\mathrm{fTunnelSoil}\times\mathrm{epsSoil}\times\mathrm{alphaR}
+
\mathrm{alphaSoil}
\right)
}{
\mathrm{fTunnelSky}\times\mathrm{epsCover}\times\mathrm{alphaR}
+
\mathrm{aCoverOverSoil}\times\mathrm{alphaCover}
+
\mathrm{fTunnelSoil}\times\mathrm{epsSoil}\times\mathrm{alphaR}
+
\mathrm{alphaSoil}
}
"""

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

for p in parameters:

    slider = widgets.FloatSlider(
        value=p["value"],
        min=p["min"],
        max=p["max"],
        step=p["step"],
        continuous_update=True,
        layout=widgets.Layout(width="300px")
    )

    sliders[p["name"]] = slider

    row = widgets.HBox([
        widgets.HTML(
            f"<code><b>{p['name']}</b></code>",
            layout=widgets.Layout(width="150px")
        ),
        slider,
        widgets.HTML(
            p["description"],
            layout=widgets.Layout(width="250px")
        ),
        widgets.HTML(
            p["unit"],
            layout=widgets.Layout(width="100px")
        ),
        widgets.HTML(
            f"<i>{p['reference']}</i>",
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

    # Calculate tTunnel
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
# ## Widget

# %%
display_tTunnel_widget()

# %% [markdown]
# ## Next step

# %%
# Define model variables
tunnel_model = {
    "tau": {
        "description": "Transmissivity (hemispherical) of the cover for sun radiation",
        "unit": "-",
        "reference": "Stanghellini et al. (2024), Eq. 3.2",
        "definition": 0.7,
        "type": "const"
    },
    "iSun": {
        "description": "Solar radiation",
        "unit": "W/m2",
        "reference": "Stanghellini et al. (2024), Eq. 3.9",
        "definition": 700,
        "type": "const"
    },
    "fTunnelSky": {
        "description": "View factor between tunnel and sky",
        "unit": "-",
        "reference": "Stanghellini et al. (2024), Eq. 3.5",
        "definition": 0.5,
        "type": "const"
    },
    "epsCover": {
        "description": "Emissivity of the cover, including effect of screen(s)",
        "unit": "-",
        "reference": "Stanghellini et al. (2024), Eq. 3.3",
        "definition": 1,
        "type": "const"
    },
    "alphaR": {
        "description": "Apparent transfer coefficient for thermal radiation",
        "unit": "-",
        "reference": "Stanghellini et al. (2024), Eq. 3.6",
        "definition": 6,
        "type": "const"
    },
    "tSky": {
        "description": "Apparent temperature of the sky (depends, among other things, on cloudiness)",
        "unit": "°C",
        "reference": "Stanghellini et al. (2024), Eq. 3.9",
        "definition": 0,
        "type": "input"
    },
    "tOut": {
        "description": "Temperature of the air outside the greenhouse",
        "unit": "°C",
        "reference": "Stanghellini et al. (2024), Eq. 3.9",
        "definition": 30,
        "type": "input"
    },
    "tSoil": {
        "description": "Temperature of the soil surface",
        "unit": "°C",
        "reference": "Stanghellini et al. (2024), Eq. 3.9",
        "definition": 35,
        "type": "input"
    },
    "fTunnelSoil": {
        "description": "View factor between tunnel and soil",
        "unit": "-",
        "reference": "Stanghellini et al. (2024), Eq. 3.5",
        "definition": 0.5,
        "type": "const"
    },
    "epsSoil": {
        "description": "Emissivity of the soil, including possible effect of mulch",
        "unit": "-",
        "reference": "Stanghellini et al. (2024), Eq. 3.3",
        "definition": 1,
        "type": "const"
    },
    "aCoverOverSoil": {
        "description": "Surface area of cover per unit surface area of soil",
        "unit": "-",
        "reference": "Stanghellini et al. (2024), Eq. 3.7. This variable is used to represent aCover divided by aSoil",
        "definition": 1.2,
        "type": "const"
    },
    "alphaCover": {
        "description": "Heat transfer coefficient of the cover material (including possible screens)",
        "unit": "W/m2/K",
        "reference": "Stanghellini et al. (2024), Eq. 3.7",
        "definition": 6,
        "type": "const"
    },
    "alphaSoil": {
        "description": "Heat transfer coefficient of the soil (including possible mulches)",
        "unit": "W/m2/K",
        "reference": "Stanghellini et al. (2024), Eq. 3.68",
        "definition": 5,
        "type": "const"
    }
}

# %%
tunnel_model.update({
    "tTunnel": {
        "description": "Temperature of the unventilated greenhouse",
        "unit": "°C",
        "reference": "Stanghellini et al. (2024), Eq. 3.9 (rearranged to isolate tTunnel)",
        "type": "state",
        "definition": "(" \
        "tau * iSun " \
        "+ fTunnelSky * epsCover * alphaR * tSky " \
        "+ aCoverOverSoil * alphaCover * tOut " \
        "+ tSoil * (fTunnelSoil * epsSoil * alphaR + alphaSoil)" \
    ") / ( " \
        "fTunnelSky * epsCover * alphaR " \
        "+ aCoverOverSoil * alphaCover " \
        "+ fTunnelSoil * epsSoil * alphaR " \
        "+ alphaSoil " \
    ")",
    }
})

# %%
import pprint
pprint.pprint(tunnel_model)

# %%
import green
