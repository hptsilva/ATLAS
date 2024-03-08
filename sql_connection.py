import mysql.connector
import random
import uuid
from decouple import config

class MySQLConnector:

    DB_PASSWORD=config('DB_PASSWORD')
    HOST=config('HOST')
    DATA_BASE=config('DATA_BASE')
    cnx = mysql.connector.connect(user = 'humbertoptsilva',
                                password = DB_PASSWORD,
                                host = HOST,
                                database = DATA_BASE)
    cursor = cnx.cursor()

    async def procurar_servidor(self, id_server):

        self.cnx._open_connection()
        consulta = 'SELECT * FROM atlas.servidor WHERE id_servidor = %s'
        self.cursor.execute(consulta, (id_server,))
        resultado = self.cursor.fetchone()
        self.cnx.close()
        return resultado

    async def procurar_canal_boas_vindas(self, id_server):

        self.cnx._open_connection()
        consulta = 'SELECT * FROM atlas.canal_de_boas_vindas WHERE fk_id_servidor = %s'
        self.cursor.execute(consulta, (id_server,))
        resultado = self.cursor.fetchone()
        self.cnx.close()
        return resultado

    async def alterar_quarentena(self, id_server, status):

        self.cnx._open_connection()
        update = 'UPDATE servidor SET status_servidor = %s WHERE id_servidor = %s'
        self.cursor.execute(update, (status, id_server,))
        self.cnx.commit()
        self.cnx.close()

    async def inserir_servidor(self, id_server, name_server):

        self.cnx._open_connection()
        inserir_server = 'INSERT INTO servidor(id_servidor, nome, autorizacao_dm, status_servidor) VALUES(%s, %s, %s, %s)'
        self.cursor.execute(inserir_server,(id_server, name_server, 'Não','liberado'))
        self.cnx.commit()
        self.cnx.close()

    async def alterar_nome_servidor(self, id_server, name_server):

        self.cnx._open_connection()
        update_server = 'UPDATE servidor SET nome = %s WHERE id_servidor = %s'
        self.cursor.execute(update_server, (name_server, id_server,))
        self.cnx.commit()
        self.cnx.close()

    async def escolher_canal_de_boas_vindas(self, id_server, channel):

        resultado = await self.procurar_canal_boas_vindas(id_server)
        self.cnx._open_connection()
        if resultado:
            alterar = 'UPDATE canal_de_boas_vindas SET id_canal_boas_vindas = %s, nome = %s WHERE fk_id_servidor = %s'
            self.cursor.execute(alterar, (channel.id, channel.name, id_server, ))
            self.cnx.commit()
            self.cnx.close()
        else:
            inseir = 'INSERT INTO canal_de_boas_vindas VALUES(%s,%s,%s)'
            self.cursor.execute(inseir, (channel.id, channel.name, id_server, ))
            self.cnx.commit()
            self.cnx.close()

