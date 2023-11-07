import mysql.connector
from decouple import config

class MySQLConnector:

    DB_PASSWORD=config('DB_PASSWORD')
    HOST=config('HOST')
    DATA_BASE=config('DATA_BASE')
    cnx = mysql.connector.connect(user = 'root',
                                password = DB_PASSWORD,
                                host = HOST,
                                database = DATA_BASE,
                                auth_plugin = 'mysql_native_password')
    cursor = cnx.cursor()

    def procurar_servidor(self, id_server):

        self.cnx._open_connection()
        consulta = 'SELECT * FROM isac.servidor WHERE id_servidor = %s'
        self.cursor.execute(consulta, (id_server,))
        resultado = self.cursor.fetchone()
        self.cnx.close()
        return resultado

    def procurar_canal_boas_vindas(self, id_server):

        self.cnx._open_connection()
        consulta = 'SELECT * FROM isac.canal_de_boas_vindas WHERE fk_id_servidor = %s'
        self.cursor.execute(consulta, (id_server,))
        resultado = self.cursor.fetchone()
        self.cnx.close()
        return resultado

    def procurar_canal_twitch(self, id_server):

        consulta = 'SELECT * FROM isac.canal_twitch WHERE fk_id_servidor = %s'
        self.cursor.execute(consulta, (id_server,))
        resultado = self.cursor.fetchone()
        return resultado

    def alterar_quarentena(self, id_server, status):

        self.cnx._open_connection()
        update = 'UPDATE servidor SET status_servidor = %s WHERE id_servidor = %s'
        self.cursor.execute(update, (status, id_server,))
        self.cnx.commit()
        self.cnx.close()

    def inserir_servidor(self, id_server, name_server):

        self.cnx._open_connection()
        inserir_server = 'INSERT INTO servidor(id_servidor, nome, autorizacao_dm, status_servidor) VALUES(%s, %s, %s, %s)'
        self.cursor.execute(inserir_server,(id_server, name_server, 'Não','liberado'))
        self.cnx.commit()
        self.cnx.close()

    def alterar_nome_servidor(self, id_server, name_server):

        self.cnx._open_connection()
        update_server = 'UPDATE servidor SET nome = %s WHERE id_servidor = %s'
        self.cursor.execute(update_server, (name_server, id_server,))
        self.cnx.commit()
        self.cnx.close()

    def escolher_canal_de_boas_vindas(self, id_server, channel):

        self.cnx._open_connection()
        resultado = self.procurar_canal_boas_vindas(self, id_server)
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

    def procurar_servidor_banido(self, id_server):
        
        self.cnx._open_connection()
        procurar = 'SELECT * FROM isac.servidores_banidos WHERE id_servidor = %s'
        self.cursor.execute(procurar, (id_server, ))
        resultado = self.cursor.fetchone()
        self.cnx.close()
        return resultado
    
    def escolher_canal_twitch(self, id_server, channel):

        self.cnx._open_connection()
        resultado = self.procurar_canal_twitch(self, id_server)
        if resultado:
            alterar = 'UPDATE canal_twitch SET id_canal_twitch = %s, nome = %s WHERE fk_id_servidor = %s'
            self.cursor.execute(alterar, (channel.id, channel.name, id_server, ))
            self.cnx.commit()
            self.cnx.close()
        else:
            inseir = 'INSERT INTO canal_twitch VALUES(%s,%s,%s)'
            self.cursor.execute(inseir, (channel.id, channel.name, id_server, ))
            self.cnx.commit()
            self.cnx.close()

    def inserir_streamer(self, id_server, membro):

        self.cnx._open_connection()
        consulta = 'SELECT * FROM isac.streamers WHERE id_streamer = %s'
        self.cursor.execute(consulta, (membro.id,))
        resultado = self.cursor.fetchone()
        if resultado:
            consulta = 'SELECT * FROM isac.servidor_streamers WHERE fk_id_streamer = %s AND fk_id_servidor = %s'
            self.cursor.execute(consulta, (membro.id, id_server, ))
            resultado = self.cursor.fetchone()
            if resultado:
                self.cnx.close()
                return 'Usuário escolhido já está registrado.'
            else:
                inserir = 'INSERT INTO servidor_streamers VALUES(%s, %s)'
                self.cursor.execute(inserir, (membro.id, id_server, ))
                self.cnx.commit()
                self.cnx.close
                return 'Usuário escolhido foi registrado.'
        else:
            inserir = 'INSERT INTO streamers VALUES(%s, %s)'
            self.cursor.execute(inserir, (membro.id, membro.name, ))
            self.cnx.commit()
            inserir = 'INSERT INTO servidor_streamers VALUES(%s, %s)'
            self.cursor.execute(inserir, (membro.id, id_server, ))
            self.cnx.commit()
            self.cnx.close
            return 'Usuário escolhido foi registrado.'
        
    def procurar_streamer(self, id_server, id_member):

        self.cnx._open_connection()
        consulta = 'SELECT * FROM isac.servidor_streamers WHERE fk_id_streamer = %s AND fk_id_servidor = %s'
        self.cursor.execute(consulta, (id_member, id_server, ))
        resultado = self.cursor.fetchone()
        self.cnx.close()
        return resultado
    
    def excluir_streamer(self, id_server, id_member):

        self.cnx._open_connection()
        excluir = 'DELETE * FROM isac.servidor_streamers WHERE fk_id_streamer = %s AND fk_id_servidor = %s'
        self.cursor.execute(excluir, (id_member, id_server, ))
        self.cnx.commit()
        self.cnx.close()
        return 'Streamer excluído da lista'
    
    def listar_streamers(self, id_server):

        self.cnx._open_connection()
        consulta = 'SELECT * FROM isac.servidor_streamers WHERE fk_id_servidor = %s'
        self.cursor.execute(consulta, (id_server, ))
        resultado = self.cursor.fetchall()
        self.cnx.close()
        return resultado

    def inserir_enquete(self, id_server, id_enquete):
        
        self.cnx._open_connection()
        inserir = 'INSERT INTO enquetes VALUES(%s, %s)'
        self.cursor.execute(inserir, (id_enquete, id_server, ))
        self.cnx.commit()
        self.cnx.close()

    def pesquisar_enquete(self, id_server, id_enquete):

        self.cnx._open_connection()
        consulta = 'SELECT * FROM isac.enquetes WHERE id_enquete = %s AND fk_id_servidor = %s'
        self.cursor.execute(consulta, (id_enquete, id_server, ))
        resultado = self.cursor.fetchone()
        self.cnx.close()
        return resultado