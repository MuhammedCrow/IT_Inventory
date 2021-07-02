import pyodbc


def connect_sql():
    connStr = (
        r'DRIVER={SQL Server};'
        r'SERVER=DESKTOP-N60GPF0;'
        r'DATABASE=inventory;'
        r'UID=mualaa;'
        r'PWD=P@ssw0rd;'
    )
    conx = pyodbc.connect(connStr)
    return conx
