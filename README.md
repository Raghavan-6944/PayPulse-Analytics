# 📊 PAY Pulse Analytics

A **PhonePe Pulse**-inspired interactive data analytics dashboard built with **Streamlit**, **MySQL**, and **Plotly**. Explore transaction and user data across all Indian states with a stunning dark-themed choropleth map interface.

---

## 🖼️ Overview

PAY Pulse Analytics replicates the look and feel of the PhonePe Pulse Explore Data dashboard. It lets you:

- Visualize **UPI transaction volumes and amounts** state-wise on an interactive India map
- Analyze **registered PhonePe users and app opens** by state and district
- Browse **top device brands**, **top districts**, and **top postal codes** for any year/quarter
- Toggle between **Transactions** and **Users** domains with real-time data refresh

---

## 🗂️ Project Structure

```
phonepe_project/
│
├── dashboard/
│   ├── app.py                  # Main Streamlit application
│   └── india_state_geo.json    # GeoJSON for India state boundaries
│
├── extraction/
│   └── extract_data.py         # Parses PhonePe Pulse JSON files → MySQL
│
├── database/
│   └── schema.sql              # MySQL table definitions
│
├── dataset/                    # Raw PhonePe Pulse data (JSON files)
│   ├── aggregated/
│   │   ├── transaction/
│   │   └── user/
│   ├── map/
│   │   ├── transaction/
│   │   └── user/
│   └── top/
│       └── transaction/
│
└── analysis/
    └── analysis.ipynb          # Exploratory Data Analysis notebook
```

---

## 🛠️ Tech Stack

| Layer        | Technology                     |
|--------------|-------------------------------|
| Frontend UI  | Streamlit + Custom CSS         |
| Visualizations | Plotly Express / Graph Objects |
| Backend DB   | MySQL                          |
| Data Source  | PhonePe Pulse GitHub Dataset   |
| Language     | Python 3.x                     |

---

## 📦 Prerequisites

- Python 3.8+
- MySQL Server (running locally)
- PhonePe Pulse dataset cloned into the `dataset/` folder

---

## ⚙️ Installation & Setup

### 1. Clone / Download the Project

```bash
git clone <your-repo-url>
cd phonepe_project
```

### 2. Install Python Dependencies

```bash
pip install streamlit pandas mysql-connector-python plotly
```

### 3. Set Up the MySQL Database

Open MySQL and create the database and tables:

```sql
CREATE DATABASE phonepe_db;
USE phonepe_db;

CREATE TABLE aggregated_transaction (
    state            VARCHAR(100),
    year             INT,
    quarter          INT,
    transaction_type VARCHAR(100),
    transaction_count BIGINT,
    transaction_amount DOUBLE
);

CREATE TABLE aggregated_user (
    state      VARCHAR(100),
    year       INT,
    quarter    INT,
    brand      VARCHAR(100),
    count      BIGINT,
    percentage DOUBLE
);

CREATE TABLE map_transaction (
    state    VARCHAR(100),
    year     INT,
    quarter  INT,
    district VARCHAR(100),
    count    BIGINT,
    amount   DOUBLE
);

CREATE TABLE map_user (
    state            VARCHAR(100),
    year             INT,
    quarter          INT,
    district         VARCHAR(100),
    registered_users BIGINT,
    app_opens        BIGINT
);

CREATE TABLE top_transaction (
    state       VARCHAR(100),
    year        INT,
    quarter     INT,
    entity_name VARCHAR(200),
    count       BIGINT,
    amount      DOUBLE
);
```

### 4. Download the PhonePe Pulse Dataset

```bash
git clone https://github.com/PhonePe/pulse.git dataset
```

### 5. Configure Database Credentials

Open `extraction/extract_data.py` and `dashboard/app.py` and update the MySQL credentials:

```python
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="YOUR_PASSWORD",   # ← Update this
    database="phonepe_db"
)
```

### 6. Extract and Load Data into MySQL

```bash
cd extraction
python extract_data.py
```

This will parse all JSON files from the `dataset/` folder and load them into the MySQL tables. You should see:

```
Aggregated Transaction Done
Aggregated User Done
Map Transaction Done
Map User Done
Top Transaction Done
All Data Inserted Successfully
```

### 7. Launch the Dashboard

```bash
cd dashboard
streamlit run app.py
```

Open your browser at **http://localhost:8501**

---

## 🎯 Features

### 🔷 Transactions View
- **India Choropleth Map** — State-wise transaction count heatmap
- **Transaction Summary** — Total count, total payment value, average transaction value
- **Category Breakdown** — Merchant Payments, Peer-to-Peer, Recharge & Bill Payments, etc.
- **Donut Chart** — Transaction category distribution
- **Ranked Lists** — Top 10 States, Districts, and Postal Codes by transaction volume

### 🔶 Users View
- **India Choropleth Map** — State-wise registered user heatmap
- **User Summary** — Total registered users & app opens
- **Device Brand Bar Chart** — Top 10 smartphone brands used by PhonePe users
- **Ranked Lists** — Top 10 States and Districts by registered users

### 🎛️ Filters
- **Domain Toggle** — Switch between Transactions / Users
- **Year Selector** — Filter by year
- **Quarter Selector** — Q1, Q2, Q3, Q4

---

## 🗄️ Database Schema

| Table                   | Key Columns                                                   |
|-------------------------|---------------------------------------------------------------|
| `aggregated_transaction` | state, year, quarter, transaction_type, count, amount        |
| `aggregated_user`        | state, year, quarter, brand, count, percentage               |
| `map_transaction`        | state, year, quarter, district, count, amount                |
| `map_user`               | state, year, quarter, district, registered_users, app_opens  |
| `top_transaction`        | state, year, quarter, entity_name, count, amount             |

---

## 📊 Data Source

This project uses the open-source **[PhonePe Pulse](https://github.com/PhonePe/pulse)** dataset, which contains transaction and user data across Indian states from 2018 onwards, published quarterly by PhonePe.

---

## 🚀 Running the EDA Notebook

```bash
cd analysis
jupyter notebook analysis.ipynb
```

---

## 📝 Notes

- The dashboard connects to a **local MySQL instance** — ensure MySQL is running before launching Streamlit.
- The GeoJSON file (`india_state_geo.json`) must remain in the `dashboard/` folder alongside `app.py`.
- State name matching between MySQL data and GeoJSON uses the `ST_NM` property key.

---

## 👤 Author

Developed as part of the **GUVI Last Batch Implementation Project**.
