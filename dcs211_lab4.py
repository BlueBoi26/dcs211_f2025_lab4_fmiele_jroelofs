import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import seaborn as sns
from prettytable import PrettyTable as Table

filename = 'county_economic_status_2024.csv'

df = pd.read_csv(filename, skiprows = 4, 
skipfooter = 2, engine = "python", thousands = ',')

#renaming columns
df.columns = ['fips','state','county','arc_county', 'county_economic_status_24', 'ave_unemp_rate_19-21', 
              'pcmi_21', 'poverty_rate_17-21', 'ave_unemp_19-21_percent', 'pcmi_21_percent', 'pcmi_21_percent_inversed',
              'poverty_rate_17-21_percent', 'comp_index_24', 'index_rank_24', 'quartile_24']

#removing first row
df = df.iloc [1:] 
print(df.head())

#mean
print(np.mean(df['poverty_rate_17-21']))

#standard deviation
print(np.std(df['poverty_rate_17-21']))

#what data type
print(type(df['state']))

#how many counties per state
print(df.value_counts(['state']))

# Create the PrettyTable
table = Table()
table.field_names = ["State", " # counties", "PCI (mean)", "PCI (median)", "Poverty Rate"]

# Group each dataframe together by state
state_groups = df.groupby("state")

# Group the top 10 states by size (number of counties)
top_states = state_groups.size().nlargest(10)

for state, county_count in top_states.items():
    # Get the DataFrame for that specific state
    group = state_groups.get_group(state)
    
    # Compute state statistics
    pci_mean = group['pcmi_21'].mean()
    pci_median = group['pcmi_21'].median()
    pov_mean = group['poverty_rate_17-21'].mean()

    # Add a row to the PrettyTable
    table.add_row([state, county_count, f"{pci_mean:.2f}", f"{pci_median:.2f}", f"{pov_mean:.2f}"])
print(table)

# Create the PrettyTable
table2 = Table()
table2.field_names = ["State", " # counties", "PCI (mean)", "PCI (median)", "Poverty Rate"]

# Group each dataframe together by state
state_groups = df.groupby("state")

# Group the top 10 states by size (number of counties)
bottom_states = state_groups.size().nsmallest(10)

# Check if "District of Columbia" is in the index, and if it is, use the drop function to remove it
if "District of Columbia" in bottom_states.index:
    bottom_states = bottom_states.drop("District of Columbia")

for state, county_count in bottom_states.items():
    # Get the DataFrame for that specific state
    group = state_groups.get_group(state)
    
    # Compute state statistics
    pci_mean = group['pcmi_21'].mean()
    pci_median = group['pcmi_21'].median()
    pov_mean = group['poverty_rate_17-21'].mean()

    # Add a row to the PrettyTable
    table2.add_row([state, county_count, f"{pci_mean:.2f}", f"{pci_median:.2f}", f"{pov_mean:.2f}"])

print(table2)