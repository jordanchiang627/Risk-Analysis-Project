import pandas as pd
import geopandas as gpd
# flake8: noqa

disasters = pd.read_csv('DisasterDeclarationsSummaries.csv')
# print(disasters.head())
disasters = disasters[['femaDeclarationString', 'disasterNumber', 'state', 'declarationDate', 
'incidentType', 'declarationTitle', 'fipsStateCode', 'fipsCountyCode', 'placeCode', 'designatedArea', 'incidentId']]
# print(disasters.head())
disastersFlorida = disasters[disasters['state'] == 'FL']
disastersFlorida['designatedArea'] = disastersFlorida['designatedArea'].str.replace(r'[()]', '', regex=True)
disastersFlorida = disastersFlorida[disastersFlorida['designatedArea'] != 'Statewide']
print(disastersFlorida.head())
# print(disastersFlorida.shape)

frequency = disastersFlorida['designatedArea'].value_counts().reset_index()
frequency.columns = ['County Name', 'Disaster Frequency']
frequency = frequency[frequency['County Name'].str.contains('County', case=False, na=False)]
frequency['Disaster Frequency'] = frequency['Disaster Frequency'].astype(float)
print(frequency.dtypes)
print(frequency.head())

income = pd.read_csv('FloridaCountyIncome2022.csv')
# print(income.head())
income = income.rename(columns = {'Median Household Income (Census ACS), Dollars, 2022': 'County', 'Unnamed: 1':'Median Income'})
income = income.drop(index = [0, 1])
income['County'] = income['County'] + ' County'
income['Median Income'] = income['Median Income'].str.replace(',','').astype(float)
print(income.dtypes)
print(income.head())

density = pd.read_csv("FloridaPopDensity.csv")
density = density[['fips', 'stateCode', 'county', 'density']]
print(density.dtypes)
print(density.head())

DensityIncome = density.merge(income, left_on = 'county', right_on = 'County', how = 'inner')
DensityIncome = DensityIncome[['County', 'density', 'Median Income']]
print(DensityIncome.head())

FrequencyDensityIncome = DensityIncome.merge(frequency, left_on = 'County', right_on = 'County Name', how = 'inner')
FrequencyDensityIncome = FrequencyDensityIncome[['County', 'density', 'Median Income', 'Disaster Frequency']]
FrequencyDensityIncome['density'] = FrequencyDensityIncome['density'].round(3)

NormalizedColumns = {
    'Disaster Frequency': False,
    'Median Income': True,
    'density': False
}

for column, invert in NormalizedColumns.items():
    if invert: 
        FrequencyDensityIncome[f'Normalized {column}'] = round(1 - (FrequencyDensityIncome[column] - FrequencyDensityIncome[column].min()) / \
            (FrequencyDensityIncome[column].max() - FrequencyDensityIncome[column].min()), 4)
    else:
        FrequencyDensityIncome[f'Normalized {column}'] = round((FrequencyDensityIncome[column] - FrequencyDensityIncome[column].min()) / \
            (FrequencyDensityIncome[column].max() - FrequencyDensityIncome[column].min()), 4)

Classes = {
    'Normalized Disaster Frequency': 0.5,
    'Normalized Median Income': 0.3,
    'Normalized density': 0.2
}

FrequencyDensityIncome['Claim Probability'] = round(sum(
    Classes[f'Normalized {col}'] * FrequencyDensityIncome[f'Normalized {col}']
    for col in ['Disaster Frequency', 'Median Income', 'density']
), 3)

print(FrequencyDensityIncome.head())
print(FrequencyDensityIncome.shape)

Counties = gpd.read_file("USACounty/USACounty.shp")
Counties['NAME'] = Counties['NAME'] + ' County'
Counties = Counties[Counties['STATEFP'] == '12']
Counties = Counties[['NAME', 'geometry']]
print(Counties.crs)
print(Counties.head())

FloridaCountiesData = Counties.merge(FrequencyDensityIncome, left_on = 'NAME', right_on = 'County', how = 'inner')
FloridaCountiesData = FloridaCountiesData.drop(columns = ['NAME'])
print(FloridaCountiesData.head())
print(FloridaCountiesData.shape)

disasters.to_csv("CleanedData/disastersCleaned.csv", index = False)
disastersFlorida.to_csv("CleanedData/disastersFloridaCleaned.csv", index = False)
frequency.to_csv("CleanedData/frequencyFLDisasters.csv", index = False)
income.to_csv("CleanedData/incomeFloridaCleaned.csv", index = False)
density.to_csv("CleanedData/densityFloridaCleaned.csv", index = False)
FrequencyDensityIncome.to_csv("CleanedData/AllDataFlorida.csv", index = False)
FloridaCountiesData.to_file("CleanedData/FloridaCountiesData.geojson", driver = "GeoJSON")