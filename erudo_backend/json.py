"""
JSON for asking a question and sending the explanation json

{
    "question": "what did user_id 1 order?",
    "explanation_json": {

        "erudohq-dev.user_orders.orders": {
            "description": "This table stores information about each order placed by users.",
            "columns": {
                "order_id": "Unique identifier for each order.",
                "user_id": "Identifier for the user who placed the order. References the users table.",
                "product": "Name or identifier of the product ordered.",
                "amount": "Total monetary value of the order.",
                "order_date": "Date when the order was placed."
            }
        },
        "erudohq-dev.user_orders.users": {
            "description": "This table contains user profile information.",
            "columns": {
                "user_id": "Unique identifier for each user.",
                "name": "Full name of the user.",
                "email": "Email address of the user."
            }
        }
    }
}
"""