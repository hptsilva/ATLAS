import discord

COLOR_ATLAS = 0x1414b8

class Reacoes_Enquete:

    # Edita a mensagem da enquete quando um membre usa alguma reação
    async def reacoes(self, message, user, reacao):

        embed_antigo = message.embeds[0]
        campo_sim = embed_antigo.fields[2]
        value_sim = campo_sim.value
        campo_nao = embed_antigo.fields[3]
        value_nao = campo_nao.value
        campo_talvez = embed_antigo.fields[4]
        value_talvez = campo_talvez.value
        url_image = embed_antigo.image.url
        if embed_antigo.description is None:
            embed= discord.Embed(title=f'{embed_antigo.title}',
                                 color=COLOR_ATLAS)
        else:
            embed = discord.Embed(title=f'{embed_antigo.title}',
                                  description=f'{embed_antigo.description}',
                                  color=COLOR_ATLAS)
        embed.add_field(name='Opções:', value='| ✅ - Sim | ⛔ - Não | ❔ - Talvez |', inline=False)
        # Se a reação for ✅
        if reacao == 1:
            mencoes_sim = value_sim.split('\n')
            mencoes_nao = value_nao.split('\n')
            mencoes_talvez = value_talvez.split('\n')
            # retira o dono da reação na lista
            cond = 0
            for nome in mencoes_sim:
                if nome == f'{user.name}':
                    mencoes_sim.remove(nome)
                    cond = 1
            for nome in mencoes_nao:
                if nome == f'{user.name}':
                    mencoes_nao.remove(nome)
            for nome in mencoes_talvez:
                if nome == f'{user.name}':
                    mencoes_talvez.remove(nome)
            # Adiciona o dono na reação na lista
            if cond == 0:
                mencoes_sim.append(user.name)
            mencoes1 = "\n".join([f"{nome}" for nome in mencoes_sim])
            mencoes2 = "\n".join([f"{nome}" for nome in mencoes_nao])
            mencoes3 = "\n".join([f"{nome}" for nome in mencoes_talvez])
            url_image = embed_antigo.image.url
            embed.timestamp = embed_antigo.timestamp
            embed.add_field(name='Horário:', value=f'<t:{int(embed.timestamp.timestamp())}:f>', inline=False)
            embed.add_field(name='✅ Nomes:', value=f'{mencoes1}', inline=True)
            embed.add_field(name='⛔ Nomes:', value=f'{mencoes2}', inline=True)
            embed.add_field(name='❔ Nomes:', value=f'{mencoes3}', inline=True)
        # Se a reação for ⛔
        elif reacao == 2:
            # retira o dono da reação na lista
            mencoes_sim = value_sim.split('\n')
            mencoes_nao = value_nao.split('\n')
            mencoes_talvez = value_talvez.split('\n')
            # retira o dono da reação na lista
            cond = 0
            for nome in mencoes_sim:
                if nome == f'{user.name}':
                    mencoes_sim.remove(nome)
            for nome in mencoes_nao:
                if nome == f'{user.name}':
                    mencoes_nao.remove(nome)
                    cond = 1
            for nome in mencoes_talvez:
                if nome == f'{user.name}':
                    mencoes_talvez.remove(nome)
            # Adiciona o dono na reação na lista
            if cond == 0:
                mencoes_nao.append(user.name)
            mencoes1 = "\n".join([f"{nome}" for nome in mencoes_sim])
            mencoes2 = "\n".join([f"{nome}" for nome in mencoes_nao])
            mencoes3 = "\n".join([f"{nome}" for nome in mencoes_talvez])
            url_image = embed_antigo.image.url
            embed.timestamp = embed_antigo.timestamp
            embed.add_field(name='Horário:', value=f'<t:{int(embed.timestamp.timestamp())}:f>', inline=False)
            embed.add_field(name='✅ Nomes:', value=f'{mencoes1}', inline=True)
            embed.add_field(name='⛔ Nomes:', value=f'{mencoes2}', inline=True)
            embed.add_field(name='❔ Nomes:', value=f'{mencoes3}', inline=True)
        # Se a reação for ❔
        elif reacao == 3:
            mencoes_sim = value_sim.split('\n')
            mencoes_nao = value_nao.split('\n')
            mencoes_talvez = value_talvez.split('\n')
            # retira o dono da reação na lista
            cond = 0
            for nome in mencoes_sim:
                if nome == f'{user.name}':
                    mencoes_sim.remove(nome)
            for nome in mencoes_nao:
                if nome == f'{user.name}':
                    mencoes_nao.remove(nome)
            for nome in mencoes_talvez:
                if nome == f'{user.name}':
                    mencoes_talvez.remove(nome)
                    cond = 1
            # Adiciona o dono na reação na lista
            if cond == 0:
                mencoes_talvez.append(user.name)
            mencoes1 = "\n".join([f"{nome}" for nome in mencoes_sim])
            mencoes2 = "\n".join([f"{nome}" for nome in mencoes_nao])
            mencoes3 = "\n".join([f"{nome}" for nome in mencoes_talvez])
            url_image = embed_antigo.image.url
            embed.timestamp = embed_antigo.timestamp
            embed.add_field(name='Horário:', value=f'<t:{int(embed.timestamp.timestamp())}:f>', inline=False)
            embed.add_field(name='✅ Nomes:', value=f'{mencoes1}', inline=True)
            embed.add_field(name='⛔ Nomes:', value=f'{mencoes2}', inline=True)
            embed.add_field(name='❔ Nomes:', value=f'{mencoes3}', inline=True)
        else:
            url_image = embed_antigo.image.url
            embed.timestamp = embed_antigo.timestamp
            embed.add_field(name='Horário:', value=f'<t:{int(embed.timestamp.timestamp())}:f>', inline=False)
            embed.add_field(name='✅ Nomes:', value=f'{value_sim}', inline=True)
            embed.add_field(name='⛔ Nomes:', value=f'{value_nao}', inline=True)
            embed.add_field(name='❔ Nomes:', value=f'{value_talvez}', inline=True)
            embed.set_image(url=f'{url_image}')
            embed.set_footer(text=f'O EVENTO FOI CANCELADO')
            return embed
        embed.set_image(url=f'{url_image}')
        footer = embed_antigo.footer.text
        embed.set_footer(text=f'{footer}')
        return embed


