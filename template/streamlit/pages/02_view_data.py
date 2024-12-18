import streamlit as st
from api.database import get_db
from sqlalchemy import text
from contextlib import closing

# Page Title
st.title("🔍 View Loaded Data")

# Function to fetch all table names from the database
def fetch_tables(db):
    try:
        result = db.execute(
            text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
        )
        return [row[0] for row in result]
    except Exception as e:
        st.error(f"⚠ Error fetching table names: {e}")
        return []

# Function to fetch table data
def fetch_table_data(table_name, db):
    try:
        result = db.execute(text(f"SELECT * FROM {table_name}"))
        return [dict(row._mapping) for row in result]
    except Exception as e:
        st.error(f"⚠ Error fetching data from table '{table_name}': {e}")
        return []

# Fetch the list of tables
st.info("Fetching available tables from the database...")
with closing(next(get_db())) as db:  # Use next() to get the session
    tables = fetch_tables(db)

# If tables are available
if tables:
    st.success(f"✅ Found {len(tables)} table(s) in the database.")
    
    # Table selection box
    selected_table = st.selectbox(
        "📋 Select Table to View:",
        tables,
        help="Choose the table you want to display from the database."
    )

    # Button to view the selected table data
    if st.button("📊 View Table Data"):
        with st.spinner(f"Loading data for table: **{selected_table}**..."):
            with closing(next(get_db())) as db:  # Use next() to get the session
                data = fetch_table_data(selected_table, db)
                
                if data:
                    st.success(f"✅ Successfully loaded data from table: **{selected_table}**")
                    st.dataframe(data)  # Display data in a table format
                else:
                    st.warning(f"⚠ Table **{selected_table}** is empty.")
else:
    st.warning("⚠ No tables found. Please upload and load data first.")

# Footer
st.markdown("---")
st.caption("🔧 Use the **Load Data** page to upload and load JSON data into the database.")
