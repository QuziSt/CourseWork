from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import requests
from vk import VK
from progress.bar import IncrementalBar
import os
import time
import json


class GoogleDriveClass:
	def __init__(self, directory):
		self.directory = directory
		
	def create_and_upload(self):
		access_vk_token = input('Введите токен VK')
		user_id = input('Введите ID пользователя Вконтакте:\n')
		vk = VK(access_vk_token, user_id)
		data = vk.all_photos()
		bar1 = IncrementalBar('Загрузка файлов на компьютер', max=len(data))
		json_result = []
		photos_names = []
		for i in list(data):
			bar1.next()
			photo_info = {}
			photo_url = i
			photo = requests.get(photo_url)
			if data[i][0] in photos_names:
				with open(f'vk_photos/{data[i][1]}.jpg', 'wb') as where_to_save_on_pc:
					where_to_save_on_pc.write(photo.content)
			else:
				with open(f'vk_photos/{data[i][0]}.jpg', 'wb') as where_to_save_on_pc:
					where_to_save_on_pc.write(photo.content)
			json_result.append(photo_info)
			time.sleep(0.33)
		with open(f'vk_photos/json_result.json', 'w') as where_to_save_on_pc:
			json.dump(json_result, where_to_save_on_pc)
		bar1.finish()
		print('Загрузка завершена.')
		
		gauth = GoogleAuth()
		gauth.LocalWebserverAuth()
		
		bar2 = IncrementalBar('Загрузка файлов на Google Drive', max=len(os.listdir(self.directory)))
		drive = GoogleDrive(gauth)
		for file_name in os.listdir(self.directory):
			bar2.next()
			file = drive.CreateFile({'parents': [{'id': '1qpWu7PbQct3iuWWNA_lcsadbTUWDQoHC'}]})
			file.SetContentFile(os.path.join(self.directory, file_name))
			file.Upload()
			time.sleep(0.33)
		bar2.finish()
		print('Загрузка завершена.')
	