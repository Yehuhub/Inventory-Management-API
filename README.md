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

## 🔹 Users

**Base URL:** `/api/users`

| Method | Endpoint                  | Description               |
|--------|---------------------------|---------------------------|
| GET    | `/`                       | Get all users             |
| GET    | `/<user_id>`              | Get user by ID            |
| POST   | `/`                       | Create a new user         |
| PATCH  | `/<user_id>`              | Update user fields        |
| DELETE | `/<user_id>`              | Delete user               |

---

## 🔹 Clients

**Base URL:** `/api/clients`

| Method | Endpoint                                         | Description                        |
|--------|--------------------------------------------------|------------------------------------|
| GET    | `/`                                              | Get all clients                    |
| GET    | `/<client_id>`                                   | Get client by ID                   |
| GET    | `/<client_id>/orders`                            | Get orders of a client             |
| GET    | `/phone/<phone_number>`                          | Find client by phone               |
| GET    | `/name/<first_name>/<last_name>`                 | Find client by full name           |
| POST   | `/`                                              | Create new client                  |
| PATCH  | `/<client_id>`                                   | Update client details              |
| DELETE | `/<client_id>`                                   | Delete client                      |

---

## 🔹 Categories

**Base URL:** `/api/categories`

| Method | Endpoint                                         | Description                          |
|--------|--------------------------------------------------|--------------------------------------|
| GET    | `/`                                              | Get all categories                   |
| GET    | `/<category_id>`                                 | Get category by ID                   |
| GET    | `/name/<name>`                                   | Get category by name                 |
| GET    | `/<category_id>/items`                           | Get items by category ID             |
| GET    | `/name/<name>/items`                             | Get items by category name           |
| POST   | `/`                                              | Create new category                  |
| PATCH  | `/<category_id>`                                 | Update category                      |
| DELETE | `/<category_id>`                                 | Delete category by ID                |
| DELETE | `/name/<name>`                                   | Delete category by name              |

---

## 🔹 Branches

**Base URL:** `/api/branches`

| Method | Endpoint                  | Description           |
|--------|---------------------------|-----------------------|
| GET    | `/`                       | Get all branches      |
| GET    | `/<branch_id>`            | Get branch by ID      |
| POST   | `/`                       | Create new branch     |
| PATCH  | `/<branch_id>`            | Update branch         |
| DELETE | `/<branch_id>`            | Delete branch         |

---

## 🔹 Items

**Base URL:** `/api/items`

| Method | Endpoint                  | Description           |
|--------|---------------------------|-----------------------|
| GET    | `/`                       | Get all items         |
| GET    | `/<item_id>`              | Get item by ID        |
| POST   | `/`                       | Create new item       |
| PATCH  | `/<item_id>`              | Update item           |
| DELETE | `/<item_id>`              | Delete item           |

---

## 🔹 Prices

**Base URL:** `/api/prices`

| Method | Endpoint                             | Description                      |
|--------|--------------------------------------|----------------------------------|
| GET    | `/`                                  | Get all prices                   |
| GET    | `/<item_id>/<branch_id>`             | Get item price in a branch       |
| POST   | `/`                                  | Add new price                    |
| PATCH  | `/<item_id>/<branch_id>`             | Update existing price            |

---

## 🔹 Orders

**Base URL:** `/api/orders`

| Method | Endpoint              | Description                    |
|--------|-----------------------|--------------------------------|
| GET    | `/`                   | Get all orders                 |
| GET    | `/<order_id>`         | Get order by ID                |
| POST   | `/`                   | Create a new order with items  |
| DELETE | `/<order_id>`         | Delete order                   |

**POST Body Example:**
```json
{
  "client_id": 1,
  "user_id": 2,
  "items": [
    {"item_id": 10, "quantity": 2},
    {"item_id": 7, "quantity": 1}
  ]
}
```
---

## 🔹 Transactions

**Base URL:** `/api/transactions`

| Method | Endpoint                | Description             |
|--------|-------------------------|-------------------------|
| GET    | `/`                     | Get all transactions    |
| GET    | `/<transaction_id>`     | Get transaction by ID   |
| POST   | `/`                     | Create new transaction  |
| DELETE | `/<transaction_id>`     | Delete transaction      |

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
