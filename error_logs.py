class Error_Logs:

     #Salva o log de mensagem no arquivo de texto
     def salvar_log(log):
        with open('log.txt', 'a') as log_file:
            log_file.write(log)
