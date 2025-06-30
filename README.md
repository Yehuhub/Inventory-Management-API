# Inventory-Management-API

==================================IMPROVEMENTS THAT CAN BE MADE===================================

    -   add SQLAlchemyError exception handling on post method to notify the reason why an object was not created
    -   ask if a router that returns a list returns an empty list or not found
    -   make it so it reads items and categories from csv
    -   export database to excel

==================================================================================================
!!!!!At least one complex endpoint (e.g., advanced search, reports, statistics)[need to ask sean]!!!!

yehu - √item, √order, √transaction
lara - user branch, category, client

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
