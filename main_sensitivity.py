
### Add necessary paths -------------------------------------------------------
import sys
sys.path.insert(1,".\\code_library")#add path of lib folder

### Add necessary packages ----------------------------------------------------
import os
import numpy as np
import pandas as pd
import copy
from load_inputs import load_inputs #Function to load input data
from epc_cost import epc_cost #Function to compute the foak EPC cost
from total_plant_cost import total_plant_cost #Function to compute the TPC
from energy_price import energy_price #function to extract electricity prices
from variable_opex import variable_opex #function to compute variable opex
from fixed_opex import fixed_opex#function to compute fixed opex
from annual_labor_cost import annual_labor_cost
from levelized_cost_of_capital import levelized_cost_of_capital
from levelized_cost_of_removal import levelized_cost_of_removal
from monte_carlo import monte_carlo
from learning_factor import learning_factor
from summarize_output import summarize_output
from sensitivity import sensitivity
from adjusted_foak_scale import adjusted_foak_scale
from InputTemplate import *



# Manual Inputs ----------------------------------------------------------------

# File path and file name of input/output
input_filepath = ".\\input\\"
input_filename = "inputs_DACS_multi.xlsx"

output_filepath = ".\\output\\"
output_filename = "output_DACS_multi_sensitivity.xlsx"
writer = pd.ExcelWriter(output_filepath + output_filename, engine='xlsxwriter') #necesary  writting multiple sheets 

# List relevant technologies
technologies = ["LS", "SS", "CaO"]
#technologies = ["SS"]

# Set starting value (= "seed") of random number generator
np.random.seed(314) #This ensures that the results always stay the same

# Load inputs into a data structure --------------------------------------------
input_raw = load_inputs(input_filepath + input_filename) #load inputs. Returns an object of class Input.

# Calculate LCOR
for tech in technologies:

    #print technology to terminal
    print("Started technology " + tech)

    sensitivities = np.unique(input_raw.sensitivity.Set)
    #sensitivities= np.array([38,192])
    n_sensitivity = len(sensitivities)

    # Create output data table
    #create list of capacities which to output
    foak_scale = adjusted_foak_scale(input_raw, tech); 
    capacity_list = [foak_scale, 1.1*10**9] #capacities range from foak_scale to 1 Gt per year captured. 
    capacity_name = ["foak", "noak"]
    
    input_raw.learned = LearnedVars()
    input_raw.unlearned = UnlearnedVars()

    count = 0
    n_capacity = len(capacity_list)
    for c in range(0, n_capacity):
        
        #create capacity
        capacity = capacity_list[c] 

        #create output table
        output = pd.DataFrame(columns=['Scenario', 'Capacity'], index=range(n_sensitivity))

        for set in sensitivities:
            print("Progress: " + "{:.0%}".format(count/(n_sensitivity*n_capacity)), end = "\r")

            #update inputs with sensitivity runs
            input = copy.deepcopy(input_raw) #create a copy of original data to modify
            input, output = sensitivity(input, output, tech, set) 

            #reset saved variables
            input.learned = LearnedVars()
            input.unlearned =UnlearnedVars()

            #Fill output table--------------------------------------------------
            output.loc[set, "Capacity"]  = capacity #capacity
            output.loc[set, "LCOR"]  = levelized_cost_of_removal(input, tech, capacity) #compute lcor
            output.loc[set, "VOM"] = variable_opex(input,tech, capacity)
            output.loc[set, "FOM"] = fixed_opex(input,tech, capacity)
            output.loc[set, "LCOC"] = levelized_cost_of_capital(input,tech,capacity)
            # output.loc[output_row, "TPC"] = total_plant_cost(input,tech,capacity)
            # output.loc[output_row, "EPC"] = epc_cost(input,tech,capacity)

            count = count + 1
        # Save RAW Outputs ---------------------------------------------------------
        save_name = output_filepath + output_filename
        sheet_name =  tech + '_' + capacity_name[c]
        output.to_excel(writer, sheet_name=sheet_name, index = False)

writer.close()
print("Code Terminated Successfully")