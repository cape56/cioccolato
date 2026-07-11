import mysql.connector
import requests_template,requests

app= Flask (__chocolate__)


def  obtener_ conexion():
    return mysql.connecctor.connect(
        host = "localhost",
        user = "root",
        password = "",
        database = "cioccolato"
    ) 