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
# Comandos possíveis:

* /avatar  
![image](https://github.com/user-attachments/assets/e3da74ff-653a-48af-95c0-ed80eda289e2)
* /evento  
![image](https://github.com/user-attachments/assets/bf1b7552-ba94-48b1-8b32-3fe3a6e4a01c)
* (Modelo da mensagem do evento)  
![Captura de tela de 2024-11-19 17-47-34](https://github.com/user-attachments/assets/9b0feec2-1033-44a4-89f6-21ad03ab00cd)
* (Janela para editar o evento)  
![editar-evento](https://github.com/user-attachments/assets/5d6306e1-3893-4d70-86a2-2c12606b09cc)
* Mensagem de boas-vindas  
![boas vindas](https://github.com/user-attachments/assets/7e5db295-7013-4731-afe4-99db37baec08)

