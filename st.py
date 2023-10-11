import plotly.express as px
import streamlit as st
from pandas import DataFrame, read_sql
from sqlalchemy import create_engine
import datetime

engine = create_engine('sqlite:///db.sqlite', echo=False)

daily_prices = read_sql(f"""
    SELECT avg(priceStudents) AS StudierendenPreis, date AS Datum FROM dish
    WHERE restaurant = 'mensa-academica-paderborn' AND category = 'dish' AND date(date) <= date('2023-10-31')
    GROUP BY date
    """, con=engine)

price_steps = read_sql(f"""
    SELECT name_de AS Gericht, priceStudents AS StudierendenPreis, date AS Datum, thumbnail FROM dish
    WHERE restaurant = 'mensa-academica-paderborn' AND category = 'dish' AND date(date) <= date('2023-10-31')
    GROUP BY name_de, priceStudents, date
    """, con=engine)


price_diff = read_sql(f"""
    SELECT name_de AS Gericht, min(priceStudents), max(priceStudents),
    max(priceStudents)/min(priceStudents) AS difference 
    FROM (SELECT name_de, priceStudents, min(date) AS min_date, max(date) AS max_date 
        FROM dish WHERE restaurant = 'mensa-academica-paderborn' AND category = 'dish' AND date(date) <= date('2023-10-31')
        GROUP BY name_de, priceStudents) 
    GROUP BY name_de ORDER BY difference DESC
    """, con=engine)

# relevant_price_diff = price_diff[price_diff['difference'] > 1]

# relevant_dishes = relevant_price_diff['Gericht']

# df = price_steps[price_steps['Gericht'].isin(relevant_dishes)]
df = price_steps

st.title("Visualisierung der Mensa-Preise")

tab1, tab2 = st.tabs(["Preisverlauf", "Einzelpreise"])
with tab2:
    st.dataframe(price_diff, height=300)

    options = st.multiselect('Wähle ein oder mehrere Gerichte:', set(df['Gericht']))

    filtered_df = df[df['Gericht'].isin(options)]

    if options:
        dis_filtered = filtered_df[['Gericht', 'thumbnail']].drop_duplicates()
        dis_filtered = dis_filtered[dis_filtered['thumbnail'].str.len() > 0]

        st.image(list(dis_filtered['thumbnail']), caption=list(dis_filtered['Gericht']), width=200)

        fig = px.scatter(filtered_df, x="Datum", y="StudierendenPreis", color='Gericht', text="StudierendenPreis")
        fig.update_traces(textposition="bottom center")
        fig.update_layout(
            yaxis_title="Preis für Studierende (in Euro)",
        )
        st.plotly_chart(fig, use_container_width=True, theme=None)

        st.download_button('Grafik herunterladen', fig.to_image(format='png', width=800, height=600),
                           f'gerichte.png', 'image/png')
with tab1:
    fig = px.scatter(daily_prices, x="Datum", y="StudierendenPreis")
    fig.update_layout(
        yaxis_title="Preis für Studierende (in Euro)",
    )
    st.plotly_chart(fig, use_container_width=True, theme=None)
