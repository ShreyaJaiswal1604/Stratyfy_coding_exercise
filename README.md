---

# 🍦 Stratyfy Coding Exercise 🍦

---

## **🎯 Project Overview**

Welcome to the **Stratyfy Coding Exercise**! This project simulates a real-world scenario of managing **sales data for an ice cream parlor**. The goal is to:

1. **Set up a dynamic database** to store JSON data.  
2. **Build API endpoints** using FastAPI to access and analyze data.  
3. **Create an engaging interactive dashboard** with Streamlit for uploading, viewing, and analyzing sales data.

---
## **Architecture Diagram** 🏗️✨

Below is the architecture diagram illustrating the structure and flow of the project:

![Stratyfy Architecture](https://github.com/ShreyaJaiswal1604/Stratyfy_coding_exercise/blob/main/images/stratify-architectur.jpeg)

The diagram provides an overview of the interactions between the components:
- **Streamlit Frontend**: 🎨 Interactive UI for uploading data, viewing reports, and performing analytics.
- **FastAPI Backend**: 🚀 API for fetching and processing data.
- **Database**: 💾 PostgreSQL used for data storage and schema management.
- **Visualizations**: 📊 Revenue and volume charts are dynamically generated for sundaes.

---
## **🛠 Tools and Technologies Used**

- **Backend**:
   - 🚀 **FastAPI**: Framework for building API endpoints.
   - 🗄 **SQLAlchemy**: Database ORM for schema management.
   - 🛢 **PostgreSQL**: Relational database for data storage.

- **Frontend**:
   - 🎨 **Streamlit**: Framework for creating interactive dashboards.
   - 📊 **Matplotlib** and **Seaborn**: Visualization tools for analytics.

- **Environment Management**:
   - 🐍 **Poetry**: For dependency and environment management.

- **Other Tools**:
   - 🔗 **Requests**: API call handling.
   - 📂 **dotenv**: Environment variable management.

---

## **📊 Project Requirements**

The project requires two JSON data files:  
1. **`sundaes.json`**: Contains the menu of available sundaes.  
2. **`sales.json`**: Contains transaction details for each sundae, with `timestamp` in Unix format.

### **Tasks**:
- Load the JSON data into a **PostgreSQL database** dynamically.
- Set up two **FastAPI endpoints**:
   - `GET /sundaes`: Retrieve all sundaes.
   - `GET /sundaes/{id}`: Retrieve sundae details, including:
     - `volume`: Number of sundaes sold.  
     - `revenue`: Total revenue for the sundae.  

- Build a **Streamlit Dashboard** with features for:
   - Uploading and loading JSON data into the database.
   - Viewing the data tables interactively.
   - Analyzing and visualizing sundae sales revenue.

---

## **📁 Folder Structure**

Here’s the well-organized project structure:

```plaintext
Stratyfy_coding_exercise/
├── api/                        # FastAPI backend
│   ├── api.py                  # API endpoints
│   ├── database.py             # Database setup
│   └── schema.py               # Schema utilities
│
├── streamlit/                  # Streamlit frontend dashboard
│   ├── pages/                  # Multi-page Streamlit app
│   │   ├── 01_load_data.py         # Upload JSON data
│   │   ├── 02_view_data.py         # View database tables
│   │   ├── 03_revenue_analysis_by_id.py # Revenue analysis by sundae ID
│   │   └── 04_revenue_report.py    # Comprehensive revenue report
│   ├── database.py             # Database utility for Streamlit
│   ├── home.py                 # Main entry point for Streamlit
│   └── utils.py                # Helper functions
│
├── webapp/                     # Backend models and data
│   ├── data/                   # JSON files
│   │   ├── sales.json
│   │   ├── sundaes.json
│   │   └── sundaes_OG.json
│   ├── database.py             # SQLAlchemy setup
│   ├── models.py               # Database ORM models
│   └── __init__.py
│
├── .env                        # Environment variables for DB credentials
├── exercise.py                 # FastAPI server entry point
├── poetry.lock                 # Dependency lock file
├── pyproject.toml              # Project dependencies
└── README.md                   # Project documentation
```


---

### **⚙️ Setup and Implementation**

Follow these steps to set up and run the project seamlessly:

---

### **1. Clone the Repository**

Begin by cloning the project repository to your local machine:

```bash
git clone https://github.com/yourusername/Stratyfy_coding_exercise.git
cd Stratyfy_coding_exercise
```
---

### **2. Install Dependencies**

Ensure Poetry is installed on your system. If not, install it by running:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```
Then install the project dependencies:

```bash
poetry install
```
---

### **3. Setup Environment Variables**
Create a .env file in the root directory of the project to configure the database credentials. Add the following:

```bash
DB_USER=your_username          # PostgreSQL username
DB_PASSWORD=your_password      # PostgreSQL password
DB_HOST=localhost              # Database host
DB_PORT=5432                   # Database port
DB_NAME=your_database_name     # Database name

```
Replace your_username, your_password, and your_database_name with your PostgreSQL configuration.

---
### **4. Initialize the Database**

Make sure your PostgreSQL server is running. Load the database schema and data using Streamlit:
1. Start the Streamlit app to upload JSON data:

```bash
cd streamlit
poetry run streamlit run pages/01_load_data.py
```

2. Use the UI to upload sundaes.json and sales.json into the database.
3. Once the upload is successful, the database tables (sundaes and sales) will be created and populated.

---
### **5. Start the FastAPI Server**

Launch the FastAPI server to access the API endpoints:

```bash
poetry run uvicorn api.api:app --reload
```
API Endpoints:

- GET /sundaes
  Returns all available sundaes.

- GET /sundaes/{id}
  Returns specific sundae details with:

- volume (number of sundaes sold)
  revenue (total revenue for the sundae).
  
- API Documentation:
  Open the Swagger UI at http://127.0.0.1:8000/docs to explore and test endpoints.
---
### **6. Launch the Streamlit Dashboard**

Run the Streamlit dashboard for interactive data management and analytics:

```bash
cd streamlit
poetry run streamlit run home.py

```
#### Streamlit Pages
- Home: Project overview and navigation.
- Upload and Load Data (01_load_data.py): Upload JSON files and load data into the database.
- View Data (02_view_data.py): Select and view table data dynamically.
- Revenue Analysis (By ID) (03_revenue_analysis_by_id.py): Analyze revenue and volume for specific sundae IDs.
- Revenue Report (04_revenue_report.py): Generate an interactive revenue dashboard for all sundaes.

---

### **7. Workflow Summary**

- Upload JSON Data: Use the Upload and Load Data page to populate the database.
- API Endpoints: Use FastAPI endpoints for data access.
- Interactive Analytics:
- View specific sundae revenue via Revenue Analysis.
- Generate full sundae revenue reports using Revenue Report.

---
### **8. Testing**

API Testing
1. Open the API documentation:
```bash
cd streamlit
poetry run streamlit run home.py](http://127.0.0.1:8000/docs
```
- use tools like Postman or curl to test the endpoints:
  
2. Streamlit Testing
- Run all Streamlit pages and validate the functionality:

```bash
poetry run streamlit run home.py
```
---
### 🎉  **9. Conclusion**
This project provides an end-to-end solution for uploading data, managing a database, and analyzing revenue through APIs and an interactive Streamlit UI. You can customize it further as needed for real-world scenarios.
