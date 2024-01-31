from levelized_cost_of_capital import levelized_cost_of_capital
from variable_opex import variable_opex 
from fixed_opex import fixed_opex
from learning_factor import learning_factor
from adjusted_foak_scale import adjusted_foak_scale
import numpy as np

def levelized_cost_of_removal(input, tech, capacity):
    #LCOR computes the levelized cost of carbon removal of
    #each DAC technology given the parameters in the inputs.
    #INPUTS
    #   input (InputTemplate) ... standard input data structure
    #   tech (String)     ... technology name.
    #   capacity (double) ... installed capacity of technology (tCO2/yr) for use
    #                         in the learning rate calculations.
    #
    #OUTPUT
    #   lcor (double) ... levelized cost of carbon removal in $/(tCO2)

    #get foak scale
    foak_scale = adjusted_foak_scale(input, tech)

    #Use saved value, if available
    if np.isclose(capacity, foak_scale) & ~np.isnan(input.unlearned.lcor):
        return input.unlearned.lcor
    elif ~np.isclose(capacity, foak_scale) & ~np.isnan(input.learned.lcor):
        return input.learned.lcor
    
    #calculate cost components
    lcoc = levelized_cost_of_capital(input,tech, capacity)
    vom = variable_opex(input, tech, capacity)
    fom = fixed_opex(input, tech, capacity)

    #compute lcor
    lcor = lcoc  + fom + vom

    #add lcor_learning_rate
    lr_lcor = input.technology.loc["learning_rate_lcor", tech]
    lf_lcor = learning_factor(lr_lcor, foak_scale, capacity)
    lcor = lcor*lf_lcor
    
    #store value for future use
    if np.isclose(capacity, foak_scale):
        input.unlearned.lcor = lcor
    else: 
        input.learned.lcor = lcor

    return lcor