
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="COVID-19 Dashboard",
    layout="wide"
)

st.title("COVID-19 Data Analysis Dashboard")
st.write("COVID-19 cases and deaths analysis by country")

@st.cache_data
def load_data():
    df = pd.read_csv("COVID_Datacleaning.csv")
    df = df.drop_duplicates()
    df['Date'] = pd.to_datetime(df['Date'])
    return df

df = load_data()

# KPI calculations
total_countries = df['Country'].nunique()
total_confirmed = df['newConfirmedCase'].sum()
total_deaths = df['newDeathCase'].sum()

col1, col2, col3 = st.columns(3)

col1.metric("Total Countries", total_countries)
col2.metric("Total Confirmed Cases", f"{total_confirmed:,.0f}")
col3.metric("Total Deaths", f"{total_deaths:,.0f}")

st.subheader("Top 10 Countries by Confirmed Cases")

top_countries = (
    df.groupby('Country')['Confirmedcase']
    .max()
    .nlargest(10)
    .sort_values()
)

fig, ax = plt.subplots(figsize=(10, 6))
top_countries.plot(kind='barh', color='red', ax=ax)
ax.set_xlabel("Confirmed Cases")
ax.set_ylabel("Country")
st.pyplot(fig)
plt.close(fig)

st.subheader("Top 10 Countries by Death Cases")

top_deaths = (
    df.groupby('Country')['Death']
    .max()
    .nlargest(10)
    .sort_values()
)

fig, ax = plt.subplots(figsize=(10, 6))
top_deaths.plot(kind='barh', color='darkred', ax=ax)
ax.set_xlabel("Death Cases")
ax.set_ylabel("Country")
st.pyplot(fig)
plt.close(fig)

st.subheader("Confirmed Cases vs Deaths")

fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(
    data=df,
    x='Confirmedcase',
    y='Death',
    ax=ax
)
ax.set_xlabel("Confirmed Cases")
ax.set_ylabel("Deaths")
st.pyplot(fig)
plt.close(fig)

st.subheader("Correlation Heatmap")

numeric_cols = [
    'Confirmedcase',
    'Death',
    'newConfirmedCase',
    'newDeathCase'
]

fig, ax = plt.subplots(figsize=(8, 5))
sns.heatmap(
    df[numeric_cols].corr(),
    annot=True,
    cmap='coolwarm',
    ax=ax
)
st.pyplot(fig)
plt.close(fig)

with st.expander("View Dataset"):
    st.dataframe(df)
