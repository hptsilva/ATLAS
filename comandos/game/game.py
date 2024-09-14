import discord
from discord.ext import commands
from comandos.game.game_sql_connection import Game_Sql_Connection

COLOR_ISAC = 0xf24f00

objeto = Game_Sql_Connection()

class RPG(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Crie uma partida
    @commands.hybrid_command(name='game_criar_partida', description='Cria uma partida.')
    @commands.is_owner()
    async def game_criar_partida(self, ctx, membro1: discord.Member = None, membro2: discord.Member = None, membro3: discord.Member = None):

        await ctx.send('Processando...', ephemeral=True)
        guild_id = ctx.author.guild.id
        membros = [var for var in [membro1, membro2, membro3] if var]
        membros.append(ctx.author)
        # Verifica se existe valores repetidos na lista
        cond = len(set(membros)) < len(membros)
        if cond:
            await ctx.send('Existem membros repetidos na lista de participantes.', ephemeral=True)
            return
        else:
            pass
        # Adiciona dados da partida na base de dados e retorna o ID ou os membros que não podem participar da partida
        id_ou_membros =  await objeto.criar_partida(guild_id, ctx.author.id, membros)
        if id_ou_membros in membros:
            # Mostra os membros que não podem participar da partida.
            await ctx.send(f'{id_ou_membros.display_name} não possui um agente cadastrado.', ephemeral=True)
        else:
            # Se todos os membros estão aptos a participar cria um tópico no canal de texto.
            textChannel = ctx.message.channel
            tamanho = len(membros)
            thread = await textChannel.create_thread(name=f'Partida de {membros[tamanho-1].display_name}', invitable=False)
            lista = ''
            for membro in membros:
                await thread.send(f'{membro.mention}')
                lista += f'{membro.display_name}\n'
            await objeto.inserir_thread(thread.id, str(id_ou_membros))
            embed = discord.Embed(title=f':game_die: Partida criada :game_die:',
                                  description='Regras: \n 1º - Use os comandos /game_fazer_acao para fazer sua jogada.\n2º - O líder começará primeiro.\n3º - O ISAC avisará de quem será a próxima jogada.\n 4º - A partida acaba quando todos morrerem, cancelada pelo líder ou excede o limite de 24hrs.',
                                  color=COLOR_ISAC)
            embed.add_field(name='ID da partida:',
                            value=f'{str(id_ou_membros)}',
                            inline=False)
            embed.add_field(name='Participantes:',
                            value=f'{lista}',
                            inline=False)
            embed.set_thumbnail(url='https://lh3.googleusercontent.com/drive-viewer/AK7aPaAuhbjNROXGYfTZEAfBtz6mO8tkrRMMUjWqP1YGeFnWPCulxcB_UJI_zRtnB4IdDqBv5DTZbgMZVhC-oidmBDt-Tas42g=s1600')
            embed.set_footer(text='AVISO: Período de 24hrs para finalizar.')
            await thread.send(embed=embed)

    @commands.hybrid_command(name='game_iniciar_partida', description='Inicia a partida.')
    @commands.is_owner()
    async def game_iniciar_partida(self, ctx):

        id_lider = ctx.author.id
        thread_id = ctx.message.channel.id
        iniciar = await objeto.iniciar_partida(id_lider, thread_id)
        if iniciar:
            await ctx.send('**Partida iniciada**\nO líder começará sua ação.')
            caminho_do_arquivo = 'comandos/game/introducao.txt'
            # Lê o arquivo de texto
            with open(caminho_do_arquivo, 'r', encoding='utf-8') as arquivo:
                conteudo = arquivo.read()
            embed = discord.Embed(title='Introdução',
                                  description=f'{conteudo}',
                                  color=COLOR_ISAC)
            embed.set_thumbnail(url='https://lh3.googleusercontent.com/drive-viewer/AK7aPaCZG56rCocer_d-OuXpgqzlObJMmk_HQUNo42uJw9cYYobbEpz4m6h_SMvF-CM9-JjPDPpPn9wDcEeu06n-lx3nCi2mBA=s1600')
            await ctx.send(embed=embed)
        else:
            await ctx.send('Você não é o líder da partida, partida já foi iniciada ou não existe.', ephemeral=True)

    @commands.hybrid_command(name='game_criar_agente', description="Cria seu agente.")
    @commands.is_owner()
    async def game_criar_agente(self, ctx, nome: str, biografia: str=None):

        await ctx.send('Processando...', ephemeral=True)
        resultado = await objeto.pesquisar_agente(ctx.author.id)
        if resultado:
            await ctx.send('Você já possui um agente cadastrado.', ephemeral=True)
        else:
            await objeto.criar_agente(ctx.author.id, nome, biografia)
            await ctx.send('Agente criado.', ephemeral=True)

    # Exclui o agente
    @commands.hybrid_command(name='game_excluir_agente', description='Apague seu agente.')
    @commands.is_owner()
    async def game_excluir_agente(self, ctx, confirmacao: str):

        if confirmacao == 'Sim':
            await ctx.send('Processando...', ephemeral=True)
            resultado = await objeto.excluir_agente(ctx.author.id)
            # Verifica se uma linha no banco de dados foi afetada. Se foi afetada é porque o agente foi excluído com sucesso.
            linhas_afetadas = resultado.rowcount
            if linhas_afetadas > 0:
                await ctx.send('Agente excluído.', ephemeral=True)
            else:
                await ctx.send('Não é possível excluir um agente que não existe.', ephemeral=True)
        else:
            await ctx.send('Confirme com \'Sim\' para excluir o agente.', ephemeral=True)

    # Alterar informações do agente
    @commands.hybrid_command(name='game_alterar_agente', description='Altera dados sobre seu agente.')
    @commands.is_owner()
    async def game_alterar_Agente(self, ctx, nome: str = None, biografia: str = None, avatar: int = None):

        if nome is None and biografia is None and avatar is None:
            await ctx.send('Não há nenhum dado a ser alterado.', ephemeral=True)
        else:
            await ctx.send('Processando...', ephemeral=True)
            resultado = await objeto.pesquisar_agente(ctx.author.id)
            if resultado:
                try:
                    await objeto.alterar_agente(resultado, nome, avatar, biografia)
                    await ctx.send('Alteração realizada com sucesso.', ephemeral=True)
                except:
                    await ctx.send('Ocorreu algum erro. Se o problema persistir informe o dono da aplicação.')
            else:
                await ctx.send('Não existe nenhum agente registrado em seu nome.', ephemeral=True)

    # Mostra informações do agente
    @commands.hybrid_command(name='game_ficha', description='Ver informações do agente.')
    @commands.is_owner()
    async def game_ver_agente(self, ctx, membro: discord.Member = None):

        await ctx.send('Processando...', ephemeral=True)
        if membro is None:
            membro = ctx.author
        resultado = await objeto.pesquisar_agente(membro.id)
        if resultado:
            embed = discord.Embed(title='Ficha do agente',
                                  color=COLOR_ISAC)
            embed.add_field(name='Nome:',
                            value=resultado[1],
                            inline=True)
            embed.add_field(name='Nível:',
                            value=resultado[2],
                            inline=True)
            embed.add_field(name='Ranking:',
                            value=f'#{1}',
                            inline=True)
            embed.add_field(name='Biografia:',
                            value=resultado[4],
                            inline=False)
            imagem_agentes = {1 : 'https://lh3.googleusercontent.com/drive-viewer/AK7aPaDYUmiTNc3F8PnaB5S-QKQ_H_KyZbuAJeaE95wkSgWqA_ZMFaArx2KAs4o2BVW5fjVp94eapOQKd7lNxUnb1__YcSFSeA=s1600',
                              2 : 'https://lh3.googleusercontent.com/drive-viewer/AK7aPaA5BJiDOOkekpltvA5Qp19xxfHIaFf_H3Ulpmb9mhBzZj5chwQ63pKIz3nd-DaDGyMCKCVVWk4wxu3xTPgf6fue4S3b=s1600',
                              3 : 'https://lh3.googleusercontent.com/drive-viewer/AK7aPaCHGPVnPhlSfAsasjSGRSD12W6pNT80jV7_SB1eqD0Jp8D4weQowILfmdMcV3DuIWhdFlnkpF2UZd_kQ2reDYmR2PMi4Q=s1600',
                              4 : 'https://lh3.googleusercontent.com/drive-viewer/AK7aPaAVpby1lsIzILO_RoXO4L_af1Ei5DkzeGhGyTJZvoW0B2efhmkb2_Pq04THqIryhvpELsXGI5XAGEgsVZEeDsW5T0i5Pg=s1600',
                              5 : 'https://lh3.googleusercontent.com/drive-viewer/AK7aPaDJQVnUZL5dfS79VoaQ1wERYnjdkfwYl26g74wQYgOk-HisKIrEQi2BfPUBKjlNWR0ORWLnW4KKgri9hpL0gG8shHQP8w=s1600',
                              6 : 'https://lh3.googleusercontent.com/drive-viewer/AK7aPaCIg9fbC7tYzT4tr9YTuzNPVijnMm3bu0Xnq2E_0-fjfPlmCOK0TFS0QQo_QSZX11HSIxrklzrHWiWqie7zvoNGeGR3=s1600',
                              7 : 'https://lh3.googleusercontent.com/drive-viewer/AK7aPaD-tftCoHQ0DUMJce6tULmHGi0AAUymx-AS6uDqTgcR_BoK9AzbPNswR0-F99dejtvrDUZlalRa8W6susBtl7cxEuEm=s1600',
                              8 : 'https://lh3.googleusercontent.com/drive-viewer/AK7aPaDhgsITCpq-cg06AKMrQ2_Enrkp7AFYQUhTtCXxI3HkAaDXrw9aD99j4pSl15uVERyhaRcv5xYHEnEiHaCeuXtlg5wgPA=s1600',
                              9 : 'https://lh3.googleusercontent.com/drive-viewer/AK7aPaCZoaqBwcgWTjD3kCh-xgn1KksvWhpq0-ZajAKOdpB6hX30JROElqjSGQLyfoJqi6FX4TXGu8JvJY9HUYUGIrv8z4ZJ=s1600'
                              }
            url_imagem = imagem_agentes[resultado[3]]
            embed.set_thumbnail(url=url_imagem)
            embed.set_footer(text=f'Agente de {membro.display_name}')
            await ctx.send(embed=embed)
        else:
            await ctx.send('Não existe um agente registrado para esse membro.', ephemeral=True)

async def setup(bot):
    await bot.add_cog(RPG(bot))
