### Add necessary paths -------------------------------------------------------
import sys
import os
current_dir = os.path.dirname(os.path.realpath(__file__))
lib_path = os.path.join(current_dir, "code_library")
# Add the library path to sys.path
sys.path.insert(1, lib_path)

### Add necessary packages ----------------------------------------------------
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
from adjusted_foak_scale import adjusted_foak_scale
from InputTemplate import *
from summarize_components import summarize_components

# Manual Inputs ----------------------------------------------------------------

# File path and file name of input/output
input_filepath = os.path.join(current_dir, "inputs/")
input_filename = "inputs_DACS_single.xlsx"

output_filepath = os.path.join(current_dir, "output/")
# Create output directory if it doesn't exist
os.makedirs(output_filepath, exist_ok=True)
output_filename = "output_DACS_single_5000.xlsx"
writer = pd.ExcelWriter(output_filepath + output_filename, engine='xlsxwriter') #necesary  writting multiple sheets 

# List relevant technologies
technologies = ["LS", "SS", "CaO"]
#technologies = ["SS"]

# Set number of monte carlo trials
n = 10

# Set number of capacities to output
n_capacity = 50

# Set starting value (= "seed") of random number generator
np.random.seed(314) #This ensures that the results always stay the same

# Load inputs into a data structure --------------------------------------------
input_raw = load_inputs(input_filepath + input_filename) #load inputs. Returns an object of class Input.

# Calculate LCOR
for tech in technologies:
    
    input = copy.deepcopy(input_raw) #create a copy of original data to modify

    #print technology to terminal
    print("Started technology " + tech)

    # Create output data table
    output = pd.DataFrame(columns=['Trial', 'Capacity'], index=range(n*n_capacity))
    output_row = 0 #counter to keep track of what row we are currently filling

    #create list of capacities which to output. Note: these are design capacities. For removal capacity, multiply by capacity factor
    foak_scale = adjusted_foak_scale(input, tech)
    upper = 1*10**9
    capacity_list = foak_scale*np.power(2,np.linspace(0,np.log(upper/foak_scale)/np.log(2), n_capacity, endpoint=True))

    
    for trial in range(0,n):

        print("Progress: " + "{:.0%}".format(trial/n), end = "\r")

        #reset the Unlearned Outputs
        input.unlearned = UnlearnedVars()

        #update inputs with monte carlo values
        input, output = monte_carlo(input, output, tech, output_row, output_row + n_capacity) 

        #compute LCOR for various capacity values
        for capacity in capacity_list:

            #reset Learned Outputs
            input.learned = LearnedVars()

            #Fill output table--------------------------------------------------
            output.loc[output_row, "Trial"]  = trial #trial number
            output.loc[output_row, "Capacity"]  = capacity #capacity
            output.loc[output_row, "LCOR"]  = levelized_cost_of_removal(input, tech, capacity) #compute lcor
            output.loc[output_row, "VOM"] = variable_opex(input,tech, capacity)
            output.loc[output_row, "FOM"] = fixed_opex(input,tech, capacity)
            output.loc[output_row, "LCOC"] = levelized_cost_of_capital(input,tech,capacity)
            # output.loc[output_row, "TPC"] = total_plant_cost(input,tech,capacity)
            # output.loc[output_row, "EPC"] = epc_cost(input,tech,capacity)
            #move on to next row in output

            if np.isclose(capacity, foak_scale):
                component_names = list(input.unlearned.component_costs.index)
                lr_names = [name + '_lr' for name in component_names]
                output.loc[output_row, component_names] = input.unlearned.component_costs['Learned_direct_materials_cost']
                output.loc[output_row, lr_names] = list(input.unlearned.component_costs['Learning_rate'])
                
            else: 
                component_names = list(input.learned.component_costs.index)
                lr_names = [name + '_lr' for name in component_names]
                output.loc[output_row, component_names] = input.learned.component_costs['Learned_direct_materials_cost']
                output.loc[output_row, lr_names] = list(input.learned.component_costs['Learning_rate'])

            output_row = output_row + 1

    # Save RAW Outputs ---------------------------------------------------------
    save_name = output_filepath + output_filename
    output.to_excel(writer, sheet_name=tech, index = False)

    # Save summarized outputs --------------------------------------------------
    summary = summarize_output(output) #calculate quantiles
    median_cost, median_lr = summarize_components(output, ['LCOR'] + component_names, lr_names)
    summary.to_excel(writer, sheet_name= (tech + "_summary"), index = True)
    median_cost.to_excel(writer, sheet_name= (tech + "_50pct_component_costs"), index = True)
    median_lr.to_excel(writer, sheet_name= (tech + "_50pct_component_lr"), index = True)




writer.close()
print("Code Terminated Successfully")