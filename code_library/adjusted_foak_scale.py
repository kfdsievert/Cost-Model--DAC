from energy_price import energy_price
import numpy as np

#Calculates the FOAK scale of a technology, adjusting for carbon emissions from
#the energy supply
def adjusted_foak_scale(input, tech):

    #function returns the existing value of adjusted_foak_scale
    if ~np.isnan(input.unlearned.adjusted_foak_scale):
        return input.unlearned.adjusted_foak_scale

    #get initial foak scale
    foak_scale = input.technology.loc['foak_scale', tech]

    #get co2 intensities
    electricity_co2, heat_co2 = energy_price(input)[2:4] #unit: ton co2/GJ

    #get energy requirement
    electricity_requirement = input.technology.loc["electricity_requirement", tech]#Unit: GJ/tCO2
    heat_requirement_gas = input.technology.loc["heat_requirement_gas", tech]#Unit: GJ/tCO2
    heat_requirement_heatpump = input.technology.loc["heat_requirement_heatpump", tech]#Unit: GJ/tCO2
    cop_heatpump = input.technology.loc["cop_heatpump", tech]#dimensionless
    net_electricity_requirement = (electricity_requirement + heat_requirement_heatpump/cop_heatpump) #Unit: GJ/tCO2
    net_heat_requirement = heat_requirement_gas #Unit: GJ/tCO2
    
    #adjust foak scale
    adj_foak_scale = foak_scale*(1-net_electricity_requirement*electricity_co2-
                                 net_heat_requirement*heat_co2)
    
    #save output for future use
    input.unlearned.adjsuted_foak_scale = adj_foak_scale
    
    return adj_foak_scale

