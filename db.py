import pandas as pd
import mysql.connector 
from mysql.connector import CMySQLConnection
def get_connection():
   conn= mysql.connector.connect(host='Localhost',user="root"
                            ,password="V@patidar999313",
                            database="sales_data")
   return conn

def load_data_from_db():
    conn = get_connection()
    query = "SELECT * FROM sales"
    df = pd.read_sql(query,conn)
    conn.close()
    return df
