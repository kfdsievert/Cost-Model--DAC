from total_plant_cost import total_plant_cost
from annual_labor_cost import annual_labor_cost
from learning_factor import learning_factor
from adjusted_foak_scale import adjusted_foak_scale
import numpy as np
import pandas as pd

def fixed_opex(input, tech, capacity):
    #FIXED_OPEX computes the fixed operating and maintenance costs of
    #each DAC technology given the parameters in the inputs.
    #INPUTS
    #   input (InputTemplate) ... standard input data structure
    #   tech (String) ... technology name.
    #
    #OUTPUT
    #   fom (double) ... fixed operating and maintenance costs in $/(tCO2*yr)

    #get foak scale
    foak_scale = adjusted_foak_scale(input, tech)
    
    #Use saved value, if available
    if np.isclose(capacity, foak_scale) & ~np.isnan(input.unlearned.fom):
        return input.unlearned.fom
    elif ~np.isclose(capacity, foak_scale) & ~np.isnan(input.learned.fom):
        return input.learned.fom
    
    # Extract relevant parameters
    insurance_factor = input.universal.loc["insurance_factor", "Value"]
    tax_fees_factor = input.universal.loc["taxes_fees_factor", "Value"]
    capacity_factor = input.technology.loc["plant_capacity_factor", tech]#Unit: dimensionless 


    # Compute total plant cost
    tpc_unlearned = total_plant_cost(input, tech, foak_scale)
    
    # Compute components of fixed cost
    labor_cost = annual_labor_cost(input, tech)
    insurance_cost = insurance_factor * tpc_unlearned
    tax_fees_cost = tax_fees_factor * tpc_unlearned

    # Compute final fom
    fom = (labor_cost + insurance_cost + tax_fees_cost)/(foak_scale*capacity_factor)

    #get learning rates for the system
    lr_system = input.technology.loc["learning_rate_system", tech]

    #compute learning factors
    lf_system = learning_factor(lr_system, foak_scale, capacity)
    
    #add learning to fixed cost
    fom = fom*lf_system

    #save results for future use
    index = ['fom_' + tech]
    component_costs = {'Learned_direct_materials_cost': [fom], 
                       'Learning_rate':                 [lr_system]}
    component_costs = pd.DataFrame(component_costs, index = index)

    if np.isclose(capacity, foak_scale):
        input.unlearned.fom = fom
        input.unlearned.component_costs = pd.concat([input.unlearned.component_costs, component_costs])
    else:
        input.learned.fom = fom
        input.learned.component_costs = pd.concat([input.learned.component_costs, component_costs])
    return fom

