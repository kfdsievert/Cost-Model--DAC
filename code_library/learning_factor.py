import numpy as np

def learning_factor(learning_rate, foak_scale, capacity):
    '''
    LEARNING_FACTOR: This function computes the cost multiplier (Learning Factor) associated
    with cost reductions from learning-by-doing. The learning rate is used to calculate the learning exponent 'b', 
    which is then used to calculate the learning factor. This learning factor serves as a cost multiplier associated with the learning rate.
    It is multiplied with "first-of-a-kind" (FOAK) costs in order to get "nth-of-a-kind" costs.

    Parameters:
    learning_rate (double or array): The learning rate of the technology component, 
                         expressed as a fraction (e.g 0.05 for 5%).
    foak_scale (double): The technology FOAK scale in tCO2/yr.
    capacity (double): The current installed "nth-of-a-kind" capacity of interest in the model.

    Returns:
    lf (double or array): The learning factor which can be multiplied by FOAK costs
                  to get nth-of-a-kind costs. The size of the output matches
                  the size of the "learning_rate" input.

    Note: If capacity and FOAK scale are the same, then the learning factor equals 1. 
        This is necessary to calculate initial cost without learning.
    '''

    x = capacity/foak_scale # ratio of capacity to FOAK scale
    b = -np.log((1-learning_rate))/np.log(2) # learning exponent

    lf = np.power(x, -b) # compute learning factor as x^b

    return lf