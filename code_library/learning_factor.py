import numpy as np

def learning_factor(learning_rate, faok_scale, capacity):
    #LEARNING_FACTOR computes the cost multiplier (= Learning Factor) associated
    #with cost reductions from learning-by-doing. 
    #Learning rate is used to calculate b and b is then used to calculate learning factor, which serves as cost multiplier associated with learning rate
    # multiplied with "initial" costs in order to get "nth-of-a-kind" costs.
    # 
    # INPUT:
    # learning_rate (double or array) 
    #                        ... the learning rate of the technology component, 
    #                            expressed as a fraction (e.g 0.05 for 5%)
    # foak_scale (double)    ... the technology foak scale in tCO2/yr
    # capacity (double)      ... the current installed "nth-of-a-kind" capacity of
    #                            interest in the model.
    #  
    # OUTPUT:
    # lf (double or array) 
    #             ... the learning factor which can be multiplied by foak coasts
    #                 to get nth-of-a-kind costs. The size of the output matches
    #                 the size of the "learning_rate" input.
    #
    #Note, if capacity and foak scale are the same, then the learning factor equals 1 which is necessary to calculate initial cost without learning

    x = capacity/faok_scale #ratio of capacity to foak scale
    b = -np.log((1-learning_rate))/np.log(2) #learning exponent

    lf = np.power(x, -b) #compute learning factor as x^b

    return lf