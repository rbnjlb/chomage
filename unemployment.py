import requests
import pandas as pd
import numpy as np
import json
import pycountry
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator


def get_alpha(countryName):
    country = pycountry.countries.get(name=countryName).alpha_2
    if country is None:
        raise ValueError(f"Pays inconnu : {countryName}")
    return country.lower()
    

def get_data(country, format):

    url = f"https://api.worldbank.org/v2/country/{country}/indicator/SL.UEM.TOTL.ZS?format={format}"
    reponse = requests.get(url)
    data = reponse.json()
    
    path = f"{country}Unemployment.json"
    
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, sort_keys= True, indent=4 )
        
    with open(path, "r") as file:
        loadData = json.load(file)

    return loadData
    

def to_DF(country, data):
    years = []
    values = []
    
    for i in data[1]:
        
        year = i["date"]
        value = i["value"]
        
        if value is not None:
            years.append(year)
            values.append(value)
            
    row = pd.DataFrame({
        "Country" : country,
        "Year" : years,
        "Unemployment" : values,
    })

    return row 
        
            
def unemployment_per_country(countries):
    dfs = []
    for i in countries:

        country = get_alpha(i)   
        loadData = get_data(country, "json")  
    
        temp_df = to_DF(country, loadData)
        dfs.append(temp_df)
    df = pd.concat(dfs, ignore_index=True)
  
    return df  
    
    

countries = ["France","Japan","Nigeria","New Zealand","Thailand","Argentina"]     

df = unemployment_per_country(countries)
      
            
            
plt.figure(figsize=(10, 6))
for country, group in df.groupby("Country"):
    group = group.sort_values("Year")
    country = pycountry.countries.get(alpha_2=country).name
    plt.plot(group["Year"], group["Unemployment"], label=country.capitalize())

plt.legend(    
    loc="upper center",
    bbox_to_anchor=(0.5, -0.15),
    ncol=3,
    frameon=False
    )


ax = plt.gca()
ax.xaxis.set_major_locator(MultipleLocator(5))

plt.grid(axis="y", linestyle="--", alpha=0.4)
plt.title("Chômage par pays")
plt.xlabel("Année")
plt.ylabel("%")
plt.tight_layout(rect=[0, 0.05, 1, 1])
#plt.show()


#dfstat = df.groupby("Country")["Unemployment"].agg(["mean", "std", "min", "max"]))


df["mean_unemployment"] = df.groupby("Country")["Unemployment"].transform("mean")
df["std_unemployment"] = df.groupby("Country")["Unemployment"].transform("std")



df["norm_unemployment"] = ((df["Unemployment"] - df["mean_unemployment"])/ df["std_unemployment"])

conditions = [
    df["norm_unemployment"] < -1,
    df["norm_unemployment"].between(-1, 1),
    df["norm_unemployment"] > 1
]

choices = [
    "Low",
    "Normal",
    "High"
]

df["level"] = np.select(conditions, choices, default="Normal")
    
    
    
plt.figure(figsize=(10, 6))
for country, group in df.groupby("Country"):
    group = group.sort_values("Year")
    country = pycountry.countries.get(alpha_2=country).name
    plt.plot(group["Year"], group["norm_unemployment"], label=country.capitalize())

plt.legend(    
    loc="upper center",
    bbox_to_anchor=(0.5, -0.15),
    ncol=3,
    frameon=False
    )


ax = plt.gca()
ax.xaxis.set_major_locator(MultipleLocator(5))
plt.axhline(y=0, color="black")

plt.grid(axis="y", linestyle="--", alpha=0.4)
plt.title("Chômage par pays")
plt.xlabel("Année")
plt.ylabel("%")
plt.tight_layout(rect=[0, 0.05, 1, 1])
plt.show()

