import configparser

import psycopg2

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from VK.functions import get_data
from db.db import bd_data, update_label_2, update_label_3, get_list_elect


def send_some_msg(id, some_text, attach, keyboard):
    vk.messages.send(user_id=id, message=some_text, attachment=attach, random_id=0, keyboard=keyboard)


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read("setting.ini")
    group_token = config.get('GROUP', 'token')
    access_token = config.get('USER', 'token')
    database = config.get('db', 'database')
    user = config.get('db', 'user')
    password = config.get('db', 'password')
    vk_session = vk_api.VkApi(token=group_token)
    vk = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    label = 0
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                msg = event.text.lower()
                id = event.user_id
                keyboard = VkKeyboard()
                buttons = ['Пропустить', 'В избранное', 'Список избранных']
                button_colors = [VkKeyboardColor.PRIMARY, VkKeyboardColor.POSITIVE, VkKeyboardColor.NEGATIVE]
                for btn, btn_clr in zip(buttons, button_colors):
                    keyboard.add_button(btn, btn_clr)
                with psycopg2.connect(database=database, user=user, password=password ) as conn:
                    if msg == "привет":
                        send_some_msg(id, f'Привет!\n Подожди, пожалуйста, подбираю кандидатов....', None, None)
                        bd_data(conn, access_token, id)
                        try:
                            data = get_data(conn, access_token)
                            send_some_msg(id, f'{data[0]}\n https://vk.com/id{data[1]}\n', data[2], keyboard.get_keyboard())
                            label = data[1]
                        except Exception:
                            send_some_msg(id, f'Кандидатов нет!', None, None)
                    elif msg == "пропустить":
                        update_label_2(conn, label)
                        try:
                            data = get_data(conn, access_token)
                            send_some_msg(id, f'{data[0]}\n https://vk.com/id{data[1]}\n', data[2], keyboard.get_keyboard())
                            label = data[1]
                        except Exception:
                            send_some_msg(id, f'Кандидаты отсутствуют!', None, None)
                            send_some_msg(id, f'Нажмите кнопку "Список избранных", чтобы увидеть кандидатов, которых Вы выбрали!',
                                          None, None)
                    elif msg == 'в избранное':
                        update_label_3(conn, label)
                        try:
                            data = get_data(conn, access_token)
                            send_some_msg(id, f'{data[0]}\n https://vk.com/id{data[1]}\n', data[2], keyboard.get_keyboard())
                            label = data[1]
                        except Exception:
                            send_some_msg(id, f'Кандидаты отсутствуют!', None, None)
                            send_some_msg(id, f'Нажмите кнопку "Список избранных", чтобы увидеть кандидатов, которых Вы выбрали!',
                                          None, None)

                    elif msg == 'список избранных':
                        candidats = get_list_elect(conn)
                        if len(candidats) !=0:
                            for candidat in candidats:
                                candidat_name = candidat[0]
                                candidat_id = candidat[1]
                                send_some_msg(id, f'{candidat_name}\n https://vk.com/id{candidat_id}\n', None, None)
                        else:
                            send_some_msg(id, f'Список избранных пуст!', None, None)

                    else:
                        send_some_msg(id, f'Для начала работы напиши: Привет',  None, None)