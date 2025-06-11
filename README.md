# Inventory-Management-API

inventory management

tables-
users
branches
items
item_stock
transactions(tracks who takes what from where)
orders from other branches
orders
discounts_per_quantity

User-

ID | first_name | last_name | phone_number | branch_id | password | role

Branch-

ID | name | address | manager_id | phone_number

Item-

ID | name | category | description | image | createdAt

Item_stock - 

ID | branch_id | item_id | quantity | updatedAt

Transactions-

ID | user_id | item_id | branch_id | type(send/receive/transfer?) | quantity | description | createdAt

Orders-

ID | client_id | user_id | status | delivery_date | createdAt | updatedAt 

Order_Items - 

ID | order_id | item_id | quantity 

Client-

ID | address | name | phone | createdAt

Price -

ID |  item_id | quantity(min quantity for the price) | price | updatedAt
