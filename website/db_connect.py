import pyodbc


def connect_sql():
    connStr = (
        r'DRIVER={SQL Server};'
        r'SERVER=DESKTOP-N60GPF0;'
        r'DATABASE=inventory;'
        r'UID=malaa;'
        r'PWD=P@ssw0rd;'
    )
    return pyodbc.connect(connStr)
