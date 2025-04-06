#%%
import pandas as pd
import psycopg2
from sqlalchemy import create_engine

# Database connection parameters
db_name = "user_orders"
db_user = "postgres"
db_password = "mysecretpassword"
db_host = "localhost"
db_port = "5433"

# Create a database engine
DATABASE_URI = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
engine = create_engine(DATABASE_URI)

# Query to select data from the orders table
query = "SELECT * FROM users"

# Read the data into a DataFrame
df = pd.read_sql(query, engine)

# Export the DataFrame to a CSV file
df.to_csv('users.csv', index=False)

print("Data exported to users.csv successfully.")

# %%
