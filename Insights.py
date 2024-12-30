import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import dataframe_image as dfi
# flake8: noqa

data = pd.read_csv("CleanedData/AllDataFlorida.csv")
#print(data.head())

plt.figure(figsize=(8, 6))
plt.hist(data['Claim Probability'], bins=20, color='blue', alpha=0.7, edgecolor='black')
plt.title('Distribution of Claim Probability')
plt.xlabel('Claim Probability')
plt.ylabel('Frequency')
plt.grid(False)
#plt.show()

plt.figure(figsize=(8, 6))
sns.kdeplot(data=data, x='Claim Probability', fill=True, color='green')
plt.title('Density Plot of Claim Probability')
plt.xlabel('Claim Probability')
plt.ylabel('Density')
plt.grid(False)
#plt.show()

plt.figure(figsize=(8, 6))
plt.hist(data['density'], bins=20, color='blue', alpha=0.7, edgecolor='black')
plt.title('Distribution of Population Density')
plt.xlabel('Population Denstiy (people/square mile)')
plt.ylabel('Frequency')
plt.grid(False)
#plt.show()

plt.figure(figsize=(8, 6))
plt.hist(data['Median Income'], bins=20, color='blue', alpha=0.7, edgecolor='black')
plt.title('Distribution of Median Income')
plt.xlabel('Median Income ($)')
plt.ylabel('Frequency')
plt.grid(False)
#plt.show()

plt.figure(figsize=(8, 6))
plt.hist(data['Disaster Frequency'], bins=20, color='blue', alpha=0.7, edgecolor='black')
plt.title('Distribution of Disaster Frequency')
plt.xlabel('Disaster Frequency')
plt.ylabel('Frequency')
plt.grid(False)
#plt.show()

columns = ['density', 'Median Income', 'Disaster Frequency', 'Claim Probability']

stats = {}

for column in columns:
    stats[column] = {
        'Min': data[column].min(),
        'Max': data[column].max(),
        'Median': data[column].median()
    }

stats_df = pd.DataFrame(stats).T
print(stats_df)
dfi.export(stats_df.round(2), "Images/stats_image.png")

CorrelationMatrix = data[columns].corr()

print("Correlation Matrix:")
print(CorrelationMatrix)
dfi.export(CorrelationMatrix.round(4), "Images/CorrelationMatrix.png")

ClaimProbCorrelations = CorrelationMatrix[['Claim Probability']].drop(index='Claim Probability')
print("Correlations with Claim Probability:")
print(ClaimProbCorrelations)
dfi.export(ClaimProbCorrelations.round(4), "Images/ClaimProbCorrelations.png")

for column in columns:
    Top5 = data.sort_values(by=column, ascending=False).head(5)
    Top5 = Top5[['County', column]]
    Top5[column] = Top5[column].round(3)
    file_name = f"Images/Top5Counties_{column.replace(' ', '_')}.png"
    dfi.export(Top5, file_name)

for column in columns:
    Bottom5 = data.sort_values(by=column, ascending=True).head(5)
    Bottom5 = Bottom5[['County', column]]
    Bottom5[column] = Bottom5[column].round(3)
    file_name = f"Images/Bottom5Counties_{column.replace(' ', '_')}.png"
    dfi.export(Bottom5, file_name)
