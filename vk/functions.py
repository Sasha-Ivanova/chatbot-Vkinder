import psycopg2

from db.db import bot_request, bd_data, update_label_2, update_label_3, get_list_elect


def get_data(conn: object, access_token: object) -> object:
    candidat = bot_request(conn)
    candidat_name = candidat[0][0]
    candidat_id = candidat[0][1]
    candidat_photo = [str(i[-1]) for i in candidat]
    attachment = (f'photo{candidat_id}_{candidat_photo[0]}_{access_token}, '
                  f'photo{candidat_id}_{candidat_photo[1]}_{access_token}, '
                  f'photo{candidat_id}_{candidat_photo[2]}_{access_token}')
    list_data = [candidat_name, candidat_id, attachment]
    return list_data


def send_some_msg(vk, id, some_text, attach, keyboard):
    vk.messages.send(user_id=id, message=some_text, attachment=attach, random_id=0, keyboard=keyboard)


def get_answed(vk, database, user, password,  msg, keyboard, access_token, id, label):
    with psycopg2.connect(database=database, user=user, password=password) as conn:
        if msg == "привет":
            send_some_msg(vk, id, f'Привет!\n Подожди, пожалуйста, подбираю кандидатов....', None, None)
            bd_data(conn, access_token, id)
            try:
                data = get_data(conn, access_token)
                send_some_msg(vk, id, f'{data[0]}\n https://vk.com/id{data[1]}\n', data[2],
                              keyboard.get_keyboard())
                label = data[1]
                return label
            except Exception:
                send_some_msg(vk, id, f'Кандидатов нет!', None, None)
        elif msg == "пропустить":
            update_label_2(conn, label)
            try:
                data = get_data(conn, access_token)
                send_some_msg(vk, id, f'{data[0]}\n https://vk.com/id{data[1]}\n', data[2],
                              keyboard.get_keyboard())
                label = data[1]
                return label
            except Exception:
                send_some_msg(vk, id, f'Кандидаты отсутствуют!', None, None)
                send_some_msg(vk, id,
                              f'Нажмите кнопку "Список избранных", чтобы увидеть кандидатов, которых Вы выбрали!',
                              None, None)
        elif msg == 'в избранное':
            update_label_3(conn, label)
            try:
                data = get_data(conn, access_token)
                send_some_msg(vk, id, f'{data[0]}\n https://vk.com/id{data[1]}\n', data[2],
                              keyboard.get_keyboard())
                label = data[1]
                return label
            except Exception:
                send_some_msg(vk, id, f'Кандидаты отсутствуют!', None, None)
                send_some_msg(vk, id,
                              f'Нажмите кнопку "Список избранных", чтобы увидеть кандидатов, которых Вы выбрали!',
                              None, None)

        elif msg == 'список избранных':
            candidats = get_list_elect(conn)
            if len(candidats) != 0:
                for candidat in candidats:
                    candidat_name = candidat[0]
                    candidat_id = candidat[1]
                    send_some_msg(vk, id, f'{candidat_name}\n https://vk.com/id{candidat_id}\n', None, None)
            else:
                send_some_msg(vk, id, f'Список избранных пуст!', None, None)

        else:
            send_some_msg(vk, id, f'Для начала работы напиши: Привет', None, None)
