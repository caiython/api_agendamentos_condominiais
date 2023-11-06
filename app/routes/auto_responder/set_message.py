from app import db, Area, CacheUsuario, Horario, Agendamento
from .responses import Responses
from datetime import datetime
from sqlalchemy import func

def set_message(sender_message, cache_instance, user, condominio):

    if cache_instance.conteudo == '0':
        cache_instance.conteudo = '0_01'
        db.session.commit()
        return Responses.welcome(condominio.nome)
    
    elif cache_instance.conteudo == '0_01':
        expected_message = {
            '01': ['1', '01', 'reservas de espaços'],
            'f': ['f', 'finalizar', 'sair', 'cancelar', 'fechar']
        }
        if sender_message.lower() in expected_message['01']:
            cache_instance.conteudo = '0_01_01'
            db.session.commit()
            return Responses.space_reservation()
        elif sender_message.lower() in expected_message['f']:
            cache_instance.conteudo = '0'
            db.session.commit()
            return Responses.thank_you(condominio.nome)
        else:
            return Responses.invalid_code()

    elif cache_instance.conteudo == '0_01_01':
        expected_message = {
            '01': ['1', '01', 'realizar agendamento'],
            '02': ['2', '02', 'ver meus agendamentos'],
            'f': ['f', 'finalizar', 'sair', 'cancelar', 'fechar']
        }
        if sender_message.lower() in expected_message['01']:
            cache_instance.conteudo = '0_01_01_01'
            db.session.commit()
            return Responses.choose_area(condominio)
        elif sender_message.lower() in expected_message['02']:
            cache_instance.conteudo = '0_01_01_02'
            db.session.commit()
            agendamentos = Agendamento.query.filter(Agendamento.usuario==user, Agendamento.condominio==condominio, Agendamento.status=='agendado').all()
            return Responses.my_schedules(agendamentos)
        elif sender_message.lower() in expected_message['f']:
            cache_instance.conteudo = '0'
            db.session.commit()
            return Responses.thank_you(condominio.nome)
        else:
            return Responses.invalid_code()
    elif cache_instance.conteudo == '0_01_01_01':
        expected_message = {
            'f': ['f', 'finalizar', 'sair', 'cancelar', 'fechar']
        }
        if sender_message.lower() in expected_message['f']:
            cache_instance.conteudo = '0'
            db.session.commit()
            return Responses.thank_you(condominio.nome)
        else:
            area = Area.query.filter_by(area_id=sender_message.lower(), condominio=condominio).first()
            if area is None:
                return Responses.invalid_code()
            else:
                cache_instance.conteudo = '0_01_01_01_01'
                db.session.commit()
                cache_area_id = CacheUsuario(tipo='area_id',conteudo=area.area_id,usuario=user,condominio=condominio)
                db.session.add(cache_area_id)
                db.session.commit()
                return Responses.choose_date()
    elif cache_instance.conteudo == '0_01_01_01_01':
        expected_message = {
            'f': ['f', 'finalizar', 'sair', 'cancelar', 'fechar']
        }

        if sender_message.lower() in expected_message['f']:
            cache_instance.conteudo = '0'
            CacheUsuario.query.filter(CacheUsuario.usuario_id == user.usuario_id, CacheUsuario.tipo != 'instance').delete()
            db.session.commit()
            return Responses.thank_you(condominio.nome)
        else:
            try:
                user_input_date = datetime.strptime(sender_message, f"%d/%m/%y").date()
            except:
                return Responses.invalid_code()
            
            area_id = CacheUsuario.query.filter(CacheUsuario.usuario_id == user.usuario_id,CacheUsuario.condominio_id == condominio.condominio_id,CacheUsuario.tipo == 'area_id').first().conteudo
            area = Area.query.filter_by(area_id=area_id, condominio=condominio).first()
            
            dias_da_semana_unicos = db.session.query(Horario.dia_da_semana).join(Area.horarios).filter(Area.condominio_id == condominio.condominio_id, Area.area_id == area_id).distinct().all()
            dias_da_semana_unicos = converte_dias_da_semana_unicos(dias_da_semana_unicos)
            
            user_input_weekday = user_input_date.weekday()
            user_input_weekday_text = converte_dia_da_semana_numero_para_texto(user_input_weekday)

            if user_input_weekday in dias_da_semana_unicos:
                
                horarios_disponiveis = db.session.query(Horario.horario_id, Horario.horario).join(Area.horarios).filter(Area.condominio == condominio,Area.area_id == area.area_id,Horario.dia_da_semana == user_input_weekday_text).all()
                
                agendamentos = Agendamento.query.filter(func.DATE(Agendamento.data_hora) == user_input_date, Agendamento.status == 'agendado', Agendamento.condominio == condominio, Agendamento.area == area).all()
                horarios_agendados = [agendamento.data_hora.time() for agendamento in agendamentos]

                horarios_disponiveis = [horario for horario in horarios_disponiveis if horario[1] not in horarios_agendados]

                if len(horarios_disponiveis) == 0:
                    return Responses.no_schedule_for_selected_date(area.nome, sender_message)

                cache_instance.conteudo = '0_01_01_01_01_01'
                date = CacheUsuario(tipo='date',conteudo=user_input_date,usuario=user,condominio=condominio)
                db.session.add(date)
                db.session.commit()
                return Responses.choose_schedule(horarios_disponiveis)
            else:
                return Responses.no_weekday_for_selected_date(area.nome, user_input_weekday_text)

    elif cache_instance.conteudo == '0_01_01_01_01_01':
        expected_message = {
            'f': ['f', 'finalizar', 'sair', 'cancelar', 'fechar']
        }
        if sender_message.lower() in expected_message['f']:
            cache_instance.conteudo = '0'
            CacheUsuario.query.filter(CacheUsuario.usuario_id == user.usuario_id, CacheUsuario.tipo != 'instance').delete()
            db.session.commit()
            return Responses.thank_you(condominio.nome)
        else:
            area_id = CacheUsuario.query.filter(CacheUsuario.usuario_id == user.usuario_id,CacheUsuario.condominio_id == condominio.condominio_id,CacheUsuario.tipo == 'area_id').first().conteudo
            area = Area.query.filter_by(area_id=area_id, condominio=condominio).first()
            date_cache = datetime.strptime(CacheUsuario.query.filter(CacheUsuario.tipo == 'date').first().conteudo, f'%Y-%m-%d').date()
            weekday_cache = converte_dia_da_semana_numero_para_texto(date_cache.weekday())

            horarios_disponiveis = db.session.query(Horario.horario_id, Horario.horario).join(Area.horarios).filter(Area.condominio == condominio,Area.area_id == area_id,Horario.dia_da_semana == weekday_cache).all()
            agendamentos = Agendamento.query.filter(func.DATE(Agendamento.data_hora) == date_cache, Agendamento.status == 'agendado', Agendamento.condominio == condominio, Agendamento.area == area).all()
            horarios_agendados = [agendamento.data_hora.time() for agendamento in agendamentos]
            horarios_disponiveis = [horario for horario in horarios_disponiveis if horario[1] not in horarios_agendados]
            
            for horario in horarios_disponiveis:
                if sender_message == str(horario[0]):

                    schedule_datetime = datetime.combine(date_cache, horario[1])
                    new_schedule = Agendamento(data_hora=schedule_datetime, status='agendado', usuario=user, condominio=condominio, area=area)
                    db.session.add(new_schedule)
                    cache_instance.conteudo = '0'
                    CacheUsuario.query.filter(CacheUsuario.usuario_id == user.usuario_id, CacheUsuario.tipo != 'instance').delete()
                    db.session.commit()
                    return Responses.scheduling_finish(area.nome, horario[1].strftime("%Hh"), date_cache.strftime(f"%d/%m/%y"), condominio.nome)

            return Responses.invalid_code()
    
    elif cache_instance.conteudo == '0_01_01_02':
        expected_message = {
            'f': ['f', 'finalizar', 'sair', 'cancelar', 'fechar']
        }
        if sender_message.lower() in expected_message['f']:
            cache_instance.conteudo = '0'
            db.session.commit()
            return Responses.thank_you(condominio.nome)
        else:
            agendamento = Agendamento.query.filter(Agendamento.agendamento_id==sender_message, Agendamento.usuario==user, Agendamento.condominio==condominio, Agendamento.status=='agendado').first()
            
            if agendamento is None:
                return Responses.invalid_code()
            
            agendamento.status = 'cancelado'
            cache_instance.conteudo = '0'
            db.session.commit()

            return Responses.schedule_cancel(agendamento.agendamento_id, condominio.nome)


def converte_dias_da_semana_unicos(dias_da_semana_unicos):
    output = []
    for tuple in dias_da_semana_unicos:
        dia_da_semana = tuple[0]
        if dia_da_semana == 'segunda-feira':
            output.append(0)
        elif dia_da_semana == 'terça-feira':
            output.append(1)
        elif dia_da_semana == 'quarta-feira':
            output.append(2)
        elif dia_da_semana == 'quinta-feira':
            output.append(3)
        elif dia_da_semana == 'sexta-feira':
            output.append(4)
        elif dia_da_semana == 'sábado':
            output.append(5)
        else:
            output.append(6)
    return output

def converte_dia_da_semana_numero_para_texto(weekday):
    if weekday == 0:
        return 'segunda-feira'
    elif weekday == 1:
        return 'terça-feira'
    elif weekday == 2:
        return 'quarta-feira'
    elif weekday == 3:
        return 'quinta-feira'
    elif weekday == 4:
        return 'sexta-feira'
    elif weekday == 5:
        return 'sábado'
    else:
        return 'domingo'