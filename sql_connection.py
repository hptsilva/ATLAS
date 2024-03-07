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

    async def procurar_servidor_banido(self, id_server):

        self.cnx._open_connection()
        procurar = 'SELECT * FROM atlas.servidores_banidos WHERE id_servidor = %s'
        self.cursor.execute(procurar, (id_server, ))
        resultado = self.cursor.fetchone()
        self.cnx.close()
        return resultado

    async def escolher_canal_twitch(self, id_server, channel):

        self.cnx._open_connection()
        resultado = await self.procurar_canal_twitch(id_server)
        if resultado:
            alterar = 'UPDATE canal_twitch SET id_canal_twitch = %s, nome = %s WHERE fk_id_servidor = %s'
            self.cursor.execute(alterar, (channel.id, channel.name, id_server, ))
            self.cnx.commit()
            self.cnx.close()
        else:
            inserir = 'INSERT INTO canal_twitch VALUES(%s,%s,%s)'
            self.cursor.execute(inserir, (channel.id, channel.name, id_server, ))
            self.cnx.commit()
            self.cnx.close()

    async def inserir_enquete(self, id_server, id_enquete, start_time, end_time, status):

        self.cnx._open_connection()
        inserir = 'INSERT INTO enquetes VALUES(%s, %s, %s, %s, %s)'
        self.cursor.execute(inserir, (id_enquete, id_server, start_time, end_time, status, ))
        self.cnx.commit()
        self.cnx.close()

    async def pesquisar_enquete(self, id_server, id_enquete):

        self.cnx._open_connection()
        consulta = 'SELECT * FROM atlas.enquetes WHERE id_enquete = %s AND fk_id_servidor = %s'
        self.cursor.execute(consulta, (id_enquete, id_server, ))
        resultado = self.cursor.fetchone()
        self.cnx.close()
        return resultado

    async def inserir_evento(self, id_evento, id_servidor, id_criador):

        self.cnx._open_connection()
        id_registro = uuid.uuid4()
        inserir = 'INSERT INTO eventos VALUES(%s, %s, %s, %s, %s)'
        self.cursor.execute(inserir, (str(id_registro), id_evento, id_servidor, id_criador, None, ))
        self.cnx.commit()
        self.cnx.close()
        return id_registro

    async def pesquisar_evento(self, id_evento, id_criador, id_servidor):

        self.cnx._open_connection()
        pesquisar = 'SELECT * FROM eventos WHERE uuid_evento = %s AND id_criador = %s AND fk_id_servidor = %s'
        self.cursor.execute(pesquisar, (id_evento, id_criador, id_servidor))
        resultado = self.cursor.fetchone()
        self.cnx.close()
        return resultado

    async def cancelar_evento(self, id_evento):

        self.cnx._open_connection()
        deletar = 'DELETE FROM eventos WHERE id_evento = %s'
        self.cursor.execute(deletar, (id_evento, ))
        self.cnx.commit()
        self.cnx.close()

    async def inserir_dm_evento(self, id_dm, uuid):

        self.cnx._open_connection()
        inserir = 'UPDATE eventos SET id_dm_mensagem = %s WHERE uuid_evento = %s'
        self.cursor.execute(inserir, (id_dm, str(uuid), ))
        self.cnx.commit()
        self.cnx.close()


