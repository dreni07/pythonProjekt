import streamlit as st
import plotly.express as pl
import pandas as pd

# Sample data
data = {
    'Store Name': ['Store A', 'Store B', 'Store C'],
    'Sales': [100, 200, 300]
}
sorting_values = pd.DataFrame(data)

colors = ['#001F3F', '#FFC107']

figure = pl.pie(
    sorting_values,
    names='Store Name',
    values='Sales',
    title='Most Sales',
    color_discrete_sequence=colors
)

figure.update_layout(
    width=800,
    height=600
)

st.plotly_chart(figure, use_container_width=False)