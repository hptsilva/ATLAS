import discord
from decouple import config

COLOR = int(config('COLOR'))
ICON_URL = config('ICON_URL')

class Reacoes_Enquete:

    # Edita a mensagem da enquete quando um membre usa alguma reação
    async def reacoes(self, message, user, reacao):

        embed_antigo = message.embeds[0]
        campo_sim = embed_antigo.fields[1]
        value_sim = campo_sim.value
        value_sim = value_sim.replace(">","").replace(" ","").replace("@","").replace("!","").replace("<","").replace("-","")
        campo_nao = embed_antigo.fields[2]
        value_nao = campo_nao.value
        value_nao = value_nao.replace(">","").replace(" ","").replace("@","").replace("!","").replace("<","").replace("-","")
        campo_talvez = embed_antigo.fields[3]
        value_talvez = campo_talvez.value
        value_talvez = value_talvez.replace(">","").replace(" ","").replace("@","").replace("!","").replace("<","").replace("-","")
        url_image = embed_antigo.image.url
        if embed_antigo.description is None:
            embed= discord.Embed(title=f'{embed_antigo.title}',
                                 color=COLOR)
        else:
            embed = discord.Embed(title=f'{embed_antigo.title}',
                                  description=f'{embed_antigo.description}',
                                  color=COLOR)
        # Se a reação for ✅
        if reacao == 1:
            mencoes_sim = value_sim.split('\n')
            mencoes_nao = value_nao.split('\n')
            mencoes_talvez = value_talvez.split('\n')
            # retira o dono da reação na lista
            cond = 0
            for nome in mencoes_sim:
                if nome == f'{user.id}':
                    mencoes_sim.remove(nome)
                    cond = 1
            for nome in mencoes_nao:
                if nome == f'{user.id}':
                    mencoes_nao.remove(nome)
            for nome in mencoes_talvez:
                if nome == f'{user.id}':
                    mencoes_talvez.remove(nome)
            # Adiciona o dono na reação na lista
            if cond == 0:
                mencoes_sim.append(user.id)
            mencoes_sim = [elemento for elemento in mencoes_sim if elemento != ""]
            mencoes_nao = [elemento for elemento in mencoes_nao if elemento != ""]
            mencoes_talvez = [elemento for elemento in mencoes_talvez if elemento != ""]

            mencoes_sim = ["> " + f"<@!{str(nome)}>" for nome in mencoes_sim]
            mencoes1 = "\n".join([f"{nome}" for nome in mencoes_sim])
            if len(mencoes_nao) > 0:
                mencoes_nao = ["> " + f"<@!{str(nome)}>" for nome in mencoes_nao]
            mencoes2 = "\n".join([f"{nome}" for nome in mencoes_nao])
            if len(mencoes_talvez) > 0:
                mencoes_talvez = ["> " + f"<@!{str(nome)}>" for nome in mencoes_talvez]
            mencoes3 = "\n".join([f"{nome}" for nome in mencoes_talvez])
            url_image = embed_antigo.image.url
            embed.timestamp = embed_antigo.timestamp
            embed.add_field(name='Horário:', value=f':alarm_clock: <t:{int(embed.timestamp.timestamp())}:f>\n:hourglass: <t:{int(embed.timestamp.timestamp())}:R>', inline=False)
            embed.add_field(name='🟩 Sim:', value=f'{mencoes1}', inline=True)
            embed.add_field(name='🟥 Não:', value=f'{mencoes2}', inline=True)
            embed.add_field(name='🟦 Talvez:', value=f'{mencoes3}', inline=True)
        # Se a reação for ⛔
        elif reacao == 2:
            # retira o dono da reação na lista
            mencoes_sim = value_sim.split('\n')
            mencoes_nao = value_nao.split('\n')
            mencoes_talvez = value_talvez.split('\n')
            # retira o dono da reação na lista
            cond = 0
            for nome in mencoes_sim:
                if nome == f'{user.id}':
                    mencoes_sim.remove(nome)
            for nome in mencoes_nao:
                if nome == f'{user.id}':
                    mencoes_nao.remove(nome)
                    cond = 1
            for nome in mencoes_talvez:
                if nome == f'{user.id}':
                    mencoes_talvez.remove(nome)
            # Adiciona o dono na reação na lista
            if cond == 0:
                mencoes_nao.append(user.id)

            mencoes_sim = [elemento for elemento in mencoes_sim if elemento != ""]
            mencoes_nao = [elemento for elemento in mencoes_nao if elemento != ""]
            mencoes_talvez = [elemento for elemento in mencoes_talvez if elemento != ""]

            if len(mencoes_sim) > 0:
                mencoes_sim = ["> " + f"<@!{str(nome)}>" for nome in mencoes_sim]
            mencoes1 = "\n".join([f"{nome}" for nome in mencoes_sim])
            mencoes_nao = ["> " + f"<@!{str(nome)}>" for nome in mencoes_nao]
            mencoes2 = "\n".join([f"{nome}" for nome in mencoes_nao])
            if len(mencoes_talvez) > 0:
                mencoes_talvez = ["> " + f"<@!{str(nome)}>" for nome in mencoes_talvez]
            mencoes3 = "\n".join([f"{nome}" for nome in mencoes_talvez])
            url_image = embed_antigo.image.url
            embed.timestamp = embed_antigo.timestamp
            embed.add_field(name='Horário:', value=f':alarm_clock: <t:{int(embed.timestamp.timestamp())}:f>\n:hourglass: <t:{int(embed.timestamp.timestamp())}:R>', inline=False)
            embed.add_field(name='🟩 Sim:', value=f'{mencoes1}', inline=True)
            embed.add_field(name='🟥 Não:', value=f'{mencoes2}', inline=True)
            embed.add_field(name='🟦 Talvez:', value=f'{mencoes3}', inline=True)
        # Se a reação for ❔
        elif reacao == 3:
            mencoes_sim = value_sim.split('\n')
            mencoes_nao = value_nao.split('\n')
            mencoes_talvez = value_talvez.split('\n')
            # retira o dono da reação na lista
            cond = 0
            for nome in mencoes_sim:
                if nome == f'{user.id}':
                    mencoes_sim.remove(nome)
            for nome in mencoes_nao:
                if nome == f'{user.id}':
                    mencoes_nao.remove(nome)
            for nome in mencoes_talvez:
                if nome == f'{user.id}':
                    mencoes_talvez.remove(nome)
                    cond = 1
            # Adiciona o dono na reação na lista
            if cond == 0:
                mencoes_talvez.append(user.id)

            mencoes_sim = [elemento for elemento in mencoes_sim if elemento != ""]
            mencoes_nao = [elemento for elemento in mencoes_nao if elemento != ""]
            mencoes_talvez = [elemento for elemento in mencoes_talvez if elemento != ""]

            if len(mencoes_sim) > 0:
                mencoes_sim = [">  " + f"<@!{str(nome)}>" for nome in mencoes_sim]
            mencoes1 = "\n".join([f"{nome}" for nome in mencoes_sim])
            if len(mencoes_nao) > 0:
                mencoes_nao = ["> " + f"<@!{str(nome)}>" for nome in mencoes_nao]
            mencoes2 = "\n".join([f"{nome}" for nome in mencoes_nao])
            mencoes_talvez = ["> " + f"<@!{str(nome)}>" for nome in mencoes_talvez]
            mencoes3 = "\n".join([f"{nome}" for nome in mencoes_talvez])
            url_image = embed_antigo.image.url
            embed.timestamp = embed_antigo.timestamp
            embed.add_field(name='Horário:', value=f':alarm_clock: <t:{int(embed.timestamp.timestamp())}:f>\n:hourglass: <t:{int(embed.timestamp.timestamp())}:R>', inline=False)
            embed.add_field(name='🟩 Sim:', value=f'{mencoes1}', inline=True)
            embed.add_field(name='🟥 Não:', value=f'{mencoes2}', inline=True)
            embed.add_field(name='🟦 Talvez:', value=f'{mencoes3}', inline=True)
        elif reacao == 4:
            url_image = embed_antigo.image.url
            embed.timestamp = embed_antigo.timestamp
            embed.add_field(name='Horário:', value=f':alarm_clock: <t:{int(embed.timestamp.timestamp())}:f>\n:hourglass: <t:{int(embed.timestamp.timestamp())}:R>', inline=False)
            value_sim = campo_sim.value
            value_nao = campo_nao.value
            value_talvez = campo_talvez.value
            embed.add_field(name='🟩 Sim:', value=f'{value_sim}', inline=True)
            embed.add_field(name='🟥 Não:', value=f'{value_nao}', inline=True)
            embed.add_field(name='🟦 Talvez:', value=f'{value_talvez}', inline=True)
            if url_image != '' and url_image != None:
                embed.set_image(url=f'{url_image}')
            embed.set_footer(text=f'EVENTO CANCELADO',
                             icon_url=ICON_URL,
            )
            return embed
        else:
            url_image = embed_antigo.image.url
            embed.timestamp = embed_antigo.timestamp
            embed.add_field(name='Horário:', value=f':alarm_clock: <t:{int(embed.timestamp.timestamp())}:f>\n:hourglass: <t:{int(embed.timestamp.timestamp())}:R>', inline=False)
            value_sim = campo_sim.value
            value_nao = campo_nao.value
            value_talvez = campo_talvez.value
            embed.add_field(name='🟩 Sim:', value=f'{value_sim}', inline=True)
            embed.add_field(name='🟥 Não:', value=f'{value_nao}', inline=True)
            embed.add_field(name='🟦 Talvez:', value=f'{value_talvez}', inline=True)
            if url_image != '' and url_image != None:
                embed.set_image(url=f'{url_image}')
            embed.set_footer(text=f'EVENTO CONCLUÍDO\nObrigado(a) pela presença de todos.',
                             icon_url=ICON_URL,
            )
            return embed
        if url_image != '' and url_image != None:
            embed.set_image(url=f'{url_image}')
        text_footer = embed_antigo.footer.text
        embed.set_footer(text=f'{text_footer}',
                         icon_url=ICON_URL,
        )
        return embed
