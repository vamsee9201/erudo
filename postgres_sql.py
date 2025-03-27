
# %%
import psycopg2
db_name = "postgres"
db_user = "postgres"
db_password = "mysecretpassword"
db_host = "localhost"  # or your database host
db_port = "5433" # default port if not specified


conn = psycopg2.connect(
        database=db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port
    )

# %%
cur = conn.cursor()
cur.execute("SELECT * FROM table_name")
# %%
import psycopg2
db_name = "user_orders"
db_user = "postgres"
db_password = "mysecretpassword"
db_host = "localhost"  # or your database host
db_port = "5433"

conn = psycopg2.connect(
        database=db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port
    )
cur = conn.cursor()
#%%
cur.execute("""
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema = 'public'
""")
tables = cur.fetchall()
for table in tables:
    print(table[0])
#%%
for record in cur:
    print(record)
#%%
