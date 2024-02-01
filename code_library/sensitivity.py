import numpy as np
import sys

def sensitivity(input, output, tech, set):
    '''
    SENSITIVITY: This function updates the input parameters to include changes specified
    for sensitivity analysis. The changes are specified in the input "sensitivity" spreadsheet.
    The parameters for each sensitivity scenario are stored in successive rows of the data table "output".

    Parameters:
    input (InputTemplate): Standard input data structure
    output (Pandas DataFrame): Output table
    tech (string): Technology of interest
    set (integer): Row number of change in sensitivity table to be applied.
                   The outputs will be saved in the same row. 

    Returns:
    input (InputTemplate): Standard input data structure with updated inputs 
                           following the changes specified for the sensitivity analysis.
    output (Pandas DataFrame): Data table in which to store the changed parameters.
                               The values are stored to make it easier to analyze 
                               simulation results at the end.

    Note: This function supports three types of changes: "new value", "pct_change", and "add".
          For "new value", it replaces the original value with a new one.
          For "pct_change", it modifies the original value by a certain percentage.
          For "add", it adds a certain value to the original value.
    '''

    data = input.sensitivity.copy()
    data = data.loc[data.Set == set]
    data = data.reset_index()

    for s in range(0,len(data)):
        sheet = data.loc[s, "Sheet"] # Sheet which to modify
        row = data.loc[s, "Row"] # Row which to modify (=variable name)
        column = data.loc[s, "Column"] # Row which to modify (=variable name)
        change = data.loc[s, "Desired_change"]# Column which to modify
        scenario_name = data.loc[s, "Scenario_name"]

        # When necessary, make column be the appropriate technology name
        if column == 'tech':
            column = tech
            
        # Skip the row if it relates to a technology parameter for a different technology
        # than theone currently under consideration.
        # If ((sheet == 'technology') and (column != tech)) or\
        #     ((sheet == 'epc_cost') and (tech not in row)):
        #     continue

        match change:

            case "new value": # If replacing with new value

                # Update input value
                value = data.loc[s, "Value"]
                getattr(input, sheet).loc[row, column] = value 

                # Save value to output   
                output.loc[set, "Scenario"] = scenario_name
                output.loc[set, "Value_"+str(s)] = value

            case "pct_change": # If replacing with new value
                # Update input value
                pct = data.loc[s, "Value"]
                old_value = getattr(input, sheet).loc[row, column]
                new_value = old_value*(1+pct)
                getattr(input, sheet).loc[row, column] = new_value

                # Save value to output   
                output.loc[set, "Scenario"] = scenario_name
                output.loc[set, "Value_"+str(s)] = pct

            case _:            
                raise Exception("Sensitivity type {change} not defined".format(change = change))

    return input, output


        


    

    