import requests
from pick import pick

class VK:
	def __init__(self, token, user_id, version='5.131'):
		self.token = token
		self.id = user_id
		self.version = version
		self.params = {'access_token': self.token, 'v': self.version}
	
	def download_photos(self, count=5):
		where_from = {'Профиль': 'profile',
		              'Стена': 'wall',
		              'Сохраненные': 'saved'}
		where, index = pick(list(where_from.keys()), 'Откуда взять фотографии?', indicator='=>')
		url = 'https://api.vk.com/method/photos.get'
		
		params = {'owner_id': self.id, 'rev': 0, 'extended': 1, 'count': f'{count}', 'type': 'z',
		          'access_token': self.token, 'album_id': f'{where_from[where]}', 'v': '5.131'}
		photos = requests.get(url, params=params)
		return photos.json()
	
	def all_photos(self):
		data = self.download_photos()
		photo_urls = {}
		for photo in data['response']['items']:
			photo_urls.setdefault(photo['sizes'][-1]['url'], [photo['likes']['count'], photo['date'],
			                                                  photo['sizes'][-1]['type']])
		return photo_urls
		

