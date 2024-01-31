from total_plant_cost import total_plant_cost
from energy_price import energy_price
from annual_labor_cost import annual_labor_cost
from learning_factor import learning_factor
from adjusted_foak_scale import adjusted_foak_scale
import numpy as np
import pandas as pd

def levelized_cost_of_capital(input, tech, capacity):
    #LCOC computes the levelized cost of capital of
    #each DAC technology given the parameters in the inputs.
    #INPUTS
    #   input (InputTemplate) ... standard input data structure
    #   tech (String) ... technology name.
    #
    #OUTPUT
    #   lcoc (double) ... levelized cost of capital in $/(tCO2)

    #get foak scale
    foak_scale = adjusted_foak_scale(input, tech) #Unit: tCO2

    #Use saved value, if available
    if np.isclose(capacity, foak_scale) & ~np.isnan(input.unlearned.lcoc):
        return input.unlearned.lcoc
    elif ~np.isclose(capacity, foak_scale) & ~np.isnan(input.learned.lcoc):
        return input.learned.lcoc
   
    # extract relevant data from inputs
    owners_cost_fraction = input.universal.loc["owners_cost", "Value"]#Unit: dimensionless
    spare_parts_fraction = input.universal.loc["spare_parts_cost", "Value"]#Unit: dimensionless
    startup_capital_fraction = input.universal.loc["startup_capital", "Value"]#Unit: dimensionless
    startup_labor_fraction = input.universal.loc["startup_labor", "Value"]#Unit: dimensionless
    startup_fuel_fraction = input.universal.loc["startup_fuel", "Value"]#Unit: dimensionless
    startup_chemical_fraction = input.universal.loc["startup_chemicals", "Value"]#Unit: dimensionless
    gas_requirement = input.technology.loc["heat_requirement_gas", tech]#Unit: GJ/tCO2
    chemicals_cost =  input.technology.loc["chemicals_cost", tech]#Unit: $/tCO2
    discount_rate = input.universal.loc["discount_rate", "Value"]#Unit: dimensionless
    plant_life = input.universal.loc["plant_life", "Value"]#Unit: years
    capacity_factor = input.technology.loc["plant_capacity_factor", tech]#Unit: dimensionless #tech-specific

    # calculate the total plant cost
    tpc = total_plant_cost(input,tech, capacity)
    tpc_unlearned = total_plant_cost(input, tech, foak_scale)

    # get energy prices
    gas_price = energy_price(input)[1]

    #calculate additional missing costs
    owners_cost = owners_cost_fraction * tpc_unlearned
    spare_parts_cost = spare_parts_fraction*tpc_unlearned
    startup_capital = startup_capital_fraction*tpc_unlearned
    startup_labor = annual_labor_cost(input, tech)*startup_labor_fraction
    startup_fuel = gas_price*gas_requirement*foak_scale*startup_fuel_fraction
    startup_chemicals = startup_chemical_fraction*chemicals_cost*foak_scale

    #start-up learning rate
    lr_startup = input.technology.loc["learning_rate_startup_cost", tech]
    lf_startup = learning_factor(lr_startup, foak_scale, capacity)


    #total overnight cost (=total capital requirement)
    tcr = tpc + (owners_cost + spare_parts_cost + startup_capital +\
        + startup_labor + startup_fuel + startup_chemicals)*lf_startup
    
    #compute capital recovery factor
    crf = discount_rate*(1+discount_rate)**plant_life/((1+discount_rate)**plant_life-1)

    #compute annualized total overnight cost
    annualized_overnight = tcr*crf

    #compute the lcoc
    lcoc = annualized_overnight/(foak_scale*capacity_factor)

    #save value for future use
    index = ['owners_cost_' + tech, 'spare_parts_cost_' + tech, 'startup_capital_' + tech, 'startup_labor_' + tech, 'startup_fuel_' + tech, 'startup_chemicals_' + tech ]
    component_costs = {'Learned_direct_materials_cost': [owners_cost *lf_startup, spare_parts_cost*lf_startup, startup_capital*lf_startup, startup_labor*lf_startup, startup_fuel*lf_startup, startup_chemicals*lf_startup], 
                       'Learning_rate':                 [lr_startup,  lr_startup, lr_startup, lr_startup, lr_startup, lr_startup]}
    component_costs = pd.DataFrame(component_costs, index = index)

    if np.isclose(capacity, foak_scale):
        input.unlearned.lcoc = lcoc
        input.unlearned.component_costs = pd.concat([input.unlearned.component_costs, component_costs])
        input.unlearned.component_costs['Learned_direct_materials_cost'] = input.unlearned.component_costs['Learned_direct_materials_cost'] *crf/(foak_scale*capacity_factor) #unit: $/ton captured
    else:
        input.learned.lcoc = lcoc
        input.learned.component_costs = pd.concat([input.learned.component_costs, component_costs])
        input.learned.component_costs['Learned_direct_materials_cost'] = input.learned.component_costs['Learned_direct_materials_cost'] *crf/(foak_scale*capacity_factor) #unit: $/ton captured

    return lcoc