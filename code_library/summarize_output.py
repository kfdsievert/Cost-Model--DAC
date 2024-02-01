import pandas as pd
import numpy as np

def summarize_output(output):
# SUMMARY_OUTPUT - this function takes the raw ouput data table and summarizes
# reduces it to compute percentiles of the monte carlo trials.
# INPUT:
#      output (pandas dataframe) ... the output data table
# OUTPUT:
#      summary (pandas dataframe) ... a data table containing the 25th, 50th, and
#                                     75th percentiles of each output.

    import pandas as pd
    import numpy as np

    def summarize_output(output):
        '''
        SUMMARIZE_OUTPUT: This function takes the raw output data table and summarizes
        it to compute percentiles of the Monte Carlo trials.

        Parameters:
        output (Pandas DataFrame): The output data table

        Returns:
        summary (Pandas DataFrame): A data table containing the 5th, 25th, 50th, 75th, and 95th percentiles of each output.
        
        '''

        ## Calculate Percentiles of LCOR, VOM, FOM, and LCOC -----------------------

        # Select relevant columns
        columns = ['Capacity', 'LCOR', 'VOM', 'FOM', 'LCOC']
        output2 = output[columns]
        
        # Compute 95th percentile
        quantile0 = output2.groupby('Capacity').quantile([0.95]) # 95th percentile
        quantile0 = quantile0.rename(columns={"LCOR": "LCOR_95%", "VOM": "VOM_95%", "FOM": "FOM_95%", "LCOC": "LCOC_95%"})

        # Compute 75th percentile
        quantile1 = output2.groupby('Capacity').quantile([0.75]) # 75th percentile
        quantile1 = quantile1.rename(columns={"LCOR": "LCOR_75%", "VOM": "VOM_75%", "FOM": "FOM_75%", "LCOC": "LCOC_75%"})

        # Compute 50th percentile
        quantile2 = output2.groupby('Capacity').quantile([0.5])  # 50th percentile
        quantile2 = quantile2.rename(columns={"LCOR": "LCOR_50%", "VOM": "VOM_50%", "FOM": "FOM_50%", "LCOC": "LCOC_50%"})

        # Compute 25th percentile
        quantile3 = output2.groupby('Capacity').quantile([0.25]) # 25th percentile
        quantile3 = quantile3.rename(columns={"LCOR": "LCOR_25%", "VOM": "VOM_25%", "FOM": "FOM_25%", "LCOC": "LCOC_25%"})

        # Compute 5th percentile
        quantile4 = output2.groupby('Capacity').quantile([0.05]) # 5th percentile
        quantile4 = quantile4.rename(columns={"LCOR": "LCOR_5%", "VOM": "VOM_5%", "FOM": "FOM_5%", "LCOC": "LCOC_5%"})

        # Merge data tables
        summary = pd.merge(quantile0, quantile1, on = ["Capacity"])
        summary = pd.merge(summary, quantile2, on = ["Capacity"])
        summary = pd.merge(summary, quantile3, on = ["Capacity"])
        summary = pd.merge(summary, quantile4, on = ["Capacity"])

        return summary

    columns = ['Capacity', 'LCOR', 'VOM', 'FOM', 'LCOC']
    output2 = output[columns]
    
   #Compute 95th percentle
    quantile0 = output2.groupby('Capacity').quantile([0.95]) #95th percentile
    quantile0 = quantile0.rename(columns={"LCOR": "LCOR_95%", "VOM": "VOM_95%", "FOM": "FOM_95%", "LCOC": "LCOC_95%"})


    #Compute 75th percentle
    quantile1 = output2.groupby('Capacity').quantile([0.75]) #75th percentile
    quantile1 = quantile1.rename(columns={"LCOR": "LCOR_75%", "VOM": "VOM_75%", "FOM": "FOM_75%", "LCOC": "LCOC_75%"})

    #Compute 50th percentile
    quantile2 = output2.groupby('Capacity').quantile([0.5])  #50th percentile
    quantile2 = quantile2.rename(columns={"LCOR": "LCOR_50%", "VOM": "VOM_50%", "FOM": "FOM_50%", "LCOC": "LCOC_50%"})

    #Compute 25th percentile
    quantile3 = output2.groupby('Capacity').quantile([0.25]) #25th percentile
    quantile3 = quantile3.rename(columns={"LCOR": "LCOR_25%", "VOM": "VOM_25%", "FOM": "FOM_25%", "LCOC": "LCOC_25%"})

    #Compute 5th percentile
    quantile4 = output2.groupby('Capacity').quantile([0.05]) #25th percentile
    quantile4 = quantile4.rename(columns={"LCOR": "LCOR_5%", "VOM": "VOM_5%", "FOM": "FOM_5%", "LCOC": "LCOC_5%"})

    #Merge data tables
    summary = pd.merge(quantile0, quantile1, on = ["Capacity"])
    summary = pd.merge(summary, quantile2, on = ["Capacity"])
    summary = pd.merge(summary, quantile3, on = ["Capacity"])
    summary = pd.merge(summary, quantile4, on = ["Capacity"])

    return summary

