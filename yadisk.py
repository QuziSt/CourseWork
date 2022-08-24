from vk import VK
import requests
import json
import time
import os
from progress.bar import IncrementalBar




class YaDisk:
	def __init__(self, token):
		self.token = token
	
	def get_upload_url(self, filename='all_photos.json'):
		url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
		upload_url = requests.get(url, headers={'Content-Type': 'application/json',
		                           'Authorization': f'OAuth {self.token}'},
									params={'overwrite': 'true', 'path': f'vk/{filename}'})
		return upload_url.json()
		
	def upload_photos(self):
		access_vk_token = input('Введите токен VK')
		user_id = input('Введите ID пользователя Вконтакте:\n')
		vk = VK(access_vk_token, user_id)
		os.system('cls||clear')
		url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
		data = vk.all_photos()
		bar = IncrementalBar('Загрузка', max=len(data))
		json_result = []
		photos_names = []
		for i in list(data):
			bar.next()
			photo_info = {}
			if data[i][0] in photos_names:
				params = {'path': f'/vk/{data[i][1]}.jpg', 'url': f'{i}'}
				photo_info = {'file_name': data[i][1], 'size': data[i][-1]}
			else:
				params = {'path': f'/vk/{data[i][0]}.jpg', 'url': f'{i}'}
				photo_info = {'file_name': data[i][0], 'size': data[i][-1]}
				photos_names.append(data[i][0])
			headers = {'Authorization': f'OAuth {self.token}'}
			requests.post(url, params=params, headers=headers)
			json_result.append(photo_info)
			time.sleep(0.33)
		bar.finish()
		print('Загрузка завершена')
		with open('all_photos.json', 'w') as result:
			json.dump(json_result, result, indent=4)
		requests.put(self.get_upload_url().get('href', ''), data=open('all_photos.json', 'rb'))
		