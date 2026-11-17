
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page configuration
st.set_page_config(
    page_title="COVID-19 Dashboard",
    layout="wide"
)

# Dashboard title
st.title("COVID-19 Data Analysis Dashboard")
st.write("COVID-19 cases and deaths analysis by country")


# Step 1: Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("COVID_Datacleaning.csv")
    df = df.drop_duplicates()
    df['Date'] = pd.to_datetime(df['Date'])
    return df


df = load_data()


# Step 2: KPI calculations
total_countries = df['Country'].nunique()
total_confirmed = df['newConfirmedCase'].sum()
total_deaths = df['newDeathCase'].sum()

col1, col2, col3 = st.columns(3)

col1.metric("Total Countries", total_countries)
col2.metric("Total Confirmed Cases", f"{total_confirmed:,.0f}")
col3.metric("Total Deaths", f"{total_deaths:,.0f}")


# Step 3: Top 10 Countries by Confirmed Cases
st.subheader("Top 10 Countries by Confirmed Cases")

top_countries = (
    df.groupby('Country')['Confirmedcase']
    .max()
    .nlargest(10)
    .sort_values()
)

fig, ax = plt.subplots(figsize=(10, 6))

top_countries.plot(
    kind='barh',
    color='red',
    ax=ax
)

ax.set_xlabel("Confirmed Cases")
ax.set_ylabel("Country")
ax.set_title("Top 10 Countries by Confirmed Cases")

plt.tight_layout()
st.pyplot(fig)
plt.close(fig)


# Step 4: Top 10 Countries by Death Cases
st.subheader("Top 10 Countries by Death Cases")

top_deaths = (
    df.groupby('Country')['Death']
    .max()
    .nlargest(10)
    .sort_values()
)

fig, ax = plt.subplots(figsize=(10, 6))

top_deaths.plot(
    kind='barh',
    color='darkred',
    ax=ax
)

ax.set_xlabel("Death Cases")
ax.set_ylabel("Country")
ax.set_title("Top 10 Countries by Death Cases")

plt.tight_layout()
st.pyplot(fig)
plt.close(fig)


# Step 5: KDE Plot - Confirmed Cases vs Death Cases

st.subheader("Top 10 Countries: Confirmed vs Death Cases")

top10 = (
    df.groupby('Country')[['Confirmedcase', 'Death']]
    .max()
    .nlargest(10, 'Confirmedcase')
)

fig, ax = plt.subplots(figsize=(10, 6))

# KDE plot for Confirmed Cases
sns.kdeplot(
    data=top10,
    x='Confirmedcase',
    fill=True,
    color='red',
    alpha=0.4,
    linewidth=2,
    label='Confirmed Cases',
    ax=ax
)

# KDE plot for Death Cases
sns.kdeplot(
    data=top10,
    x='Death',
    fill=True,
    color='black',
    alpha=0.3,
    linewidth=2,
    label='Death Cases',
    ax=ax
)

# Customize KDE plot
ax.set_title(
    'Top 10 Countries: Confirmed vs Death Cases',
    fontsize=15,
    color='blue'
)

ax.set_xlabel(
    'Number of Cases',
    color='red',
    fontsize=12
)

ax.set_ylabel(
    'Density',
    color='red',
    fontsize=12
)

ax.legend()

plt.tight_layout()
st.pyplot(fig)
plt.close(fig)


# Step 6: Correlation Heatmap
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

ax.set_title("COVID-19 Correlation Heatmap")

plt.tight_layout()
st.pyplot(fig)
plt.close(fig)


# Step 7: View Dataset
with st.expander("View Dataset"):
    st.dataframe(df)
