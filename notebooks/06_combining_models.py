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

# %%
crop_definition = {
    "W": {
        "description": "Crop dry mass",
        "unit": "g/m2",
        "definition": "LUE * (1 - exp(-k*LAI)) * I * 1e-6",
        "type": "state",
        "init": "75",
        "reference": "Stanghellini (2019), Eq. 2.25. " \
                    "Note that in Eq. 2.5 (Stanghellini 2019), dW/dt is given in g/m2/day. " \
                    "However, solar light is expressed there as I, in MJ/m2/day. " \
                    "Here we use I instead in W/m2 = J/m2/s (see reference for I). " \
                    "This is multiplied by 1e-6, to convert to MW/m2 = MJ/m2/s. " \
                    "Thus we use I*1e-6 which is in MJ/m2/s, instead of MJ/m2/day. " \
                    "Therefore the unit for dW/dt becomes g/m2/s instead of g/m2/day. " \
                    "The default time unit in GreenLight is s, so W is automatically in g/m2." \
                    "The initial value of 75 g/m2 is based on Fig. 2.13 (Stanghellini 2019)" \
                    "As a reasonable value for a small crop"
    },
     "LUE": {
         "description": "Light use efficiency",
         "unit": "g crop weight per MJ PAR",
         "definition": "4.3",
         "type": "const",
         "reference": "Stanghellini (2019), pg. 49. 4.3 is chosen as a middle value, see Fig. 2.13"
    },
     "k": {
         "description": "Light extinction coefficient",
         "unit": "-",
         "definition": "0.7",
         "type": "const",
         "reference": "Stanghellini (2019), pg. 49. " \
                      "The value of 0.7 is based on Stanghellini (2019), pg. 39: " \
                      "'For many greenhouse crops, k has a value between 0.6 and 0.8'"
    },
     "I": {
         "description": "Light intensity",
         "unit": "W/m2",
         "definition": "I",
         "type": "input",
         "reference": "Stanghellini (2019), pg. 49. " \
                      "Since the default time unit in GreenLight is seconds, " \
                      "It is more convenient to use I in J/m2/s = W/m2 instead of MJ/m2/day. "\
                      "This is adjusted in the definition of W, see there"
    },
    "LAI": {
        "description": "Leaf area index",
        "unit": "m2 leaf per m2 floor",
        "definition": "W * fLeaves * SLA / 10000",
        "type": "aux",
        "reference": "Stanghellini (2019), Eq. 2.26. " \
                     "Note that according to the Eq., the LAI growth rate is equal to " \
                     "crop growth rate times fLeaves * SLA / 10000. " \
                     "Therefore LAI is equal to crop dry mass times the same factor" 
    },
     "fLeaves": {
         "description": "Fraction of crop dry mass partitioned to the leaves",
         "unit": "-",
         "definition": "0.8",
         "type": "const",
         "reference": "Stanghellini (2019), Eq. 2.26. " \
                      "The value of 0.8 is chosen to represent a young vegetative crop"
    },
     "SLA": {
         "description": "Specific leaf area",
         "unit": "cm2/g",
         "definition": "250",
         "type": "const",
         "reference": "Stanghellini (2019), Box 2.26. " \
                      "The value of 250 is a middle value for tomato, "\
                      "See Stanghellini (2019), Table 2.1"
    }   
 }

# %%
tunnel_def = {
    "tau": {
        "description": "Transmissivity (hemispherical) of the cover for sun radiation",
        "unit": "-",
        "reference": "Stanghellini et al. (2024), Eq. 3.2 & Table 3.1",
        "definition": "0.8",
        "type": "const"
    },
    "iSun": {
        "name": "iSun",
        "description": "Solar radiation",
        "unit": "W/m2",
        "reference": "Stanghellini et al. (2024), Eq. 3.2",
        "definition": "700",
        "type": "input"
    },
    "fTunnelSky": {
        "description": "View factor between tunnel and sky",
        "unit": "-",
        "reference": "Stanghellini et al. (2024), Eq. 3.5 & pg. 70",
        "definition": "0.5",
        "type": "const"
    },
    "epsilonCover": {
        "description": "Emissivity of the cover, including effect of screen(s)",
        "unit": "-",
        "reference": "Stanghellini et al. (2024), Eq. 3.3 & Section 3.2.1",
        "definition": "1",
        "type": "const"
    },
    "alphaR": {
        "description": "Apparent transfer coefficient for thermal radiation",
        "unit": "-",
        "reference": "Stanghellini et al. (2024), Eq. 3.6 & paragraph following",
        "definition": "6",
        "type": "const"
    },
    "tSky": {
        "description": "Apparent temperature of the sky (depends, among other things, on cloudiness)",
        "unit": "°C",
        "reference": "Stanghellini et al. (2024), Eq. 3.9",
        "definition": "0",
        "type": "input"
    },
    "tOut": {
        "description": "Temperature of the air outside the greenhouse",
        "unit": "°C",
        "reference": "Stanghellini et al. (2024), Eq. 3.9",
        "definition": "30",
        "type": "input"
    },
    "tSoil": {
        "description": "Temperature of the soil surface",
        "unit": "°C",
        "reference": "Stanghellini et al. (2024), Eq. 3.9",
        "definition": "35",
        "type": "input"
    },
    "fTunnelSoil": {
        "description": "View factor between tunnel and soil",
        "unit": "-",
        "reference": "Stanghellini et al. (2024), Eq. 3.5 & pg. 70",
        "definition": "0.5",
        "type": "const"
    },
    "epsilonSoil": {
        "description": "Emissivity of the soil, including possible effect of mulch",
        "unit": "-",
        "reference": "Stanghellini et al. (2024), Eq. 3.3 & Section 3.2.1",
        "definition": "1",
        "type": "const"
    },
    "aCoverOverSoil": {
        "description": "Surface area of cover per unit surface area of soil",
        "unit": "-",
        "reference": "Stanghellini et al. (2024), Eq. 3.7. This variable is used to represent aCover divided by aSoil",
        "definition": "1.2",
        "type": "const"
    },
    "alphaCover": {
        "description": "Heat transfer coefficient of the cover material (including possible screens)",
        "unit": "W/m2/K",
        "reference": "Stanghellini et al. (2024), Eq. 3.7",
        "definition": "4",
        "type": "const"
    },
    "alphaSoil": {
        "description": "Heat transfer coefficient of the soil (including possible mulches)",
        "unit": "W/m2/K",
        "reference": "Stanghellini et al. (2024), Eq. 3.68",
        "definition": "4",
        "type": "const"
    },
    "tTunnel": 
}



# %%
