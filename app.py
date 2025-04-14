import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from sklearn.decomposition import PCA
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
from src.dataset import Dataset

# Streamlit setup
st.set_page_config(layout="wide")
st.title("User Session Dashboard")

# Introduction and sidebar explanation
st.write("""
Welcome to the User Session Dashboard! Use the sidebar on the left to filter the data by country. 
The visualizations below will update based on your selection.
""")

# Load and preprocess data
@st.cache_data
def load_data():

    # Load JSON DB
    dataset = Dataset(directory='data')
    dataset.load()

    parsed_sessions = []
    for session_id in dataset.session_ids:
        session = dataset.sessions[session_id]
        session_data = {
            'timestamp': pd.to_datetime(session.timestamp),
            'hour': session.hour,
            'weekday': session.day_of_week,
            'device_type': session.device_type,
            'browser': session.browser,
            'country': session.country,
            'city': session.city,
        }
        parsed_sessions.append(session_data)

    return pd.DataFrame(parsed_sessions)

df_sessions = load_data()

# Helper conversion functions
def hour_label_to_24(label):
    return pd.to_datetime(label, format='%I %p').hour

def hour_24_to_label(hour):
    return pd.to_datetime(str(hour), format='%H').strftime('%-I %p')

hour_order = ['12 AM', '1 AM', '2 AM', '3 AM', '4 AM', '5 AM', '6 AM', '7 AM',
              '8 AM', '9 AM', '10 AM', '11 AM', '12 PM', '1 PM', '2 PM', '3 PM',
              '4 PM', '5 PM', '6 PM', '7 PM', '8 PM', '9 PM', '10 PM', '11 PM']

# Sidebar filters
selected_country = st.sidebar.selectbox(
    "Filter by Country",
    df_sessions['country'].value_counts().index
)
filtered_df = df_sessions[df_sessions['country'] == selected_country]

# Country clicks plot
st.subheader("Clicks by Country (Top 10)")
st.write("""
This plot shows the top 10 countries with the highest number of clicks. 
It provides an overview of user activity distribution across different countries.
""")
top_countries = df_sessions['country'].value_counts().nlargest(10).index
fig1, ax1 = plt.subplots()
sns.countplot(data=df_sessions[df_sessions['country'].isin(top_countries)],
              x='country', order=top_countries, ax=ax1)
ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45)
st.pyplot(fig1)

# Clicks by hour in selected country
st.subheader(f"Clicks by Hour in {selected_country} (refer to CEST time)")
st.write("""
This plot displays the distribution of clicks by hour for the selected country. 
It helps identify peak activity times during the day.
""")
fig2, ax2 = plt.subplots()
sns.countplot(data=filtered_df, x='hour', order=hour_order, ax=ax2)
ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45)
st.pyplot(fig2)

# Clicks by device type in selected country
st.subheader(f"Clicks by Device Type in {selected_country}")
st.write("""
This plot shows the distribution of clicks by device type (e.g., mobile, desktop) 
for the selected country. It provides insights into user preferences for devices.
""")
fig3, ax3 = plt.subplots()
sns.countplot(data=filtered_df, x='device_type',
              order=filtered_df['device_type'].value_counts().index, ax=ax3)
ax3.set_xticklabels(ax3.get_xticklabels(), rotation=45)
st.pyplot(fig3)

# PCA section in selected country
st.subheader(f"User Segments in {selected_country}")
st.write("""
This 3D scatter plot represents user segments based on PCA (Principal Component Analysis). 
It reduces the data dimensions to visualize patterns and clusters in user behavior.
""")
try:
    columns_to_encode = ['hour', 'weekday', 'device_type', 'browser', 'country', 'city']
    df_encoded = pd.get_dummies(filtered_df[columns_to_encode], drop_first=True)
    pca = PCA(n_components=3)
    pca_result = pca.fit_transform(df_encoded)
    df_pca = pd.DataFrame(pca_result, columns=['PC1', 'PC2', 'PC3'])

    fig_pca = px.scatter_3d(df_pca, x='PC1', y='PC2', z='PC3',
                            opacity=0.6, title="3D PCA Projection",
                            color_discrete_sequence=['blue'])
    fig_pca.update_layout(height=600, width=800, autosize=True)
    st.plotly_chart(fig_pca, use_container_width=True)
except Exception as e:
    st.error("Sorry, we need more data to segment customers or an error occurred.")
