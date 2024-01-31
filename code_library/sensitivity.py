import numpy as np
import sys

def sensitivity(input, output, tech, set):
    #MONTE_CARLO upates the input paratmers to include randomly generated values
    #for monte carlo simulations. The distribution of the random parameters is 
    #specified in the input "monte_carlo" spreadsheet. The random parameters for
    #each Monte Carlo trial are stored in successive rows of the data table "output"
    #INPUTS
    #   input (InputTemplate) ... standard input data structure
    #   output (Pandas Data Frame) ... output table
    #   tech (string) ...technology of interest
    #   s (integer) ... row number of change in sensitivity table to be applied.
    #                   The outputs will be saved in the same row. 
    #   
    #
    #OUTPUT
    #   input (InputTemplate) ... standard input data structure with randomly g
    #            generated inputs following the distributions specified for the 
    #            monte carlo analysis.
    #   output (Pandas Data Frame) ... data table in which to store the randomly
    #            generated paramters. The values are stored to make it easier to
    #            analyze simulation results at the end.

    data = input.sensitivity.copy()
    data = data.loc[data.Set == set]
    data = data.reset_index()

    for s in range(0,len(data)):
        sheet = data.loc[s, "Sheet"] #sheet which to modify
        row = data.loc[s, "Row"] #row which to modify (=variable name)
        column = data.loc[s, "Column"] #row which to modify (=variable name)
        change = data.loc[s, "Desired_change"]#column which to modify
        scenario_name = data.loc[s, "Scenario_name"]

        #when necessary, make column be the appropriate technology name
        if column == 'tech':
            column = tech
            
        #skip the row if it relates to a technology parameter for a different technology
        #than theone currently under consideration.
        # if ((sheet == 'technology') and (column != tech)) or\
        #     ((sheet == 'epc_cost') and (tech not in row)):
        #     continue

        match change:

            case "new value": #if replacing with new value

                #update input value
                value = data.loc[s, "Value"]
                getattr(input, sheet).loc[row, column] = value 

                #save value to output   
                output.loc[set, "Scenario"] = scenario_name
                output.loc[set, "Value_"+str(s)] = value

            case "pct_change": #if replacing with new value
                #update input value
                pct = data.loc[s, "Value"]
                old_value = getattr(input, sheet).loc[row, column]
                new_value = old_value*(1+pct)
                getattr(input, sheet).loc[row, column] = new_value

                #save value to output   
                output.loc[set, "Scenario"] = scenario_name
                output.loc[set, "Value_"+str(s)] = pct

            case _:            
                raise Exception("Sensitivity type {change} not defined".format(change = change))

    return input, output


        


    

    