# Automating Multi-Platform Restaurant Booking Management with Apache Airflow

## 📌 Project Overview
This project automates the management of restaurant bookings across multiple platforms (**TheFork, Quandoo, OpenTable, SevenRooms**) using **Apache Airflow** to orchestrate ETL workflows. The system extracts reservation data from **API endpoints**, standardizes it, and stores it in a **PostgreSQL** database for centralized tracking. 
A **Tableau** provides insights into booking trends, occupancy rates, and platform performance.

Additionally, this project includes **FindTables**, a **Django-based restaurant booking system** that simulates real-world table reservations. Users can make and manage reservations through API endpoints and a **jQuery-based frontend**.

---

## 🚀 Features

✔ **Automated ETL Pipeline** – Extracts, transforms, and loads booking data from multiple platforms.  
✔ **Centralized Database** – Stores structured reservation data in **PostgreSQL/MySQL**.  
✔ **Data Standardization** – Ensures uniformity in booking data across platforms.  
✔ **Interactive Dashboard** – Analyzes booking trends, occupancy rates, and platform performance.  
✔ **Django-Based Booking System** – Simulates restaurant reservations via API endpoints.  
✔ **Webhook Simulation** – Simulates real-time booking updates from platforms.  
✔ **Cloud-Ready Architecture** – Can be deployed on **AWS, Docker, or local environments**.  

---

## 📁 Project Structure

```
📂 restaurant-booking-management  
│── 📂 airflow/                   # Apache Airflow DAGs for ETL workflows  
│── 📂 backend/                   # Django-based FindTables booking system  
│── 📂 database/                  # PostgreSQL/MySQL schema and scripts  
│── 📂 dashboards/                # Tableau/Power BI dashboard files  
│── 📂 scripts/                   # Data extraction & transformation scripts  
│── 📂 frontend/                  # jQuery-based booking interface  
│── 📜 README.md                  # Project documentation  
│── 📜 requirements.txt           # Python dependencies  
│── 📜 docker-compose.yml         # Docker setup for deployment  
```

---

## 🛠️ Tech Stack

| Component           | Technology Used |
|---------------------|----------------|
| **Orchestration**  | Apache Airflow  |
| **Backend**        | Django & DRF |
| **Database**       | PostgreSQL|
| **Data Processing** | Pandas, Python |
| **Visualization**  | Tableau |
| **Frontend**       | jQuery, HTML, CSS |
| **Deployment**     | Docker, AWS |

---

## 📌 How It Works

### 1️⃣ Extract Booking Data
- Airflow DAGs extract **mock booking data** from TheFork, Quandoo, OpenTable, and SevenRooms APIs.
- Data is fetched in different formats (JSON, CSV) and standardized.

### 2️⃣ Transform & Standardize
- Python scripts clean, validate, and standardize booking data.
- Ensures uniformity in fields like `order_id`, `customer_name`, `booking_time`, `restaurant_id`, etc.

### 3️⃣ Load into Database
- Standardized data is stored in **PostgreSQL/MySQL**.
- Enables **efficient querying** and integration with the dashboard.

### 4️⃣ Dashboard Analysis
- Tableau/Power BI visualizes:
  - **Booking trends** across platforms
  - **Occupancy rates** per restaurant
  - **Platform performance** comparisons

### 5️⃣ FindTables - Django-Based Booking System
- Allows users to **simulate restaurant bookings** via API.
- Stores bookings in the central database.

### 6️⃣ Webhook Simulation
- Simulates real-time booking updates from different platforms.
- Updates database whenever a **reservation is modified or canceled**.

## 📜 License
This project is licensed under the **MIT License**.

---

## 📩 Contact & Contributions
- **Author:** Paritosh & Ayurma  
- **Contributions:** PRs are welcome! Open an issue for suggestions.  
