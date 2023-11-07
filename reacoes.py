import discord
import re

class Reacoes_Enquete():
        
    def reacoes(self, reaction, user, reacao, tipo):

        embed_antigo = reaction.message.embeds[0]
        campo_sim = embed_antigo.fields[2]
        value_sim = campo_sim.value
        campo_nao = embed_antigo.fields[3]
        value_nao = campo_nao.value
        campo_talvez = embed_antigo.fields[4]
        value_talvez = campo_talvez.value
        url_image = embed_antigo.image.url
        embed = discord.Embed(title=f'{embed_antigo.title}',
                              description=f'{embed_antigo.description}',
                              color=0xf24f00)
        embed.add_field(name='Presença:', value='✅ - Sim\n❌ - Não\n⚠️ - Talvez', inline=False)
        if reacao == 1:
            mencoes_sim = re.findall(r'<@(\d+)>', value_sim)
            if tipo == 'remove':
                usuarios_sim = [int(id) for id in mencoes_sim]
                if user.id in usuarios_sim:
                    usuarios_sim.remove(user.id)
            else:
                usuarios_sim = [int(id) for id in mencoes_sim]
                usuarios_sim.append(user.id)
            mencoes = "\n".join([f"<@{id}>" for id in usuarios_sim])
            url_image = embed_antigo.image.url
            embed.timestamp = embed_antigo.timestamp
            embed.add_field(name='Horário:', value=f'<t:{int(embed.timestamp.timestamp())}:f>', inline=False)
            embed.add_field(name='Nomes: ✅ - Sim', value=f'{mencoes}', inline=True)
            embed.add_field(name='Nomes: ❌ - Não', value=f'{value_nao}', inline=True)
            embed.add_field(name='Nomes: ⚠️ - Talvez', value=f'{value_talvez}', inline=True)
        elif reacao == 2:
            mencoes_nao = re.findall(r'<@(\d+)>', value_nao)
            if tipo == 'remove':
                usuarios_nao = [int(id) for id in mencoes_nao]
                if user.id in usuarios_nao:
                    usuarios_nao.remove(user.id)
            else:
                usuarios_nao = [int(id) for id in mencoes_nao]
                usuarios_nao.append(user.id)
            mencoes = "\n".join([f"<@{id}>" for id in usuarios_nao])
            url_image = embed_antigo.image.url
            embed.timestamp = embed_antigo.timestamp
            embed.add_field(name='Horário:', value=f'<t:{int(embed.timestamp.timestamp())}:f>', inline=False)
            embed.add_field(name='Nomes: ✅ - Sim', value=f'{value_sim}', inline=True)
            embed.add_field(name='Nomes: ❌ - Não', value=f'{mencoes}', inline=True)
            embed.add_field(name='Nomes: ⚠️ - Talvez', value=f'{value_talvez}', inline=True)
        else:
            mencoes_talvez = re.findall(r'<@(\d+)>', value_talvez)
            if tipo == 'remove':
                usuarios_talvez = [int(id) for id in mencoes_talvez]
                if user.id in usuarios_talvez:
                    usuarios_talvez.remove(user.id)
            else:
                usuarios_talvez = [int(id) for id in mencoes_talvez]
                usuarios_talvez.append(user.id)
            mencoes = "\n".join([f"<@{id}>" for id in usuarios_talvez])
            url_image = embed_antigo.image.url
            embed.timestamp = embed_antigo.timestamp
            embed.add_field(name='Horário:', value=f'<t:{int(embed.timestamp.timestamp())}:f>', inline=False)
            embed.add_field(name='Nomes: ✅ - Sim', value=f'{value_sim}', inline=True)
            embed.add_field(name='Nomes: ❌ - Não', value=f'{value_nao}', inline=True)
            embed.add_field(name='Nomes: ⚠️ - Talvez', value=f'{mencoes}', inline=True)
        embed.set_image(url=f'{url_image}')
        footer = embed_antigo.footer.text
        embed.set_footer(text=f'{footer}')
        return embed