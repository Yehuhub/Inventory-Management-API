# Inventory-Management-API

https://documenter.getpostman.com/view/41474192/2sB34fkfnw#07ff2027-5908-4864-ac03-10dcdeecb25a
==================================TODO===================================

    -   add SQLAlchemyError exception handling on post method to notify the reason why an object was not created
    -   need to change most of the not founds to badrequest/return an empty list


    -   make it so it reads items and categories from csv
    -   export database to excel

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
"client_id": 1
}

delivery date and status will be defaulted, status to pending and delivery_date to today+14 days
