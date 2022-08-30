from vk import VK
import requests
import time
import os
from progress.bar import IncrementalBar
import configparser
from pick import pick
import main

class YaDisk:
	def __init__(self, token, folder_name):
		self.token = token
		self.folder = folder_name
		
	def create_folder(self,):
		url = 'https://cloud-api.yandex.net/v1/disk/resources'
		headers = {'Content-Type': 'application/json',
		           'Authorization': f'OAuth {self.token}'}
		params = {'path': f'{self.folder}/'}
		requests.put(url, headers=headers, params=params)
		
	def get_upload_url(self, filename='all_photos.json'):
		url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
		upload_url = requests.get(url, headers={'Content-Type': 'application/json',
		                           'Authorization': f'OAuth {self.token}'},
									params={'overwrite': 'true', 'path': f'{self.folder}/{filename}'})
		return upload_url.json()
		
	def upload_photos(self):
		config = configparser.ConfigParser()
		config.read('tokens.ini')
		access_vk_token = config['vk']['vk_token']
		user_id = input('Введите ID пользователя Вконтакте или короткое имя профиля:\n')
		count = input('Какое количество фотографий Вы хотите получить?')
		while not count.isdigit():
			count = input('Какое количество фотографий Вы хотите получить?')
		where_from = {'Профиль': 'profile',
		              'Стена': 'wall',
		              'Сохраненные': 'saved'}
		where, index = pick(list(where_from.keys()), 'Откуда взять фотографии?', indicator='=>')
		album = where_from[where]
		vk = VK(access_vk_token, user_id, count, album)
		os.system('cls||clear')
		url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
		data = vk.all_photos()
		bar = IncrementalBar('Загрузка', max=len(data))
		photos_names = []
		for i in list(data):
			bar.next()
			if data[i][0] in photos_names:
				params = {'path': f'/{self.folder}/{data[i][1]}.jpg', 'url': f'{i}'}
			else:
				params = {'path': f'/{self.folder}/{data[i][0]}.jpg', 'url': f'{i}'}
				photos_names.append(data[i][0])
			headers = {'Authorization': f'OAuth {self.token}'}
			requests.post(url, params=params, headers=headers)
			time.sleep(0.33)
		bar.finish()
		print('Загрузка завершена')
		requests.put(self.get_upload_url().get('href', ''), data=open('all_photos.json', 'rb'))
		