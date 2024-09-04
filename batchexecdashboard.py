import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

# Set page config
st.set_page_config(page_title="Client Sentiment Analysis", layout="wide")

# Function to load data
@st.cache_data
def load_data():
    # This is where you'd normally load your data from a file or database
    # For this example, we'll create a sample dataframe
    data = {
        'Client ID': range(1, 138),
        'Sentiment': np.random.choice(['Positive', 'Neutral', 'Negative'], 137),
        'Theme': np.random.choice(['UI/UX', 'Reporting', 'Mobile', 'Performance', 'Customer Service'], 137),
        'Feedback': ['Sample feedback ' + str(i) for i in range(1, 138)]
    }
    return pd.DataFrame(data)

# Load data
df = load_data()

# Title
st.title('Client Sentiment Analysis Dashboard')

# Sidebar
st.sidebar.header('Filters')
selected_theme = st.sidebar.multiselect('Select Theme', options=df['Theme'].unique(), default=df['Theme'].unique())

# Filter data
filtered_df = df[df['Theme'].isin(selected_theme)]

# Main content
col1, col2 = st.columns(2)

with col1:
    st.subheader('Overall Sentiment Distribution')
    sentiment_counts = filtered_df['Sentiment'].value_counts()
    sentiment_chart = alt.Chart(sentiment_counts.reset_index()).mark_arc().encode(
        theta='count',
        color='index',
        tooltip=['index', 'count']
    ).properties(width=300, height=200)
    st.altair_chart(sentiment_chart)

with col2:
    st.subheader('Sentiment by Theme')
    theme_sentiment = filtered_df.groupby(['Theme', 'Sentiment']).size().unstack()
    theme_chart = alt.Chart(theme_sentiment.reset_index().melt('Theme')).mark_bar().encode(
        x='Theme',
        y='value',
        color='variable',
        tooltip=['Theme', 'variable', 'value']
    ).properties(width=400, height=300)
    st.altair_chart(theme_chart)

# Detailed data view
st.subheader('Detailed Feedback')
st.dataframe(filtered_df)

# Word cloud (requires additional setup)
st.subheader('Common Words in Feedback')
st.write("Word cloud visualization would go here. It requires additional setup with libraries like wordcloud.")

# Metrics
st.subheader('Key Metrics')
col1, col2, col3 = st.columns(3)
col1.metric("Total Responses", len(filtered_df))
col2.metric("Positive Sentiment", f"{(filtered_df['Sentiment'] == 'Positive').mean():.2%}")
col3.metric("Negative Sentiment", f"{(filtered_df['Sentiment'] == 'Negative').mean():.2%}")

# Individual response explorer
st.subheader('Explore Individual Responses')
selected_client = st.selectbox('Select a Client ID', options=filtered_df['Client ID'].unique())
client_data = filtered_df[filtered_df['Client ID'] == selected_client].iloc[0]
st.write(f"Sentiment: {client_data['Sentiment']}")
st.write(f"Theme: {client_data['Theme']}")
st.write(f"Feedback: {client_data['Feedback']}")
