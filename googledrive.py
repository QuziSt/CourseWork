from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import requests
from vk import VK
from progress.bar import IncrementalBar
import os
import time
from pick import pick
import configparser


class GoogleDriveClass:
	def __init__(self, directory):
		self.directory = directory
		
	def create_and_upload(self):
		config = configparser.ConfigParser()
		config.read('tokens.ini')
		access_vk_token = config['vk']['vk_token']
		user_id = input('Введите ID пользователя Вконтакте или короткое имя профиля:\n')
		count = input('Какое количество фотографий Вы хотите получить?\n')
		while not count.isdigit():
			count = input('Какое количество фотографий Вы хотите получить?\n')
		where_from = {'Профиль': 'profile',
		              'Стена': 'wall',
		              'Сохраненные': 'saved'}
		where, index = pick(list(where_from.keys()), 'Откуда взять фотографии?', indicator='=>')
		album = where_from[where]
		vk = VK(access_vk_token, user_id, count, album)
		data = vk.all_photos()
		bar1 = IncrementalBar('Загрузка файлов на компьютер', max=len(data))
		photos_names = []
		for i in list(data):
			bar1.next()
			photo_url = i
			photo = requests.get(photo_url)
			if data[i][0] in photos_names:
				with open(f'vk_photos/{data[i][1]}.jpg', 'wb') as where_to_save_on_pc:
					where_to_save_on_pc.write(photo.content)
			else:
				with open(f'vk_photos/{data[i][0]}.jpg', 'wb') as where_to_save_on_pc:
					where_to_save_on_pc.write(photo.content)
			time.sleep(0.33)
		bar1.finish()
		print('Загрузка завершена.')
		
		gauth = GoogleAuth()
		gauth.LocalWebserverAuth()
		folder_id = input('Укажите ID папки в диске:\n')
		
		bar2 = IncrementalBar('Загрузка файлов на Google Drive', max=len(os.listdir(self.directory)))
		drive = GoogleDrive(gauth)
		for file_name in os.listdir(self.directory):
			bar2.next()
			file = drive.CreateFile({'parents': [{'id': f'{folder_id}'}]})
			file.SetContentFile(os.path.join(self.directory, file_name))
			file.Upload()
			time.sleep(0.33)
		bar2.finish()
		print('Загрузка завершена.')
	