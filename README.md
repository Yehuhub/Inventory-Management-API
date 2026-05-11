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
JWT_SECRET=your-long-random-secret-at-least-32-chars
```

Make sure the database you specify in DB_NAME already exists in your PostgreSQL server.

## ▶️ Run the app

**Option A — Docker (recommended)**

Make sure Docker is running, then:

```bash
docker compose up --build
```

This will start a PostgreSQL container and the API container. The API is available at `http://localhost:5001`. On subsequent runs you can omit `--build` unless you changed the code.

To stop:

```bash
docker compose down
```

**Option B — Locally**

Make sure PostgreSQL is running and `DB_IP` in your `.env` points to your local instance, then:

```bash
flask run
```

## 🌐 Base URL

http://localhost:5000/

---

## 🔐 Authentication

All endpoints except `/api/auth/login` require a JWT token.

**Step 1 — Login**

```
POST /api/auth/login
Content-Type: application/json

{ "phone_number": "your_phone_number" }
```

Returns:

```json
{ "token": "<jwt>", "user_id": 1, "role": "manager" }
```

**Step 2 — Include the token on every request**

```
Authorization: Bearer <jwt>
```

Endpoints that create, update, or delete data (items, branches, users, categories, export/import) are restricted to **managers**. Requests from employees to those endpoints will receive a `403 Forbidden` response.

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
