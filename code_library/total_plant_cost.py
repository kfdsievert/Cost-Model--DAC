from epc_cost import epc_cost
from learning_factor import learning_factor
from adjusted_foak_scale import adjusted_foak_scale
import numpy as np
import pandas as pd

def total_plant_cost(input, tech, capacity):
    '''
    TOTAL_PLANT_COST: This function computes the total plant cost. The total plant 
    cost is the Engineering, Procurement, Construction (EPC) cost scaled by project and
    process contingency factors.

    Parameters:
    input (InputTemplate): Standard input data structure
    tech (String): Technology for which to calculate Total Plant Cost (TPC)
    capacity (float): Capacity of the plant

    Returns:
    tpc (double): Total plant cost in $

    Note: The function first checks if the capacity is the same as the First of a Kind (FOAK) scale.
    If it is, and if the unlearned total plant cost is not NaN, it returns the unlearned total plant cost.
    If the capacity is not the same as the FOAK scale, and if the learned total plant cost is not NaN, 
    it returns the learned total plant cost. If neither of these conditions are met, it computes the total plant cost.
    '''

    # Get FOAK scale
    foak_scale = adjusted_foak_scale(input, tech)

    # Use saved results if available.
    # If capacity is same as foak_scale, this function returns unlearned total plant cost --> this happens when the initial cost for the initial plant size are calculated
    if np.isclose(capacity, foak_scale) & ~np.isnan(input.unlearned.total_plant_cost):
        return input.unlearned.total_plant_cost
    elif ~np.isclose(capacity, foak_scale) & ~np.isnan(input.learned.total_plant_cost):
        return input.learned.total_plant_cost
    
    # Compute EPC cost
    epc = epc_cost(input, tech, capacity)
    epc_unlearned = epc_cost(input,tech,foak_scale) # This shows that the EPC cost without learning factor applied are used to calculate initial TPC cost
    
    # Extract learning rates for process and project contingency
    lr_process_contingency = input.technology.loc["learning_rate_process_contingency", tech]
    lr_project_contingency = input.technology.loc["learning_rate_project_contingency", tech]

    # Compute learning factors for process and project contingency
    lf_process_contingency = learning_factor(lr_process_contingency, foak_scale, capacity)
    lf_project_contingency = learning_factor(lr_project_contingency, foak_scale, capacity)

    # Get project and process contingency factors from the data and calculate
    # process and project contingency factors
    project_contingency = \
        input.universal.loc["project_contingency_factor", "Value"]*epc_unlearned*lf_project_contingency
    
    process_contingency = \
        input.technology.loc["process_contingency_factor", tech]*epc_unlearned*lf_process_contingency
    
    # Return total plant cost as the output
    tpc = 10**6 * (epc + project_contingency + process_contingency)
    
    # Save results for future use
    index = ['project_contingency_' + tech, 'process_contingency_' + tech]
    component_costs = {'Learned_direct_materials_cost': [project_contingency*10**6, process_contingency*10**6], 
                       'Learning_rate':                 [lr_project_contingency,  lr_process_contingency]}
    component_costs = pd.DataFrame(component_costs, index = index)

    if np.isclose(capacity, foak_scale):
        input.unlearned.total_plant_cost = tpc
        input.unlearned.component_costs = pd.concat([input.unlearned.component_costs, component_costs])

    else:
        input.learned.total_plant_cost = tpc
        input.learned.component_costs = pd.concat([input.learned.component_costs, component_costs])
    return tpc