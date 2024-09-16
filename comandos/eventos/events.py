import discord
import asyncio
import mysql_connection
import pytz
from decouple import config
from discord.ext import commands
from mysql_connection import MySQLConnector

COLOR = int(config('COLOR'))

class Eventos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.BOT_NAME = config('BOT_NAME')

    # Evento ativado quando o bot é iniciado.
    @commands.Cog.listener()
    async def on_ready(self):

        MySQLConnector = mysql_connection.MySQLConnector()
        await self.bot.tree.sync(guild = None)
        print(f'\nBot ({self.bot.user}) iniciado - (ID: {self.bot.user.id})')
        ordem = 1
        # Alterar a atividade do bot
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name='Starfield'))
        # Lista os nomes e IDs do servidores que o Bot é membro e atualiza o banco de dados caso o nome do servidor foi alterado
        print(f'Número de servidores: {len(self.bot.guilds)}\n')
        print(f'--------------------------------------------------------')
        for guild in self.bot.guilds:
            print(f'#{ordem} Servidor ({guild.name}) - ID ({guild.id})')
            # Criando a sessão
            resultado = await MySQLConnector.procurar_servidor(guild.id)
            if resultado is None:
                await MySQLConnector.inserir_servidor(guild.id, guild.name)
            elif resultado[2] is not guild.name:
                await MySQLConnector.alterar_nome_servidor(guild.id, guild.name)
            ordem += 1
        print('--------------------------------------------------------')
        print(f'------------------- {self.BOT_NAME} INICIADO ----------------------')
        print('--------------------------------------------------------')

    # Envia uma mensagem em um canal de texto quando o bot entrar no servidor
    @commands.Cog.listener()
    async def on_guild_join(self, guild):

        MySQLConnector = mysql_connection.MySQLConnector()
        # Verifica se o servidor está na base de dados
        resultado = await MySQLConnector.procurar_servidor(guild.id)
        if resultado:
            # reinsere os novo dados do servidor.
            await MySQLConnector.alterar_nome_servidor(guild.id, guild.name)
        else:
            # insere dados do servidor na base da dados caso não esteja
            await MySQLConnector.inserir_servidor(guild.id, guild.name)

    # Evento ativado quando ocorre alteração no servidor (como nome do servidor, por exemplo)
    @commands.Cog.listener()
    async def on_guild_update(self, before, after):

        MySQLConnector = mysql_connection.MySQLConnector()
        name_server = after.name
        if (name_server is not before.name):
            # altera o dado name_server caso o nome do servidor mude
            await MySQLConnector.alterar_nome_servidor(before.id, name_server)

    # Evento ativado quando um usuário entrar no servidor
    @commands.Cog.listener()
    async def on_member_join(self, member):

        MySQLConnector = mysql_connection.MySQLConnector()
        id_server = member.guild.id
        resultado = await MySQLConnector.procurar_servidor(id_server)
        if resultado[3] == 'quarentena':
            await member.kick(reason = "Não é permitido entrar no servidor quando o mesmo está em quarentena")
            return
        resultado = await MySQLConnector.procurar_canal_boas_vindas(id_server)
        if resultado:
            avatar_url = member.avatar.url if member.avatar else member.default_avatar.url
            nome = member.display_name
            embed = discord.Embed(
                title = f':shield: Bem-vindo ao servidor {member.guild.name} :shield:',
                description = f'{member.display_name}, estamos felizes em tê-lo(a) conosco. Aproveite!',
                color = COLOR
           )
            embed.add_field(name="Nome de usuário:", value=f"`{member.name}`", inline=True)
            embed.add_field(name="ID:", value=f"`{member.id}`", inline=True)
            bot_timezone = pytz.timezone('UTC')
            joined_at_timezone = member.joined_at.astimezone(bot_timezone)
            embed.add_field(name="Entrou em:", value=f"<t:{int(joined_at_timezone.timestamp())}:f>", inline=False)
            embed.set_thumbnail(url=avatar_url)
            canal = member.guild.get_channel(int(resultado[0]))
            await asyncio.sleep(0.35)
            await canal.send(content=f'{member.mention}',embed=embed)
            embed = discord.Embed(
                title = f':shield: Você entrou no servidor {member.guild.name}  :shield:',
                description = f'Regras:\n\n- Seja respeitoso com todos os membros do servidor.\n- Utilize os canais de texto da maneira correta. Veja a descrição de cada canal.\n- Sem mensagens de spam e phishing.\n\n **Não seguir qualquer uma das regras anteriores é passível de banimento.**\n\n**Obs:** Para criar convites no servidor, use o comando /criar_convite.',
                color = COLOR
            )
            if (member.guild.icon is not None):
                embed.set_thumbnail(url=member.guild.icon.url)
            try:
                await member.send(embed=embed)
            except:
                pass
            try:
                resultado = await MySQLConnector.pesquisar_cargo(id_server)
                if resultado:
                    role = member.guild.get_role(int(resultado[0]))
                    await member.add_roles(role)
            except:
                return

    # Evento ativado quando um membro sai do servidor. O membro ou o servidor não estão armazenados em cache.
    @commands.Cog.listener()
    async def on_raw_member_remove(self, payload):

        MySQLConnector = mysql_connection.MySQLConnector()
        id_server = payload.guild_id
        member = payload.user
        resultado = await MySQLConnector.pesquisar_canal_removidos(id_server)
        if resultado:
            avatar_url = member.avatar.url if member.avatar else member.default_avatar.url
            embed = discord.Embed(
                title = ':rotating_light: Um membro saiu do servidor :rotating_light:',
                description = f'{member.display_name} não está mais entre nós!',
                color = COLOR
            )
            embed.set_thumbnail(url=avatar_url)
            canal = member.guild.get_channel(int(resultado[0]))
            await canal.send(embed=embed)

    @commands.Cog.listener()
    async def on_scheduled_event_delete(self, event):

        try:
            await MySQLConnector.cancelar_evento(MySQLConnector, event.id)
        except:
            print(f'Evento ID {event.id} não encontrado')

async def setup(bot):
    await bot.add_cog(Eventos(bot))
