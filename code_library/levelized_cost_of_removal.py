from levelized_cost_of_capital import levelized_cost_of_capital
from variable_opex import variable_opex 
from fixed_opex import fixed_opex
from learning_factor import learning_factor
from adjusted_foak_scale import adjusted_foak_scale
import numpy as np

def levelized_cost_of_removal(input, tech, capacity):
    '''
    LEVELIZED_COST_OF_REMOVAL computes the levelized cost of carbon removal of
    each DAC technology given the parameters in the inputs.

    Parameters:
    input (InputTemplate): Standard input data structure
    tech (String): Technology name.
    capacity (double): Installed capacity of technology (tCO2/yr) for use
                       in the learning rate calculations.

    Returns:
    lcor (double): Levelized cost of carbon removal in $/(tCO2)

    Note: This function uses saved values if available. If the capacity is equal to the FOAK scale and the unlearned LCOR is available, 
          it returns the unlearned LCOR. If the capacity is not equal to the FOAK scale and the learned LCOR is available, 
          it returns the learned LCOR. Otherwise, it calculates the LCOR.
    '''

    # Get FOAK scale
    foak_scale = adjusted_foak_scale(input, tech)

    # Use saved value, if available
    if np.isclose(capacity, foak_scale) & ~np.isnan(input.unlearned.lcor):
        return input.unlearned.lcor
    elif ~np.isclose(capacity, foak_scale) & ~np.isnan(input.learned.lcor):
        return input.learned.lcor
    
    # Calculate cost components
    lcoc = levelized_cost_of_capital(input,tech, capacity)
    vom = variable_opex(input, tech, capacity)
    fom = fixed_opex(input, tech, capacity)

    # Compute LCOR
    lcor = lcoc  + fom + vom

    # Add LCOR learning rate
    lr_lcor = input.technology.loc["learning_rate_lcor", tech]
    lf_lcor = learning_factor(lr_lcor, foak_scale, capacity)
    lcor = lcor*lf_lcor
    
    # Store value for future use
    if np.isclose(capacity, foak_scale):
        input.unlearned.lcor = lcor
    else: 
        input.learned.lcor = lcor

    return lcor