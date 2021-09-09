import pyodbc


def connect_sql():
    connStr = (
        r'DRIVER={SQL Server};'
        r'SERVER=KCML-LT239;'
        r'DATABASE=inventory;'
        r'UID=malaa;'
        r'PWD=P@ssw0rd;'
    )
    conx = pyodbc.connect(connStr)
    return conx
