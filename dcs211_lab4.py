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

#function to create per-state bar graph 
us_state_to_abbrev = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC",
    "American Samoa": "AS",
    "Guam": "GU",
    "Northern Mariana Islands": "MP",
    "Puerto Rico": "PR",
    "United States Minor Outlying Islands": "UM",
    "Virgin Islands, U.S.": "VI",
}

def createByStateBarPlot(df, field, filename, title, ylabel):
    '''
    function to create bar graph, grouped by state, for certain fields

    Parameters:
        df: arc data frame
        field: which field to graph
        filename: name of file graph will be saved to
        title: title of graph
        ylabel:label of y-axis
    '''
    state_mean= df.groupby('state')[field].mean()
    state_mean= state_mean.sort_values()
    state_abbreviations = [us_state_to_abbrev[state] for state in state_mean.index]

    plt.figure(figsize=(12,6))
    plt.bar(range(len(state_mean)), state_mean.values)
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xticks(range(len(state_mean)), state_abbreviations, rotation=90)

    plt.savefig(filename)