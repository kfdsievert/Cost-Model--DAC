import numpy as np
from learning_factor import learning_factor
from adjusted_foak_scale import adjusted_foak_scale

def epc_cost(input, tech, capacity):
    '''
    EPC_COST: This function computes the initial engineering, procurement, and construction (EPC) cost [$] for a technology.  

    Parameters:
    input (InputTemplate): Standard input data structure.
    tech (string): Technology for which to calculate the EPC costs.
    capacity (float): The capacity of the technology.

    Returns:
    cost (double): EPC cost in $.
    '''

    # Copy epc_cost input to new variable
    epc_cost = input.epc_cost.copy()

    # Filter EPC_Cost to include only rows of the relevant technology
    epc_cost = epc_cost[epc_cost['Technology'] == tech]

    # Extract FOAK scale and initial scale
    unadjusted_foak_scale = input.technology.loc['foak_scale', tech]
    initial_scale = input.technology.loc['initial_scale', tech]

    # Extract epc_factor
    epc_factor = input.universal.loc['epc_factor', 'Value']

    # Scale technology costs - This is only used if initial scale deviates from FOAK scale
    epc_cost['Scaled_direct_materials_cost'] = epc_cost['Direct_materials_cost']*\
        np.power(unadjusted_foak_scale/initial_scale, epc_cost['Exponent'])

    # Apply learning rates to direct materials cost
    learning_rate = epc_cost['Learning_rate']
    foak_scale = adjusted_foak_scale(input, tech)
    lf = learning_factor(learning_rate, foak_scale, capacity)
    epc_cost['Learned_direct_materials_cost'] = epc_cost['Scaled_direct_materials_cost']*lf

    # Sum to get cost of system
    cost = epc_cost['Learned_direct_materials_cost'].sum()

    # Apply EPC cost adder
    lr_epc = input.technology.loc["learning_rate_epc", tech]
    lf_epc = learning_factor(lr_epc, foak_scale, capacity)
    unlearned_cost = epc_cost['Scaled_direct_materials_cost'].sum()
    epc_adder = unlearned_cost*epc_factor*lf_epc

    # Save component costs for future use and for component-detailed output
    component_costs = epc_cost[['Learned_direct_materials_cost', 'Learning_rate']].copy()
    component_costs.loc['epc_adder_' + tech] = [epc_adder, lr_epc]
    component_costs['Learned_direct_materials_cost'] =  component_costs['Learned_direct_materials_cost']*10**6

    if np.isclose(capacity, foak_scale):
        input.unlearned.component_costs = component_costs
    else:
        input.learned.component_costs = component_costs

    # Scale by epc_factor to calculate the total initial EPC cost [$]
    cost = cost + epc_adder

    return cost