Bot em desenvolvimento para fins de aprendizagem. Utilize a API Wrapper em Python conforme o reposítorio https://github.com/Rapptz/discord.py. A documentação está presente no link: https://discordpy.readthedocs.io/en/latest/index.html
* Utiliza a sistema de gerenciamento de banco de dados MySQL.
* Para executar o programa é preciso criar as variaveis de ambiente usando a biblioteca Python Decouple.
* Para obter o token da aplicação é necessário gerá-la no site https://discord.com/developers/applications . A aplicação precisa ter a permissão de administrador para o funcionamento correto.
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
