import mysql.connector
import uuid
from decouple import config

class MySQLConnector:

    DB_PASSWORD=config('DB_PASSWORD')
    DB_HOST=config('DB_HOST')
    DB_DATABASE=config('DB_DATABASE')
    DB_USER=config('DB_USER')
    cnx = mysql.connector.connect(user = DB_USER,
                                password = DB_PASSWORD,
                                host = DB_HOST,
                                database = DB_DATABASE)
    cursor = cnx.cursor()

    def __init__(self):
        self.DB_DATABASE = config('DB_DATABASE')

    async def procurar_servidor(self, id_server):

        self.cnx._open_connection()
        consulta = f'SELECT * FROM {self.DB_DATABASE}.servidor WHERE id = %s'
        self.cursor.execute(consulta, (id_server,))
        resultado = self.cursor.fetchone()
        self.cnx.close()
        return resultado

    async def procurar_canal_boas_vindas(self, id_server):

        self.cnx._open_connection()
        consulta = f'SELECT * FROM {self.DB_DATABASE}.canal_de_boas_vindas WHERE fk_id_servidor = %s'
        self.cursor.execute(consulta, (id_server,))
        resultado = self.cursor.fetchone()
        self.cnx.close()
        return resultado

    async def alterar_quarentena(self, id_server, status):

        self.cnx._open_connection()
        update = 'UPDATE servidor SET status_servidor = %s WHERE id = %s'
        self.cursor.execute(update, (status, id_server,))
        self.cnx.commit()
        self.cnx.close()

    async def inserir_servidor(self, id_server, name_server):

        self.cnx._open_connection()
        inserir_server = 'INSERT INTO servidor(id, nome_servidor, autorizacao_dm, status_servidor) VALUES(%s, %s, %s, %s)'
        self.cursor.execute(inserir_server,(id_server, name_server, 'Não','liberado'))
        self.cnx.commit()
        self.cnx.close()

    async def alterar_nome_servidor(self, id_server, name_server):

        self.cnx._open_connection()
        update_server = 'UPDATE servidor SET nome_servidor = %s WHERE id = %s'
        self.cursor.execute(update_server, (name_server, id_server,))
        self.cnx.commit()
        self.cnx.close()

    async def escolher_canal_de_boas_vindas(self, id_server, channel):

        resultado = await self.procurar_canal_boas_vindas(id_server)
        self.cnx._open_connection()
        if resultado:
            alterar = 'UPDATE canal_de_boas_vindas SET id = %s WHERE fk_id_servidor = %s'
            self.cursor.execute(alterar, (channel.id, id_server, ))
            self.cnx.commit()
            self.cnx.close()
        else:
            inserir = 'INSERT INTO canal_de_boas_vindas VALUES(%s,%s)'
            self.cursor.execute(inserir, (channel.id, id_server, ))
            self.cnx.commit()
            self.cnx.close()

    async def pesquisar_cargo(self, id_servidor):

        self.cnx._open_connection()
        pesquisar = 'SELECT * FROM cargo_de_boas_vindas WHERE fk_id_servidor = %s'
        self.cursor.execute(pesquisar, (id_servidor,))
        resultado = self.cursor.fetchone()
        self.cnx.close()
        return resultado

    async def inserir_cargo(self, cargo, id_servidor):

        resultado = await self.pesquisar_cargo(id_servidor)
        self.cnx._open_connection()
        if resultado:
            alterar = 'UPDATE cargo_de_boas_vindas SET id_cargo_boas_vindas = %s WHERE fk_id_servidor = %s'
            self.cursor.execute(alterar, (cargo.id, id_servidor, ))
            self.cnx.commit()
            self.cnx.close()
        else:
            inserir = 'INSERT INTO cargo_de_boas_vindas VALUES(%s, %s)'
            self.cursor.execute(inserir, (cargo.id, id_servidor, ))
            self.cnx.commit()
            self.cnx.close()

    async def pesquisar_canal_removidos(self, id_servidor):

        self.cnx._open_connection()
        pesquisar = 'SELECT * FROM canal_de_membros_removidos WHERE fk_id_servidor = %s'
        self.cursor.execute(pesquisar, (id_servidor,))
        resultado = self.cursor.fetchone()
        self.cnx.close()
        return resultado

    async def escolher_canal_removidos(self, canal, id_servidor):

        resultado = await self.pesquisar_canal_removidos(id_servidor)
        self.cnx._open_connection()
        if resultado:
            alterar = 'UPDATE canal_de_membros_removidos SET id = %s WHERE fk_id_servidor = %s'
            self.cursor.execute(alterar, (canal.id, id_servidor,))
            self.cnx.commit()
            self.cnx.close()
        else:
            inserir = 'INSERT INTO canal_de_membros_removidos VALUES(%s, %s)'
            self.cursor.execute(inserir, (canal.id, id_servidor,))
            self.cnx.commit()
            self.cnx.close()

    async def pesquisar_evento(self, id_evento):

        self.cnx._open_connection()
        pesquisar = 'SELECT * FROM eventos WHERE id = %s'
        self.cursor.execute(pesquisar, (id_evento, ))
        resultado = self.cursor.fetchone()
        self.cnx.close()
        return resultado

    async def pesquisar_eventos(self):

        self.cnx._open_connection()
        pesquisar = 'SELECT * FROM eventos WHERE notificado = %s'
        self.cursor.execute(pesquisar, ('NÃO', ))
        resultado = self.cursor.fetchall()
        self.cnx.close()
        return resultado

    async def excluir_evento(self, id_evento):

        self.cnx._open_connection()
        excluir = 'DELETE FROM eventos WHERE id = %s'
        verificacao = self.cursor.execute(excluir, (id_evento, ))
        self.cnx.commit()
        self.cnx.close()
        return verificacao

    async def inserir_evento(self, id_evento, id_servidor, id_canal):

        self.cnx._open_connection()
        inserir = 'INSERT INTO eventos VALUES(%s, %s, %s, %s)'
        self.cursor.execute(inserir, (id_evento, id_servidor, id_canal, 'NÃO', ))
        self.cnx.commit()
        self.cnx.close()

    async def alterar_evento(self, id_evento):

        self.cnx._open_connection()
        alterar = 'UPDATE eventos set notificado = %s WHERE id = %s'
        self.cursor.execute(alterar, ('SIM', id_evento, ))
        self.cnx.commit()
        self.cnx.close()

    async def pesquisar_all_view(self):

        self.cnx._open_connection()
        recuperar = 'SELECT * FROM views'
        self.cursor.execute(recuperar)
        resultado = self.cursor.fetchall()
        return resultado

    async def pesquisar_view(self, id_evento):

        self.cnx._open_connection()
        pesquisar = 'SELECT * FROM views WHERE id = %s'
        self.cursor.execute(pesquisar, (id_evento, ))
        view = self.cursor.fetchall()
        self.cnx.close()
        return view

    async def inserir_view(self, id_mensagem, id_servidor, id_canal):
        self.cnx._open_connection()
        inserir = 'INSERT INTO views VALUES(%s, %s, %s)'
        self.cursor.execute(inserir, (id_mensagem, id_servidor, id_canal, ))
        self.cnx.commit()
        self.cnx.close()

    async def excluir_view(self, id_evento):

        self.cnx._open_connection()
        excluir = 'DELETE FROM views WHERE id = %s'
        self.cursor.execute(excluir, (id_evento, ))
        self.cnx.commit()
        self.cnx.close()