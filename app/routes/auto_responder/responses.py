from app import Area

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
    
    def choose_date():
        text = '''Digite a data desejada no seguinte formato:
👉 *dd/mm/aa*

*Exemplo*: 23/12/23

❌ Caso deseje finalizar o autoatendimento, digite *F*.'''
        
        return text
    
    def no_weekday_for_selected_date(nome_da_area, dia_da_semana):
        text = f'''❌ A área *{nome_da_area}* não possui agendamentos para os dias da semana de *{dia_da_semana}*.

Por favor, insira outra data ou entre em contato com o administrador do condomínio para inclusão do dia da semana informado.'''
        
        return text
    
    def no_schedule_for_selected_date(nome_da_area, data):
        text = f'''🙁 Não há disponibilidade de horário para a área *{nome_da_area}* na data *{data}*.

Por favor, insira outra data.'''
        
        return text

    def choose_area(condominio):
        text = '🏖️ Selecione um espaço:\n\n'
        
        areas = Area.query.filter_by(condominio=condominio).all()
        for area in areas:
            text += f'*[{area.area_id}]* - {area.nome}\n'
        
        text += '''
*[F]* - Finalizar Autoatendimento ❌

☝️ Digite o código referente à opção desejada.'''
        
        return text

    def choose_schedule(horarios_disponiveis):
        text = '⏰ Selecione um horário disponível:\n\n'

        for horario in horarios_disponiveis:
            text += f'*[{horario[0]}]* - {horario[1].strftime("%Hh")}\n'
        
        text += '''
*[F]* - Finalizar Autoatendimento ❌

☝️ Digite o código referente à opção desejada.'''
        
        return text
    
    def scheduling_finish(area_name, horario, date, nome_condominio):
        text = f'''✅ Agendamento realizado!
Local: *{area_name}*
Horário: *{horario}*
Data: *{date}*
        
🏁 O autoatendimento foi finalizado. Envie uma nova mensagem para iniciar outro atendimento.

O condomínio *{nome_condominio}* agradece o contato! 😄

🤖 _Sistema Desenvolvido por *@caiocvl*._'''
        
        return text
    
    def my_schedules(agendamentos):
        text = f"📅 Meus agendamentos:\n\n"

        for agendamento in agendamentos:
            text += f'''*Agendamento {agendamento.agendamento_id}*
Espaço: {agendamento.area.nome}
Data: {agendamento.data_hora.date().strftime(f'%d/%m/%Y')}
Horário: {agendamento.data_hora.time().strftime(f'%Hh')}\n\n'''
        
        text += '''☝️ Digite *F* para finalizar o autoatendimento ou digite o número referente ao agendamento para cancelá-lo.'''
        return text

    def schedule_cancel(agendamento_id, nome_condominio):
        text = f'''O agendamento {agendamento_id} foi cancelado com sucesso.

🏁 O autoatendimento foi finalizado. Envie uma nova mensagem para iniciar outro atendimento.

O condomínio *{nome_condominio}* agradece o contato! 😄

🤖 _Sistema Desenvolvido por *@caiython*._'''
        
        return text

    def thank_you(nome_condominio):
        
        text = f'''🏁 O autoatendimento foi finalizado. Envie uma nova mensagem para iniciar outro atendimento.

O condomínio *{nome_condominio}* agradece o contato! 😄

🤖 _Sistema Desenvolvido por *caiython*._'''
        
        return text

    def invalid_code():
        
        text = '❌ Código inválido. Por favor, envie o código corretamente ou digite *F* para finalizar o atendimento.'
        
        return text
