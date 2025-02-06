import mysql.connector

database = mysql.connector.connect(  
    host = 'informatica.iesquevedo.es',  
    port = 3333,
    ssl_disabled = True,
    user = 'root', 
    password = '1asir',  
    database = 'adrian'
)