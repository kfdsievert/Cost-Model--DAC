import numpy as np

class UnlearnedVars:
    '''
    UnlearnedVars: This class is a container to store all of the relevant input tables for unlearned variables.
    It makes passing the inputs into functions cleaner. All instance variables are initialized to "NA" or NaN until data is added to them.
    '''

    def __init__(self):
        self.adjusted_foak_scale = np.nan
        self.annual_labor_cost = np.nan
        self.electricity_price = np.nan
        self.heat_price = np.nan
        self.electricity_co2 = np.nan
        self.heat_co2 = np.nan
        self.epc_cost = np.nan
        self.total_plant_cost = np.nan
        self.component_costs = "NA"  
        self.lcoc = np.nan
        self.vom = np.nan
        self.fom = np.nan
        self.lcor = np.nan      

class LearnedVars:
    '''
    LearnedVars: This class is a container to store all of the relevant input tables for learned variables.
    It makes passing the inputs into functions cleaner. All instance variables are initialized to "NA" or NaN until data is added to them.
    '''

    def __init__(self):
        self.epc_cost = np.nan
        self.total_plant_cost = np.nan
        self.lcoc = np.nan
        self.vom = np.nan
        self.fom = np.nan
        self.lcor = np.nan
        self.component_costs = "NA"        

class InputTemplate:
    '''
    InputTemplate: This class is a container to store all of the relevant input tables.
    It makes passing the inputs into functions cleaner. All instance variables are initialized to "NA" until data is added to them.
    '''

    def __init__(self):
        self.universal = "NA"
        self.technology = "NA"
        self.epc_cost = "NA"
        self.electricity = "NA"
        self.heat = "NA"
        self.monte_carlo = "NA"
        self.sensitivity = "NA"
        self.learned = LearnedVars()
        self.unlearned = UnlearnedVars()