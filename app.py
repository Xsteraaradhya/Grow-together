import streamlit as st

# Set page configuration
st.set_page_config(page_title="My Streamlit App", page_icon=":rocket:", layout="wide")

# Title and description
st.title("Welcome to My Streamlit App")
st.write("This is a sample Streamlit app deployed via GitHub and Streamlit Cloud.")

# Sample content
st.header("About")
st.write("This app demonstrates a basic Streamlit application connected to GitHub.")
name = st.text_input("Enter your name:", "")
if name:
    st.write(f"Hello, {name}! Welcome to the app!")

# Example of a simple button and interaction
if st.button("Click Me"):
    st.balloons()
    st.write("You clicked the button!")

# Example of a data visualization
st.header("Sample Data Visualization")
import pandas as pd
import numpy as np
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['A', 'B', 'C']
)
st.line_chart(chart_data)

# Sidebar for additional options
st.sidebar.header("Settings")
option = st.sidebar.selectbox("Choose an option:", ["Option 1", "Option 2", "Option 3"])
st.sidebar.write(f"Selected: {option}")