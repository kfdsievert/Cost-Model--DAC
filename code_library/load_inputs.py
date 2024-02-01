import os
from InputTemplate import InputTemplate
import pandas as pd

def load_inputs(filepath):
    '''
    LOAD_INPUTS: This function loads the input data specified in the provided file. 
    It loads the inputs into an object of class InputTemplate and returns this object.

    Parameters:
    filepath (string): File path of input file

    Returns:
    input (InputTemplate): Data structure containing the input tables

    Note: This function asserts that the provided file path is valid. If the file path is incorrect, 
          it will raise an AssertionError with a message indicating that the input file path is incorrect.
    '''

    # Assert that the file exists
    assert os.path.isfile(filepath), "The input file path is incorrect. Check for mistakes."

    # Create an InputTemplate object to store the inputs
    input = InputTemplate()

    # Get the names of all sheets in the Excel workbook
    xlsx = pd.read_excel(filepath, None)
    sheets = xlsx.keys()

    # Load Universal inputs.
    input.universal = pd.read_excel(filepath, "Universal_Inputs", index_col=0)

    # Load Technology inputs.
    input.technology = pd.read_excel(filepath, "Technology_Inputs", index_col=0)

    # Load EPC inputs
    input.epc_cost = pd.read_excel(filepath, "EPC_Cost", index_col=0, usecols="A:G")

    # Load Electricity Prices
    input.electricity = pd.read_excel(filepath, "Electricity_Prices")

    # Load Gas Prices
    input.heat = pd.read_excel(filepath, "Heat_Prices")

    # Load Monte Carlo Simulation Parameters, if available
    if 'Monte_Carlo' in sheets:
        input.monte_carlo = pd.read_excel(filepath, "Monte_Carlo")
    
    # Load Sensitivity Parameters, if available
    if 'Sensitivity' in sheets:
        input.sensitivity = pd.read_excel(filepath, 'Sensitivity')
        
    return input