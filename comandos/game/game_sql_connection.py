import mysql.connector
import random
import uuid
import datetime
import json
from decouple import config

class Game_Sql_Connection():

    DB_PASSWORD=config('DB_PASSWORD')
    HOST=config('HOST')
    GAME_DATA_BASE=config('GAME_DATA_BASE')
    cnx = mysql.connector.connect(user = 'humbertoptsilva',
                                  password = DB_PASSWORD,
                                  host = HOST,
                                  database = GAME_DATA_BASE)
    cursor = cnx.cursor()

    async def pesquisar_agente(self, id_membro):

        self.cnx._open_connection()
        consulta = 'SELECT * FROM jogo.agente WHERE id_agente = %s'
        self.cursor.execute(consulta, (id_membro, ))
        resultado = self.cursor.fetchone()
        self.cnx.close()
        return resultado

    # Criar partida
    async def criar_partida(self, guild_id, lider, membros):

        for agente in membros:
            # Se o membro que irá participar da partida não tiver um membro, a partida não será criada e a aplicação avisará quem não possui um agente cadastrado.
            resultado = await self.pesquisar_agente(agente.id)
            if resultado:
                pass
            else:
                return agente
        self.cnx._open_connection()
        inserir = 'INSERT INTO registro values(%s, %s, %s, %s, %s, %s)'
        id_registro = uuid.uuid4()
        now_time = datetime.datetime.utcnow()
        self.cursor.execute(inserir, (str(id_registro), guild_id, lider, None, now_time, None ))
        self.cnx.commit()
        for agente in membros:
            inserir = 'INSERT INTO partida values(%s, %s)'
            self.cursor.execute(inserir, (str(id_registro), agente.id, ))
            self.cnx.commit()

        inserir = 'INSERT INTO controle values(%s, %s, %s, %s, %s)'
        dicionario = {i + 1: valor.id for i, valor in enumerate(membros)}
        dicionario_json = json.dumps(dicionario)
        self.cursor.execute(inserir, (str(id_registro), dicionario_json, 1, len(membros), 1))
        self.cnx.commit()
        self.cnx.close()
        return id_registro

    # Inicia partida
    async def iniciar_partida(self, lider , thread):

        self.cnx._open_connection()
        consulta = 'SELECT * FROM jogo.registro WHERE (id_lider = %s AND id_topico = %s AND status = %s)'
        self.cursor.execute(consulta, (lider, thread, 'AGUARDANDO', ))
        resultado = self.cursor.fetchone()
        if resultado:
            alterar = 'UPDATE registro SET status = %s WHERE id_topico = %s'
            self.cursor.execute(alterar, ('INICIADO', thread, ))
            self.cnx.commit()
            self.cnx.close()
            return resultado
        else:
            self.cnx.close()
            return None

    # Cria um tópico no canal de texto que usou o comando
    async def inserir_thread(self, id_topico, id_registro):

        self.cnx._open_connection()
        inserir = 'UPDATE registro SET id_topico = %s, status = %s WHERE id_registro = %s '
        self.cursor.execute( inserir, (id_topico, 'AGUARDANDO', id_registro,))
        self.cnx.commit()
        self.cnx.close()

    # Cria um agente
    async def criar_agente(self, id_membro, nome, biografia):

        self.cnx._open_connection()
        inserir = 'INSERT INTO agente values (%s, %s, %s, %s, %s)'
        foto = random.randint(1,9)
        self.cursor.execute(inserir, (id_membro, nome, 1, foto, biografia, ))
        self.cnx.commit()
        self.cnx.close

    # Exclua um agente
    async def excluir_agente(self, id_membro):

        self.cnx._open_connection()
        excluir = 'DELETE FROM agente WHERE id_agente = %s'
        self.cursor.execute(excluir, (id_membro, ))
        self.cnx.commit()
        self.cnx.close
        return self.cursor

    # Alterar informações sobre o agente
    async def alterar_agente(self, resultado, nome, avatar, biografia):

        if nome is None:
            nome = resultado[1]
        if avatar is None:
            avatar = resultado[3]
        if biografia is None:
            biografia = resultado[4]
        self.cnx._open_connection()
        alterar = 'UPDATE agente SET nome = %s, avatar = %s, biografia = %s WHERE id_agente = %s'
        self.cursor.execute(alterar, (nome, avatar, biografia, resultado[0], ))
        self.cnx.commit()
        self.cnx.close()
