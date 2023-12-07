from db.db import bot_request


def get_data(conn: object, access_token: object) -> object:
    candidat = bot_request(conn)
    candidat_name = candidat[0][0]
    candidat_id = candidat[0][1]
    candidat_photo = [str(i[-1]) for i in candidat]
    attachment = f'photo{candidat_id}_{candidat_photo[0]}_{access_token},photo{candidat_id}_{candidat_photo[1]}_{access_token},photo{candidat_id}_{candidat_photo[2]}_{access_token}'
    list_data = [candidat_name, candidat_id, attachment]
    return  list_data

