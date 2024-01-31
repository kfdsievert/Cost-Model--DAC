import numpy as np #used for numerical operations in Python
from learning_factor import learning_factor #import learning rates
from adjusted_foak_scale import adjusted_foak_scale #import adjusted foak scale 

def epc_cost(input, tech, capacity):
    #FOAK_COSTS This function computes the initial engineering, procurement, and construction cost [$] for a technology.  
    #
    #INPUTS:
    #   input (class InputTemplate) ... the input data structure
    #   tech (string) ... technology for which to calculate the foak costs
    #OUTPUT:
    #   epc_cost (double) ... epc cost in $


    ## Save epc_cost input to new variable
    epc_cost = input.epc_cost.copy() 

    ## Filter EPC_Cost to include only rows of the relevant technology
    epc_cost = epc_cost[epc_cost['Technology'] == tech]

    ## Extract foak scale and initial scale
    unadjusted_foak_scale = input.technology.loc['foak_scale', tech]
    initial_scale = input.technology.loc['initial_scale', tech]
    
    ## Extract epc_factor
    epc_factor = input.universal.loc['epc_factor', 'Value']

    ###########
    ## Scale technology costs - This is only used if initial scale deviates from foak scale - e.g., 960 tCO2/year versus 4000 tCO2/year
    #If initial and foak scale are same inputs, then epc_cost['Direct_materials_cost'] is the same as epc_cost['Scaled_direct_materials_cost'] 
    epc_cost['Scaled_direct_materials_cost'] = epc_cost['Direct_materials_cost']*\
        np.power(unadjusted_foak_scale/initial_scale, epc_cost['Exponent'])
    ###########

    ## Apply learning rates to direct materials cost
    learning_rate = epc_cost['Learning_rate'] #learning rates for each component taken from inputs
    foak_scale = adjusted_foak_scale(input, tech) #plant scale taking grey emissions into account
    lf = learning_factor(learning_rate, foak_scale, capacity) #learning factor for each component
    epc_cost['Learned_direct_materials_cost'] = epc_cost['Scaled_direct_materials_cost']*lf

    ##for comparison with excel spreadsheet only
    # discount_rate = input.universal.loc["discount_rate", "Value"]#Unit: dimensionless
    # plant_life = input.universal.loc["plant_life", "Value"]#Unit: years
    # crf = discount_rate*(1+discount_rate)**plant_life/((1+discount_rate)**plant_life-1)
    # epc_cost["Learned_direct_materials_cost"] * crf*10**6/(foak_scale*0.9)

    ##Sum to get cost of system.
    cost = epc_cost['Learned_direct_materials_cost'].sum()

    ## Apply EPC cost adder.
    lr_epc = input.technology.loc["learning_rate_epc", tech] #taken from inputs tab Monte_Carlo
    lf_epc = learning_factor(lr_epc, foak_scale, capacity)
    unlearned_cost = epc_cost['Scaled_direct_materials_cost'].sum() 
    epc_adder = unlearned_cost*epc_factor*lf_epc #% of sum of total direct materials cost to be added to direct materials cost
    
    ## Save component costs for future use and for component-detailed output
    component_costs = epc_cost[['Learned_direct_materials_cost', 'Learning_rate']].copy()
    component_costs.loc['epc_adder_' + tech] = [epc_adder, lr_epc]
    component_costs['Learned_direct_materials_cost'] =  component_costs['Learned_direct_materials_cost']*10**6 #change units to dollars

    if np.isclose(capacity, foak_scale):
        input.unlearned.component_costs = component_costs
    else:
        input.learned.component_costs = component_costs


    ##Scale by epc_factor to calculate the total initial epc cost [$]
    cost = cost + epc_adder
    
    return cost



