import mysql.connector
from decouple import config

DB_DATABASE = config('DB_DATABASE')
DB_HOST = config('DB_HOST')
DB_ATLAS_ADMIN=config('DB_ATLAS_ADMIN')
DB_ATLAS_ADMIN_PASSWORD=config('DB_ATLAS_ADMIN_PASSWORD')
DB_ATLAS_USER=config('DB_ATLAS_USER')
DB_ATLAS_USER_PASSWORD=config('DB_ATLAS_USER_PASSWORD')

class MySQLConnector:

    # Conexão com o banco de dados
    def conectar_user():

        cnx_user = mysql.connector.connect(user = DB_ATLAS_USER,
                                            password = DB_ATLAS_USER_PASSWORD,
                                            host = DB_HOST,
                                            database = DB_DATABASE)
        cursor_user = cnx_user.cursor()
        cnx_user._open_connection()
        return cnx_user, cursor_user

    # Conexão com o banco de dados
    def conectar_admin():

        cnx_admin = mysql.connector.connect(user = DB_ATLAS_ADMIN,
                                            password = DB_ATLAS_ADMIN_PASSWORD,
                                            host = DB_HOST,
                                            database = DB_DATABASE)
        cursor_admin = cnx_admin.cursor()
        cnx_admin._open_connection()
        return cnx_admin, cursor_admin

    # Desconectar do banco de dados
    def desconectar_user(cnx_user):

        cnx_user.close()

    # Desconectar do banco de dados
    def desconectar_admin(cnx_admin):

        cnx_admin.close()
