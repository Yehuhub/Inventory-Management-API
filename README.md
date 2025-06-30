# Inventory-Management-API

==================================TODO===================================

    -   add SQLAlchemyError exception handling on post method to notify the reason why an object was not created
    -   ask if a router that returns a list returns an empty list or not found
    -   ask/think about a complex endpoint
    -   make it so it reads items and categories from csv
    -   export database to excel
    -   route testing:
        -   yehu: users, branch, category
        -   lara: client, item, order, transaction

==================================================================================================
!!!!!At least one complex endpoint (e.g., advanced search, reports, statistics)[need to ask sean]!!!!
--------order request format------------
{
"order_items":[
{"item_id": 1, "quantity": 3},
{"item_id": 5, "quantity": 20},
{"item_id": 4, "quantity": 11},
],
"user_id": 5,
"client_id": 1,

}
delivery date and status will be defaulted, status to pending and delivery_date to today+14 days
