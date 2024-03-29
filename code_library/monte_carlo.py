import numpy as np


def monte_carlo(input, output, tech, start, end):
    '''
    MONTE_CARLO: This function updates the input parameters to include randomly generated values
    for Monte Carlo simulations. The distribution of the random parameters is 
    specified in the input "monte_carlo" spreadsheet. The random parameters for
    each Monte Carlo trial are stored in successive rows of the data table "output".

    Parameters:
    input (InputTemplate): Standard input data structure
    output (Pandas DataFrame): Output table
    tech (string): Technology of interest
    start (integer): Row number where data should start being saved in output
    end (integer): Row number where data should stop being saved in output

    Returns:
    input (InputTemplate): Standard input data structure with randomly 
                           generated inputs following the distributions specified for the 
                           Monte Carlo analysis.
    output (Pandas DataFrame): Data table in which to store the randomly
                               generated parameters. The values are stored to make it easier to
                               analyze simulation results at the end.
    '''

    # Determine number of rows in the monte_carlo table; number of rows set in main_monte_carlo
    n_row = input.monte_carlo.shape[0]
    # Access to inputs table
    for i in range(0,n_row):
        sheet = input.monte_carlo.loc[i, "Sheet"] #sheet which to modify
        row = input.monte_carlo.loc[i, "Row"] #row which to modify (=variable name)
        column = input.monte_carlo.loc[i, "Column"]#column which to modify
        distribution = input.monte_carlo.loc[i, "Distribution"]#distribution which to draw form

        # Skip the row if it relates to a technology parameter for a different technology
        # than the one currently under consideration.
        if ((sheet == 'technology') and (column != tech)) or\
            ((sheet == 'epc_cost') and (tech not in row)):
            continue

        match distribution: # Random parameter is generator tailored to distribution given in inputs

            case "Normal": # If normal distribution

                # Retrieve parameters
                mean = input.monte_carlo.loc[i, "Mean"]
                variance = input.monte_carlo.loc[i, "Variance"]
                assert ~np.isnan(mean), "Normal Distribution missing mean"
                assert ~np.isnan(variance), "Normal Distribution missing variance"


                # Generate random value
                value = np.random.normal(mean, variance)

                # Update input value
                getattr(input, sheet).loc[row, column] = value 

                # Save value to output   
                output.loc[start:end, row + '_' + column] = value

            case "TripleNormal": #If normal distribution

                # Retrieve parameters
                pct1 = input.monte_carlo.loc[i, "pct1"]
                pct2 = input.monte_carlo.loc[i, "pct2"]
                pct3 = input.monte_carlo.loc[i, "pct3"]
                
                # Check that no parameters are missing
                assert ~np.isnan(pct1), "TripleNormal Distribution is missing pct1"
                assert ~np.isnan(pct2), "TripleNormal Distribution is missing pct2"
                assert ~np.isnan(pct3), "TripleNormal Distribution is missing pct3"
                assert np.isclose(np.sum([pct1,pct2,pct3]),1), "TripleNormal Probabilities do not sum to 1"
                
                # Pick which distribution it is from based on the probabilities
                rand = np.random.rand()
                if rand < pct1:
                    mean = input.monte_carlo.loc[i, "mean1"]
                    std = input.monte_carlo.loc[i, "std1"]
                elif rand < pct1 + pct2:
                    mean = input.monte_carlo.loc[i, "mean2"]
                    std = input.monte_carlo.loc[i, "std2"]
                else: 
                    mean = input.monte_carlo.loc[i, "mean3"]
                    std = input.monte_carlo.loc[i, "std3"]
                
                # Check that no parameters are missing
                assert ~np.isnan(mean), "TripleNormal Distribution missing mean"
                assert ~np.isnan(std), "TripleNormal Distribution missing std"

                # Generate random value
                value = np.random.normal(mean, std)

                # Update input value
                getattr(input, sheet).loc[row, column] = value 

                # Save value to output   
                output.loc[start:end, row + '_' + column] = value                

            case "Triangular": # If triangular distribution

                # Get parameters
                min = input.monte_carlo.loc[i, "Min"]
                max = input.monte_carlo.loc[i, "Max"]
                mode = input.monte_carlo.loc[i, "Mean"]

                # Check that no parameters are missing
                assert ~np.isnan(min), "Triangular Distribution is missing min"
                assert ~np.isnan(mode), "Triangular Distribution is missing mode"
                assert ~np.isnan(max), "Triangular Distribution is missing max"

                # Generate random value
                value = np.random.triangular(min, mode, max)

                # Update input value
                getattr(input, sheet).loc[row, column] = value

                # Save to output    
                output.loc[start:end, row + '_' + column] = value
                
            case "Uniform":# If uniform distribution
                
                # Get parameters
                min = input.monte_carlo.loc[i, "Min"]
                max = input.monte_carlo.loc[i, "Max"]

                # Check for missing parameters
                assert ~np.isnan(min), "Uniform Distribution is missing min"
                assert ~np.isnan(max), "Uniform Distribution is missing max"

                # Generate random value
                value = np.random.uniform(min, max)

                # Update input value
                getattr(input, sheet).loc[row, column] = value   

                # Save to output 
                output.loc[start:end, row + '_' + column] = value

            case _:            
                raise Exception("Distribution type {distribution} not defined".format(distribution = distribution))

    return input, output


        


    

    