# Automated ETL Pipeline for Multi-Platform Restaurant Booking Data Integration and Analytics

## Project Overview

Restaurant today relies on several booking platforms such as The Fork, Quandoo, Open Table, and Design My Nights. When a reservation is made through any of these channels, restaurants receive an immediate email notification, and each platform offers a dedicated web interface where current, past, and future bookings can be viewed. This system allows for real-time updates on guest reservations and historical data, which can be essential for managing capacity and planning operations. 

While these platforms are primarily booking tools—not full management systems—restaurants migrate the booking data into a centralized management system for operational efficiency. 

How do the restaurant do that? 

A common guess will be through APIs!

These booking platforms do offer APIs that can theoretically integrate with popular restaurant management systems.

Many restaurants(small and medium-sized) opt to manually migrate the incoming reservation data into their internal management system.

It is not ideal-- but hey, it works!

But we all know, human error and lack of a automated, centralised system severely hampers analytics capabilities, and strategic decision-making. 

This project implements an ETL pipeline orchestrated by Apache Airflow, designed to automate the whole process without human intervention. The pipeline seamlessly integrates reservation data from multiple platforms into a single, centralised warehouse.  </br>

Since,these booking platform do not provide API endpoints unless you are their customers, I have custom-built API endpoints that closely resembles their endpoints & webhooks, providing realistic representations of data structures and responses from popular reservation platforms such as TheFork, Quandoo, OpenTable, and SevenRooms.

Additionally, the project features an interactive Tableau dashboard providing real-time analytics, offering clear insights into booking trends, reservation patterns, and platform performance metrics to support informed business decisions.

Additionally, this project includes **FindTables**, a basic **Django-based restaurant booking system** that simulates real-world table reservations. Users can make and manage reservations through API endpoints and a **frontend**.
```mermaid
flowchart TB


    subgraph Begin
    direction TB
        A["Customer makes a<br/>reservation <br/> on Booking <br/> Platform"] --> 
        B["Webbhook:<br\> POST request <br/> to Apache Airflow API"] --> 
        C["<br/>Initiates Airflow pipeline"] 
    end 
    
    %% Three nodes arranged horizontally with manual line breaks for wrapping
    subgraph Pipeline
    direction LR
        D["Extract<br/>reservation data"] --> 
        E["Transform, clean,<br/>and standardize <br/>data"] --> 
        F["Load data<br/>into Centralized <br/> Data Warehouse"] 
        
    end

    subgraph Analytics
    direction LR
    G["Interactive Tableau dashboard<br/>provides updates <br/>in real-time"]
    end

    %% Subgraph for vertical flow (top-to-bottom)
    
    Begin --> Pipeline --> Analytics
```

### Airflow Pipeline

<div align="center">
  <img src="https://github.com/user-attachments/assets/98eb1307-1f0a-4461-9231-c99e174b46ae" alt="Project Image">
</div>

---

## Features

**Automated ETL Pipeline** – Extracts, transforms, and loads booking data from multiple platforms.  
**Centralized Database** – Stores structured reservation data in **PostgreSQL/MySQL**.  
**Data Standardization** – Ensures uniformity in booking data across platforms.  
**Interactive Dashboard** – Analyzes booking trends, occupancy rates, and platform performance.  
**Django-Based Booking System** – Simulates restaurant reservations via API endpoints.  
**Webhook Simulation** – Simulates real-time booking updates from platforms.  
**Cloud-Ready Architecture** – Can be deployed on **AWS, Docker, or local environments**.  

---

## Project Structure

```
📂 restaurant-booking-management  
│── 📂 dags/                   # Apache Airflow DAGs for ETL workflows
│── 📂 dags/helpers            # Data extraction & transformation scripts    
│── 📂 FindTables/             # Django-based FindTables booking system  
│── 📂 queries/                # PostgreSQL schema and scripts  
│── 📂 dashboards/             # Tableau dashboard files  
│── 📜 README.md                  # Project documentation  

```

---

## Tech Stack

| Component           | Technology Used |
|---------------------|----------------|
| **Orchestration**  | Apache Airflow  |
| **Backend**        | Django & DRF |
| **Database**       | PostgreSQL|
| **Data Processing** | Pydantic, Pandas, Python |
| **Visualization**  | Tableau |
| **Frontend**       | jQuery, HTML, CSS |
| **Deployment**     | Docker, AWS |

---

## How It Works

### Extract Booking Data
- Airflow DAGs receives **reservation data** from custom built webhooks in Django.
- Data is fetched in different formats (JSON, CSV) and standardized.

### Transform & Standardize
- Python scripts clean, validate, and standardize booking data.
- Ensures uniformity across seperate databases. 

### Load into Database
- Standardized data is stored in **PostgreSQL**.
- Enables **efficient querying** and integration with the dashboard.

### Dashboard Analysis
- Tableau visualizes:
  - **Booking trends** across platforms
  - **Occupancy rates** per restaurant
  - **Platform performance** comparisons

### FindTables - Django-Based Booking System
- Allows users to **simulate restaurant bookings** via API.
- Stores bookings in the central database.

### Webhook Simulation
- Simulates real-time booking updates from different platforms.
- Updates database whenever a **reservation is modified or canceled**.

## 📜 License
This project is licensed under the **MIT License**.

