from energy_price import energy_price
from learning_factor import learning_factor
from adjusted_foak_scale import adjusted_foak_scale
import numpy as np
import pandas as pd

def variable_opex(input, tech, capacity):
    '''
    VARIABLE_OPEX: This function computes the variable operating costs of
    each Direct Air Capture (DAC) technology given the parameters in the inputs.

    Parameters:
    input (InputTemplate): Standard input data structure
    tech (String): Technology name

    Returns:
    vom (double): Variable operating and maintenance costs in $/tCO2
    '''
    #get foak scale
    foak_scale = adjusted_foak_scale(input, tech)
    
    #Use saved value, if available
    if np.isclose(capacity, foak_scale) & ~np.isnan(input.unlearned.vom):
        return input.unlearned.vom
    elif ~np.isclose(capacity, foak_scale) & ~np.isnan(input.learned.vom):
        return input.learned.vom
    

    ## Get inputs to compute fuel costs 
    electricity_price, gas_price = energy_price(input)[0:2] #Unit: $/GJ
    gasoline_price = input.universal.loc["gasoline_price", "Value"]#Unit: $/GJ
    water_price = input.universal.loc["water_cost", "Value"]#Unit: $/m3
    chemicals_cost =  input.technology.loc["chemicals_cost", tech]#Unit: $/tCO2

    ## Extract relevant technology fuel requirements
    electricity_requirement = input.technology.loc["electricity_requirement", tech]#Unit: GJ/tCO2
    heat_requirement_gas = input.technology.loc["heat_requirement_gas", tech]#Unit: GJ/tCO2
    heat_requirement_heatpump = input.technology.loc["heat_requirement_heatpump", tech]#Unit: GJ/tCO2
    water_requirement = input.technology.loc["water_requirement", tech]#Unit: m3/tCO2
    gasoline_requirement = input.technology.loc["gasoline_requirement", tech]#Unit: GJ/tCO2
    #temperature_heat = input.technology.loc["temperature_heat", tech]#Unit:degC #not required in case temperature already included in heat requirement
    min_electricity = input.technology.loc["min_electricity_requirement",tech]#Unit GJ/tCO2
    min_heat_gas = input.technology.loc["min_heat_requirement_gas",tech]#Unit GJ/tCO2
    min_heat_heatpump = input.technology.loc["min_heat_requirement_heatpump",tech]#Unit GJ/tCO2

    ## Storage paramters
    transport_cost_perkm = input.universal.loc["transport_cost", "Value"]#Unit: $/tCO2/km
    transport_distance = input.universal.loc["transport_distance", "Value"]#Unit: km
    ratio_co2_compressed_to_captured = input.technology.loc["ratio_co2_compressed_to_captured", tech]#dimensionless
    storage_cost = input.universal.loc["storage_cost", "Value"]#unit: $/tCO2
    
    ## Other Parameters
    co2_purity = input.technology.loc["co2_purity", tech]#dimensionless
    cop_heatpump = input.technology.loc["cop_heatpump", tech]#dimensionless
    #capacity_factor = input.technology.loc["plant_capacity_factor", tech]#Unit: dimensionless #CHANGED THIS TECHNOLOGY INSTEAD OF UNIVERSAL; tech instead of value

    # Use learning rate to create learning factor
    lr_opex = input.universal.loc["learning_rate_opex", "Value"] #retrieves learning rate for variable OPEX from input data 
    lf_opex = learning_factor(lr_opex, foak_scale, capacity) #calculation of learning factor for variable OPEX

    ## Calculate energy requirement with learning rates and compare to thermodynamic minimum so that energy use does not go below that
    electricity_requirement = max(electricity_requirement*lf_opex, min_electricity)
    heat_requirement_gas = max(heat_requirement_gas*lf_opex, min_heat_gas)
    heat_requirement_heatpump = max(heat_requirement_heatpump*lf_opex, min_heat_heatpump)

    ## Calculate Variable Costs
    electricity_cost = (electricity_requirement+\
                         heat_requirement_heatpump/cop_heatpump) *\
                         electricity_price/co2_purity #Unit: $/tCO2
    gas_cost = heat_requirement_gas*gas_price#Unit: $/tCO2
    gasoline_cost = gasoline_requirement*gasoline_price*lf_opex#Unit: $/tCO2
    water_cost = water_requirement*water_price*lf_opex#Unit: $/tCO2
    transport_cost = transport_cost_perkm*transport_distance*ratio_co2_compressed_to_captured*lf_opex#$/tCO2
    chemicals_cost = chemicals_cost*lf_opex
    storage_cost = storage_cost*lf_opex
    
    # Compute final variable cost
    vom = (electricity_cost + gas_cost + gasoline_cost + water_cost + \
        chemicals_cost + transport_cost + storage_cost)#*(capacity_factor/0.9)#Unit: $/tCO2
    
    # Save value for future use
    index = ['vom_' + tech]
    component_costs = {'Learned_direct_materials_cost': [vom], 
                       'Learning_rate':                 [lr_opex]}
    component_costs = pd.DataFrame(component_costs, index = index)

    # Function checks whether capacity equals foak_scale. If not, function returns learned vom value
    if np.isclose(capacity, foak_scale):
        input.unlearned.vom = vom
        input.unlearned.component_costs = pd.concat([input.unlearned.component_costs, component_costs])
    else:
        input.learned.vom = vom
        input.learned.component_costs = pd.concat([input.learned.component_costs, component_costs])
    return vom


