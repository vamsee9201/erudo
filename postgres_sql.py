# Note: the module name is psycopg, not psycopg3
#%%
import psycopg
#%%
var = ""
# Connect to an existing database
with psycopg.connect("dbname=postgres user=postgres password=Maxverstappen@33") as conn:

    # Open a cursor to perform database operations
    with conn.cursor() as cur:

        # Execute a command: this creates a new table
        cur.execute("""
            CREATE TABLE test (
                id serial PRIMARY KEY,
                num integer,
                data text)
            """)

        # Pass data to fill a query placeholders and let Psycopg perform
        # the correct conversion (no SQL injections!)
        cur.execute(
            "INSERT INTO test (num, data) VALUES (%s, %s)",
            (100, "abc'def"))

        # Query the database and obtain data as Python objects.
        cur.execute("SELECT * FROM test")
        cur.fetchone()
        # will return (1, 100, "abc'def")

        # You can use `cur.fetchmany()`, `cur.fetchall()` to return a list
        # of several records, or even iterate on the cursor
        for record in cur:
            var = record
            print(record)

        # Make the changes to the database persistent
        conn.commit()
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
for record in cur:
    print(record)
#%%
