from total_plant_cost import total_plant_cost
from adjusted_foak_scale import adjusted_foak_scale
import numpy as np

def annual_labor_cost(input, tech):
     #ANNUAL_LABOR_COST computes the annual labor cost of
    #each DAC technology given the parameters in the inputs.
    #Note that it does not apply any learning rates. It is thus the labor
    #cost of the foak_scale.
    #INPUTS
    #   input (InputTemplate) ... standard input data structure
    #   tech (String) ... technology name.
    #
    #OUTPUT
    #   annual_labor_cost (double) ... annual labor cost $/(tCO2*yr)
   
   #use saved value, if avaialble
    if ~np.isnan(input.unlearned.annual_labor_cost):
        return input.unlearned.annual_labor_cost

    # Load labor inputs
    operator_salary = input.universal.loc["operator_salary", "Value"]
    productivity_factor = input.universal.loc["productivity_factor", "Value"]
    employees = input.technology.loc["employees", tech]
    maintenance_factor = input.universal.loc["maintenance_factor", "Value"]
    indirect_labour_factor = input.universal.loc["indirect_labour_factor", "Value"]
    foak_scale = adjusted_foak_scale(input, tech)


    # compute total plant cost
    tpc_unlearned = total_plant_cost(input, tech, foak_scale)

    # Calculate various compoenents of labor cost
    direct_labor_cost = employees*operator_salary*productivity_factor
    maintenance_cost = (maintenance_factor*tpc_unlearned)
    indirect_labor_cost = indirect_labour_factor*\
        (direct_labor_cost + maintenance_cost)
    
    # Aggregate labor components to annual labor cost
    annual_labor_cost = direct_labor_cost + indirect_labor_cost +\
        maintenance_cost
    
    #save value for future use
    input.unlearned.annual_labor_cost = annual_labor_cost
    
    return annual_labor_cost