import streamlit as st
from pathlib import Path
from database import Database
from webapp.models import Sundae, Sale, Employee  # Import your model classes
import os
import time  # To simulate loading time

# Page title with style
st.title("📂 Upload and Load JSON Data")
st.write("Use this page to upload a JSON file and load it into the database.")

# Initialize database connection
db_handler = Database()

# File uploader
uploaded_file = st.file_uploader("🔼 Upload a JSON file", type=["json"], help="Only JSON files are supported.")

# Display instructions if no file is uploaded
if not uploaded_file:
    st.info("Please upload a valid JSON file to continue.")
else:
    # File uploaded message
    st.success(f"✅ File '{uploaded_file.name}' uploaded successfully!")

    # Add a button to trigger data loading
    if st.button("🚀 Load Data into Database"):
        with st.spinner("📊 Processing file and loading data..."):
            try:
                # Parse the uploaded JSON file
                file_path = f"/tmp/{uploaded_file.name}"
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                # Display file details
                st.write("### File Information")
                st.json({"File Name": uploaded_file.name, "Size (KB)": round(len(uploaded_file.getbuffer()) / 1024, 2)})

                # Table name logic based on file name
                table_name = Path(uploaded_file.name).stem.lower()
                st.write(f"🛠 Detected Table Name: **{table_name}**")

                # Dynamically determine the model class
                model_class = None
                if table_name == "sundaes":
                    model_class = Sundae
                elif table_name == "sales":
                    model_class = Sale
                elif table_name == "employees":
                    model_class = Employee
                else:
                    st.error("⚠ Unknown table. Supported tables are 'sundaes' and 'sales'.")
                    st.stop()

                # Simulate a slight delay for better user experience
                time.sleep(1)

                # Load the JSON data into the database
                db_handler.load_bulk_data(Path(file_path), model_class)

                # Success message with a balloon animation
                st.success(f"🎉 Data loaded successfully into table **'{table_name}'**!")
                st.balloons()

            except Exception as e:
                st.error(f"❌ Error while loading data: {e}")
            finally:
                db_handler.close()
                st.write("🔒 Database connection closed.")

# Footer with style
st.markdown("---")
st.markdown("💡 **Tip:** Upload a valid JSON file named `sundaes.json` or `sales.json` for successful loading.")
