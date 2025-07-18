# 📦 Inventory Management System – API Documentation

This is a RESTful API for managing an inventory system, including users, clients, branches, items, prices, orders, and transactions. It allows for full CRUD operations on all entities, supports CSV import for items and categories, and exports data from any table to Excel format.

The API is built with Flask and SQLAlchemy and is designed for local development or deployment using PostgreSQL.

---

## ⚙️ Setup

To run the project locally, follow these steps:

1. **Install the required dependencies**  
   Make sure you have Python installed, then run:

   ```bash
   pip install -r requirements.txt
   ```
Configure your environment variables
Create a .env file in the root directory with the following content:
```bash
DB_USER=your_username
DB_PASSWORD=your_password
DB_IP=localhost
DB_PORT=5432
DB_NAME=your_database_name
CSV_IMPORT_FILE_PATH=path/to/your/file.csv
```
Make sure the database you specify in DB_NAME already exists in your PostgreSQL server.

Run the app
Start the Flask application with:
```bash
flask run
```

## 🌐 Base URL
http://localhost:5000/

---

## 📚 Endpoints Overview

- [🔹 Users](#users)
- [🔹 Clients](#clients)
- [🔹 Categories](#categories)
- [🔹 Branches](#branches)
- [🔹 Items](#items)
- [🔹 Prices](#prices)
- [🔹 Orders](#orders)
- [🔹 Transactions](#transactions)
- [📥 CSV Import](#csv-import)
- [📤 Excel Export](#excel-export)

---

## 📘 API Docs

You can view and test all API endpoints using the Postman documentation below:

👉 [API Documentation & Tester on Postman](https://documenter.getpostman.com/view/41474192/2sB34fkfnw)

This link allows you to explore all the available endpoints, see example requests and responses, and even test them directly if your server is running locally (`http://127.0.0.1:5000/`).

---

## 🧩 Complex Endpoints

Some endpoints in this system involve multiple operations and affect several tables behind the scenes:

- **POST `/api/orders`**  
  Creates a new order and automatically creates entries in the `order_items` table for each item in the order.

- **POST `/api/transactions`**  
  Creates a transaction and automatically updates the item stock in the related branch:  
  - If it's a `"receive"` transaction, stock is increased (or created if missing).  
  - If it's a `"send"` transaction, stock is decreased after validating availability.

---

## 📥 CSV Import

**Endpoint:** `/api/csv`  
**Method:** `GET`  
Imports items and categories from a CSV file located in the configured path.

**Expected CSV format:**
item_name,item_description,category_name


---

## 📤 Excel Export

**Endpoint:** `/utils/export/<table_name>`  
**Method:** `GET`  
Exports a specific table to an Excel `.xlsx` file. The file is saved in the `exported_excels/` folder.

**Supported table names:**

- `users`  
- `clients`  
- `branches`  
- `categories`  
- `items`  
- `item_stocks`  
- `orders`  
- `order_items`  
- `prices`  
- `transactions`


---

## 👥 Contributors

- **Lara Duek** - laradu@edu.jmc.ac.il
- **Yehu Raccah** - yehura@edu.jmc.ac.il
