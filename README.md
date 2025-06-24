# Inventory-Management-API

========USER=========

- get: by_id, all
- post: create
- delete: delete_by_id
- patch: update by some paramaters
- put: update by all paramaters

========Branch=========

- get: by_id, all, manager, transactions, all items in stock, users
- post: create
- delete: delete_by_id
- patch: remove manager, assign manager

========Category=========

- get: all
- post: create
- delete: by id, by name

========Client=========

- get: by_id, all, orders_by_cliend_it, by phone, by full name
- post: create
- patch: update some parameters

========Item=========

- get: by_id, all, stocks, price by id and amount, all prices by id
- post: create
- patch: update(for updating quantity in stock, prices)

========Order=========

- get: by_id, all, by date, by status, by user, by client, get order_items, price(need to add to db)
- post: create(create order items list, calculate price for all orderitem, create order with orderitems and sum prices into order price)
- patch: change_status

========Transaction=========

- get: by_id, all, by date, by status, by user, by branch
- post: create(sending transactions will remove from stock, receiving transaction will add to stock)

!!!!!At least one complex endpoint (e.g., advanced search, reports, statistics)[need to ask sean]!!!!

yehu - √item, order, transaction
lara - user branch, category, client
