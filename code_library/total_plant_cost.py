from epc_cost import epc_cost
from learning_factor import learning_factor
from adjusted_foak_scale import adjusted_foak_scale
import numpy as np
import pandas as pd

def total_plant_cost(input, tech, capacity):
    #TOTAL PLANT COST This file computes the total plant cost. The total plant 
    #cost is the Engineering, Procurement, Construction scaled by project and
    #process contingency factors.
    #
    #INPUTS:
    #   input (InputTemplate) ... standard input data structure
    #   tech (String) ... technology for which to calculate TPC
    #OUTPUT:
    #   total_plant_cost (double) ... total plant cost in $

    #get foak scale
    foak_scale = adjusted_foak_scale(input, tech)

    #use saved results if available.
    #if capacity is same as foak_scale, this function returns unlearned total plant cost --> this happens when the initial cost for the initial plant size are calculated
    if np.isclose(capacity, foak_scale) & ~np.isnan(input.unlearned.total_plant_cost):
        return input.unlearned.total_plant_cost
    elif ~np.isclose(capacity, foak_scale) & ~np.isnan(input.learned.total_plant_cost):
        return input.learned.total_plant_cost
    
    
    #compute epc_cost
    epc = epc_cost(input, tech, capacity)
    epc_unlearned = epc_cost(input,tech,foak_scale) #this shows that the epc cost without learning factor applied are used to calculate initial TPC cost
    
    #extract learning rates for process and prject contingency
    lr_process_contingency = input.technology.loc["learning_rate_process_contingency", tech]
    lr_project_contingency = input.technology.loc["learning_rate_project_contingency", tech]

    #compute learning factors for process and project contingency
    lf_process_contingency = learning_factor(lr_process_contingency, foak_scale, capacity)
    lf_project_contingency = learning_factor(lr_project_contingency, foak_scale, capacity)

    #get project and process contingency factors from the data and calculate
    #process and project contingency factors
    project_contingency = \
        input.universal.loc["project_contingency_factor", "Value"]*epc_unlearned*lf_project_contingency
    
    process_contingency = \
        input.technology.loc["process_contingency_factor", tech]*epc_unlearned*lf_process_contingency
    
    #return total plant cost as the output
    tpc = 10**6 * (epc + project_contingency + process_contingency)

    ##for comparison with Excel spreadsheet only
    # discount_rate = input.universal.loc["discount_rate", "Value"]#Unit: dimensionless
    # plant_life = input.universal.loc["plant_life", "Value"]#Unit: years
    # crf = discount_rate*(1+discount_rate)**plant_life/((1+discount_rate)**plant_life-1)
    # tpc * crf/(foak_scale*0.9)
    
    #save results for future use
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
    

