- Bot para o aplicativo Discord. Utilizo a API Wrapper em Python conforme o reposítorio https://github.com/Rapptz/discord.py. A documentação está presente no link: https://discordpy.readthedocs.io/en/latest/index.html
* Utiliza a sistema de gerenciamento de banco de dados MySQL.
* Para executar o programa é preciso criar as variaveis de ambiente usando a biblioteca Python Decouple.
* Para obter o token da aplicação é necessário gerá-lo no site https://discord.com/developers/applications.
* A aplicação precisa ter a permissão de administrador e o cargo do bot esteja no topo da hierarquia no servidor para o funcionamento correto de certos comandos.
# Instalação da biblioteca discord.py
* Para instalar a biblioteca discord.py sem o total suporte por voz use o comando abaixo:
```
  # Linux/macOS
  python3 -m pip install -U discord.py
  # Windows
  py -3 -m pip install -U discord.py
```
* Para instalar a versão de desenvolvimento:
```
  $ git clone https://github.com/Rapptz/discord.py
  $ cd discord.py
  $ python3 -m pip install -U .[voice]
```
# Comandos:

* Lista completa de comandos do bot:  
![comandos](https://github.com/user-attachments/assets/caa44c05-7e08-4628-889a-09872d9e5376)
* /avatar  
![avatar](https://github.com/hptsilva/ATLAS-DISCORD-BOT/assets/41704578/cdc2f988-8361-4b1f-98b8-6314ca9acb9c)
* /evento  
![evento](https://github.com/user-attachments/assets/a0646983-12e9-49b3-9c7e-96d5288fc639)
* (Modelo da mensagem para um evento)  
![evento](https://github.com/user-attachments/assets/9ec40bf3-c5cb-4d90-9471-a2189630007f)
* (Janela para editar a mensagem)  
![editar-evento](https://github.com/user-attachments/assets/5d6306e1-3893-4d70-86a2-2c12606b09cc)
* Mensagem de boas-vindas  
![boas vindas](https://github.com/user-attachments/assets/7e5db295-7013-4731-afe4-99db37baec08)

