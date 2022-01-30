BULK INSERT clients
FROM 'D:\users.xlsx'
WITH (
    FORMAT = 'xlsx',
    FIRSTROW = 1,
    fieldterminator = ',',
    rowterminator = '\n'
)
GO