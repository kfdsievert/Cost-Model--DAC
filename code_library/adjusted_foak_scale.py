from energy_price import energy_price
import numpy as np

# This function calculates the First-Of-A-Kind (FOAK) scale of a technology, adjusting for carbon emissions from
# the energy supply
def adjusted_foak_scale(input, tech):

    # If the 'adjusted_foak_scale' value already exists and is not NaN, return it
    if ~np.isnan(input.unlearned.adjusted_foak_scale):
        return input.unlearned.adjusted_foak_scale

    # Retrieve the initial 'foak_scale' for the given technology
    foak_scale = input.technology.loc['foak_scale', tech]

    # Retrieve CO2 intensities for electricity and heat (units: ton CO2/GJ)
    electricity_co2, heat_co2 = energy_price(input)[2:4]

    # Retrieve energy requirements for the given technology (units: GJ/tCO2)
    electricity_requirement = input.technology.loc["electricity_requirement", tech]
    heat_requirement_gas = input.technology.loc["heat_requirement_gas", tech]
    heat_requirement_heatpump = input.technology.loc["heat_requirement_heatpump", tech]
    cop_heatpump = input.technology.loc["cop_heatpump", tech]  # Coefficient of performance for heat pump (dimensionless)

    # Calculate net electricity and heat requirements (units: GJ/tCO2)
    net_electricity_requirement = (electricity_requirement + heat_requirement_heatpump/cop_heatpump)
    net_heat_requirement = heat_requirement_gas

    # Adjust 'foak_scale' based on net electricity and heat requirements and their respective CO2 intensities
    adj_foak_scale = foak_scale*(1-net_electricity_requirement*electricity_co2-
                                 net_heat_requirement*heat_co2)
    
    # Store the adjusted 'foak_scale' for future use
    input.unlearned.adjsuted_foak_scale = adj_foak_scale
    
    # Return the adjusted 'foak_scale'
    return adj_foak_scale