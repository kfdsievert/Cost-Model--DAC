import numpy as np

def energy_price(input):
    '''
    ENERGY_PRICE: This function extracts the relevant energy and heat prices, as chosen in the universal inputs. 
    It returns both values in the units of $/GJ.

    Parameters:
    input (InputTemplate): Standard input data structure.

    Returns:
    electricity_price (float): Price of electricity in $/GJ.
    heat_price (float): Price of heat in $/GJ.
    electricity_co2 (float): CO2 intensity of electricity in ton CO2/GJ.
    heat_co2 (float): CO2 intensity of heat in ton CO2/GJ.
    '''

    # Use saved results if available
    if ~np.isnan(input.unlearned.electricity_price) & ~np.isnan(input.unlearned.heat_price) &\
        ~np.isnan(input.unlearned.electricity_co2) & ~np.isnan(input.unlearned.heat_co2):
        
        return input.unlearned.electricity_price, input.unlearned.heat_price, input.unlearned.electricity_co2, input.unlearned.heat_co2
    
    # Extract important parameters for estimating the electricity and heat price
    electricity_source = input.universal.loc["electricity_source", "Value"]
    electricity_scenario = input.universal.loc["electricity_scenario", "Value"]
    heat_source = input.universal.loc["heat_source", "Value"]
    year = input.universal.loc["energy_price_year", "Value"]

    # Extract conversion factors
    conversion_electricity = input.universal.loc["conversion_electricity", "Value"] #GJ/MWh

    # Identify row in electricity and heat tables to draw cost from
    idx_electricity = (input.electricity['Scenario'] == electricity_scenario)*\
        (input.electricity['Technology'] == electricity_source)
    idx_heat = (input.heat['Fuel'] == heat_source)

    # Check that unique source was identified
    assert sum(idx_electricity) == 1, "Electricity source not unique"
    assert sum(idx_heat) == 1, "Heat source not unique"

    # Filter heat prices to only include relevant scenario
    # Calculate Energy and Heat Prices
    electricity_price = float(input.electricity.loc[idx_electricity, year]/conversion_electricity)
    heat_price = float(input.heat.loc[idx_heat, year])
    electricity_co2 = float(input.electricity.loc[idx_electricity, "carbon_intensity"])
    heat_co2 = float(input.heat.loc[idx_heat, "carbon_intensity"])

    # Save results for future use
    input.unlearned.electricity_price = electricity_price
    input.unlearned.heat_price = heat_price
    input.unlearned.electricity_co2 = electricity_co2
    input.unlearned.heat_co2 = heat_co2

    return electricity_price, heat_price, electricity_co2, heat_co2