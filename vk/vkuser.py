import requests
from tqdm import tqdm


class VKUser:

    url = 'https://api.vk.com/method'

    def __init__(self, token, id):
        self.token = token
        self.id = id

    def common_params(self):
        return {
            'access_token': self.token,
            'v': '5.199'
        }

    def get_data_user(self):
        method = '/account.getProfileInfo'
        params = self.common_params()
        response = requests.get(f'{self.url}{method}', params=params)
        return response.json()['response']

    def get_list_users(self):
        data_user = self.get_data_user()
        sex_user = data_user['sex']
        bdate_user = data_user['bdate'][-4:]
        city_user = data_user['city']['id']
        method = '/users.search'
        fields = 'sex, city, bdate'
        params = self.common_params()
        params.update({
            'birth_year': bdate_user,
            'count': 1000,
            'fields': fields,

        })
        response = requests.get(f'{self.url}{method}', params=params)
        data = response.json()['response']['items']
        data_db = []
        for i in tqdm(data):
            try:
                if i['id'] != self.id and i['sex'] != sex_user and i['city']['id'] == city_user:
                    photo = self.get_photo(i['id'])
                    if photo is not None:
                        data_db.append({
                                'user_id': i['id'],
                                'user_name': f'{i["first_name"]} {i["last_name"]}',
                                'bdate': i['bdate'],
                                'sex': i['sex'],
                                'city': i['city']['title'],
                                'link': f'https://vk.com/id{i["id"]}',
                                'photos': photo
                        })

            except KeyError:
                pass
        return data_db

    def get_photo(self, id):
        method = '/photos.get'
        params = self.common_params()
        params.update({
            'owner_id': id,
            'extended': 1,
            'album_id': 'profile'
        })
        response = requests.get(f'{self.url}{method}', params=params)
        photos = []
        for i in response.json()['response']['items']:
            photos.append({'likes': i['likes']['count'], 'photo': i["id"]})
        new_photo = sorted(photos, key=lambda x: x['likes'], reverse=True)
        if len(new_photo) >= 3:
            return new_photo[:3]
        else:
            pass
