import pandas as pd

# 1. Charger les données depuis le fichier CSV
df = pd.read_csv("btcusd_1-min_data.csv") 

# 2. Conversion du timestamp
df["Date"] = pd.to_datetime(df["Timestamp"], unit="s")
df = df.sort_values("Date")

# 3. Agrégation par jour 
df_jour = df.resample("D", on="Date").agg({
    "Open": "first",
    "High": "max",
    "Low": "min",
    "Close": "last",
    "Volume": "sum"
}).dropna()

df_jour.index.name = "Date"

# 4. Sauvegarde d’un CSV avec les données agrégées par jour
df_jour.to_csv("btc_daily_agg.csv")
print("Fichier 'btc_daily_agg.csv' créé avec succès !")
