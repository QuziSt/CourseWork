import requests

class VK:
	def __init__(self, token, user_id, count=5, album='profile', version='5.131'):
		self.token = token
		self.id = user_id
		self.version = version
		self.count = count
		self.album = album
		self.params = {'access_token': self.token, 'v': self.version}
		
	def get_user_id(self):
		url = 'https://api.vk.com/method/users.get'
		params = {'user_ids': f'{self.id}', 'access_token': f'{self.token}', 'v': '5.131'}
		user_id = requests.get(url, params=params)
		self.id = str(user_id.json()['response'][0]['id'])
		return self.id
		
	def download_photos(self):
		
		url = 'https://api.vk.com/method/photos.get'
		
		params = {'owner_id': self.get_user_id(), 'rev': 0, 'extended': 1, 'count': f'{self.count}', 'type': 'z',
		          'access_token': self.token, 'album_id': f'{self.album}', 'v': '5.131'}
		photos = requests.get(url, params=params)
		return photos.json()
	
	def all_photos(self):
		data = self.download_photos()
		photo_urls = {}
		for photo in data['response']['items']:
			photo_urls.setdefault(photo['sizes'][-1]['url'], [photo['likes']['count'], photo['date'],
		                                           photo['sizes'][-1]['type']])
		return photo_urls

		

