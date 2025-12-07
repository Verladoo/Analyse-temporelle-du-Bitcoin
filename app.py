import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    # Adapter le nom du fichier si besoin
    df = pd.read_csv("btcusd_1-min_data.csv")
    # Conversion du timestamp en datetime
    df["Date"] = pd.to_datetime(df["Timestamp"], unit="s")
    df = df.sort_values("Date")
    
    # Agrégation par jour (comme dans le notebook)
    df_jour = df.resample("D", on="Date").agg({
        "Open": "first",
        "High": "max",
        "Low": "min",
        "Close": "last",
        "Volume": "sum"
    }).dropna()
    df_jour.index.name = "Date"
    
    # Moyennes mobiles (30j et 90j)
    df_jour["MM_30"] = df_jour["Close"].rolling(window=30).mean()
    df_jour["MM_90"] = df_jour["Close"].rolling(window=90).mean()
    
    # Volatilité glissante (30j) - optionnelle pour un graphique dédié
    df_jour["Volatilite_30j"] = df_jour["Close"].rolling(window=30).std()
    
    return df_jour

def main():

    st.title("Tableau de bord interactif du Bitcoin")
    st.write("Application Streamlit pour explorer le prix, le volume et la volatilité du Bitcoin (données agrégées par jour).")

    df_jour = load_data()

    # =========================
    st.sidebar.header("Filtres")

    # plage de dates possible
    min_date = df_jour.index.min().date()
    max_date = df_jour.index.max().date()

    date_debut, date_fin = st.sidebar.date_input(
        "Période d'analyse",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )

    # Sécurité : si l'utilisateur ne sélectionne qu'une seule date
    if isinstance(date_debut, list):
        date_debut, date_fin = date_debut

    # Filtrage des données
    mask = (df_jour.index.date >= date_debut) & (df_jour.index.date <= date_fin)
    df_filtre = df_jour.loc[mask]

    if df_filtre.empty:
        st.warning("Aucune donnée pour la période sélectionnée.")
        return

    # Options d'affichage
    afficher_mm = st.sidebar.checkbox("Afficher les moyennes mobiles (30j et 90j)", value=True)
    afficher_volatilite = st.sidebar.checkbox("Afficher la volatilité glissante (30j)", value=True)

    # On remet l'index en colonne pour Plotly
    df_plot = df_filtre.reset_index().rename(columns={"Date": "DateJour"})

    # =========================
    st.subheader("Évolution du prix de clôture (Close)")

    # Graphique de base : prix de clôture
    if afficher_mm:
        fig_price = px.line(
            df_plot,
            x="DateJour",
            y=["Close", "MM_30", "MM_90"],
            labels={"value": "Prix (USD)", "DateJour": "Date", "variable": "Série"},
            title="Prix de clôture du Bitcoin avec moyennes mobiles (30j et 90j)"
        )
    else:
        fig_price = px.line(
            df_plot,
            x="DateJour",
            y="Close",
            labels={"Close": "Prix de clôture (USD)", "DateJour": "Date"},
            title="Prix de clôture quotidien du Bitcoin"
        )

    st.plotly_chart(fig_price, use_container_width=True)

    # =========================
    st.subheader("Volume d'échange quotidien")

    fig_volume_time = px.bar(
        df_plot,
        x="DateJour",
        y="Volume",
        labels={"DateJour": "Date", "Volume": "Volume (somme journalière)"},
        title="Volume d'échange du Bitcoin (par jour)"
    )
    st.plotly_chart(fig_volume_time, use_container_width=True)

    # =========================
    st.subheader("Relation entre prix de clôture et volume")

    fig_scatter = px.scatter(
        df_plot,
        x="Close",
        y="Volume",
        labels={"Close": "Prix de clôture (USD)", "Volume": "Volume (somme journalière)"},
        title="Prix de clôture vs Volume (données journalières)",
        opacity=0.5
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

    # =========================
    if afficher_volatilite:
        st.subheader("Volatilité glissante du prix (30 jours)")

        fig_volatilite = px.line(
            df_plot,
            x="DateJour",
            y="Volatilite_30j",
            labels={"Volatilite_30j": "Volatilité (écart-type sur 30 jours)", "DateJour": "Date"},
            title="Volatilité glissante du prix du Bitcoin (fenêtre de 30 jours)"
        )
        st.plotly_chart(fig_volatilite, use_container_width=True)

    # =========================
    st.subheader("Indicateurs sur la période sélectionnée")

    col1, col2, col3 = st.columns(3)
    col1.metric("Prix moyen (USD)", f"{df_filtre['Close'].mean():.2f}")
    col2.metric("Prix max (USD)", f"{df_filtre['Close'].max():.2f}")
    col3.metric("Volume total", f"{df_filtre['Volume'].sum():.0f}")

if __name__ == "__main__":
    main()
