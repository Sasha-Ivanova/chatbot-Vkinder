import configparser


import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from vk.functions import get_answed


def main(longpoll):
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
                label = get_answed(vk, database, user, password, msg, keyboard, access_token, id, label)


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
    main(longpoll)
