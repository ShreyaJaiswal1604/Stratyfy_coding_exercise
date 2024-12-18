import streamlit as st

st.set_page_config(page_title="Sundae Data Management", layout="wide")

st.title("Welcome to Sundae Data Management System 🍨")
st.write("Navigate through the sidebar to perform the following tasks:")

st.markdown("""
1. **Load Data**: Upload and load JSON files into the database.
2. **View Data**: View tables and their contents.
3. **Revenue Analysis**: Analyze volume and revenue of sundaes.
""")
