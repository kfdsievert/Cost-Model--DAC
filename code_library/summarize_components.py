import numpy as np
import pandas as pd

def summarize_components(output, column_names_cost, column_names_lr):
    '''
    SUMMARIZE_COMPONENTS: This function calculates the mean of cost and learning rate components
    for each unique capacity value in the output DataFrame. The mean is calculated only for rows
    where the LCOR value falls within the 45th to 55th percentile range for each capacity.

    Parameters:
    output (Pandas DataFrame): Output data
    column_names_cost (list): List of column names in the output DataFrame that represent cost components
    column_names_lr (list): List of column names in the output DataFrame that represent learning rate components

    Returns:
    mean_cost_df (Pandas DataFrame): DataFrame containing the mean cost components for each unique capacity
    mean_lr_df (Pandas DataFrame): DataFrame containing the mean learning rate components for each unique capacity
    '''

    capacities = np.unique(output['Capacity'])
    mean_costs_data = []
    mean_lrs_data = []

    for capacity in capacities:
        capacity_data = output[output['Capacity'] == capacity]

        if capacity_data.empty:
            continue

        lower_bound = np.percentile(capacity_data['LCOR'], 45)
        upper_bound = np.percentile(capacity_data['LCOR'], 55)

        # Filter rows where LCOR falls within the calculated percentile range
        percentile_data = capacity_data[(capacity_data['LCOR'] >= lower_bound) & (capacity_data['LCOR'] <= upper_bound)]

        if percentile_data.empty:
            continue

        # Calculate the mean of the costs and learning rates within this band
        mean_costs = percentile_data[column_names_cost].mean()
        mean_lrs = percentile_data[column_names_lr].mean()

        # Append the mean values to the lists
        mean_costs_data.append([capacity] + mean_costs.tolist())
        mean_lrs_data.append([capacity] + mean_lrs.tolist())

    # Create DataFrames from the lists
    mean_cost_df = pd.DataFrame(mean_costs_data, columns=['Capacity'] + column_names_cost)
    mean_lr_df = pd.DataFrame(mean_lrs_data, columns=['Capacity'] + column_names_lr)

    return mean_cost_df, mean_lr_df



#import numpy as np

#def summarize_components(output, column_names_cost, column_names_lr):
# SUMMARY_OUTPUT - this function takes the raw ouput data table and summarizes
# reduces it to compute percentiles of the monte carlo trials.
# INPUT:
#      output (pandas dataframe) ... the output data table
#      column_names (list) ... columns which to keep in the final table
# OUTPUT:
#      medians (pandas dataframe) ... a data table containing LCOR, VOM, FOM,
#                                     and component costs for the monte carlo trial
#                                     which resulted in the median (50th-percentile)
#                                     LCOR.

   ## Determine component costs at median -------------------------------------
    #capacities = np.unique(output.Capacity)
    #idx_list = []

    #for i in range(len(capacities)):
        #capacity = capacities[i]
        #data = output.loc[np.isclose(list(output.Capacity), capacity),:]
        #data = data.sort_values("LCOR")
        #median_row = int(np.floor(data.shape[0]/2))
        #median_idx = data.index[median_row]
        #idx_list.append(median_idx)


    #median_cost = output.loc[idx_list,['Capacity'] + column_names_cost].copy()
    #median_cost.reset_index()

    #median_lr = output.loc[idx_list, ['Capacity'] + column_names_lr].copy()
    #median_lr.reset_index()

    #return median_cost, median_lr