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

