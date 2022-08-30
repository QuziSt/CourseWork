from pick import pick
from yadisk import *
from googledrive import GoogleDriveClass
import os
import configparser
import json


def start_programm():
	commands = {'Яндекс.Диск': ya_disk,
	            'Гугл Диск': google_disk}
	answer, index = pick(['Яндекс.Диск', 'Гугл Диск'], 'Куда загрузить фотографии?', indicator='=>')
	commands[answer]()
	
	
def create_json(some_json):
	data = some_json
	json_result = []
	photos_names = []
	for i in list(data):
		photo_info = {}
		if data[i][0] in photos_names:
			photo_info = {'file_name': data[i][1], 'size': data[i][-1]}
		else:
			photo_info = {'file_name': data[i][0], 'size': data[i][-1]}
			photos_names.append(data[i][0])
		json_result.append(photo_info)
	with open('all_photos.json', 'w') as result:
		json.dump(json_result, result, indent=4)
	
	
def google_disk():
	os.system('cls||clear')
	gdrive = GoogleDriveClass(input('Ведите полный путь до папки с файлами:\n'))
	gdrive.create_and_upload()
	
	
def ya_disk():
	os.system('cls||clear')
	config = configparser.ConfigParser()
	config.read('tokens.ini')
	access_yadisk_token = config['Yandex']['ya_token']
	folder_name = input('Введите название папки, куда сохранить фотографии:\n')
	yadisk = YaDisk(access_yadisk_token, folder_name)
	yadisk.create_folder()
	yadisk.upload_photos()
	
	
if __name__ == '__main__':
	os.system('cls||clear')
	start_programm()

