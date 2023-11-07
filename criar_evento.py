import discord

class Criar_Evento():

    async def criar_evento(self, name, description, channel, start_time, end_time):
        await discord.Guild.create_scheduled_event(name=name, description=description, 
                                                   channel=channel, 
                                                   start_time=start_time, 
                                                   end_time=end_time, 
                                                   privacy_level=discord.PrivacyLevel.guild_only, 
                                                   entity_type=discord.EntityType.voice)