class Responses:

    def welcome(condominio_nome):

        text = f'''Seja bem vindo(a) ao autoatendimento do condomínio *{condominio_nome}* 🏠

👉 Opções:

*[01]* - 📅 Agendamentos

*[F]* - Finalizar Autoatendimento ❌

☝️ Digite o código referente à opção desejada.'''

        return text


    def space_reservation():

        text = '''👉 Opções:
        
*[01]* - Realizar agendamento 🗓️
*[02]* - Ver meus agendamentos 👁️

*[F]* - Finalizar Autoatendimento ❌

☝️ Digite o código referente à opção desejada.'''

        return text

    def thank_you(nome_condominio):
        
        text = f'''O autoatendimento foi finalizado. O *{nome_condominio}* agradece o contato! 😄

🤖 _Sistema Desenvolvido por *@caiocvl*._'''
        
        return text

    def invalid_code():
        
        text = '❌ Código inválido. Por favor, envie o código corretamente ou digite *F* para finalizar o atendimento.'
        
        return text
