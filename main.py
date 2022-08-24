from pick import pick
from yadisk import YaDisk
from googledrive import GoogleDriveClass
import os

def start_programm():
	commands = {'Яндекс.Диск': ya_disk,
	            'Гугл Диск': google_disk}
	answer, index = pick(['Яндекс.Диск', 'Гугл Диск'], 'Куда загрузить фотографии?', indicator='=>')
	commands[answer]()
	
	
def google_disk():
	os.system('cls||clear')
	gdrive = GoogleDriveClass(input('Ведите полный путь до папки с файлами:\n'))
	gdrive.create_and_upload()
	
	
def ya_disk():
	os.system('cls||clear')
	access_yadisk_token = input('Введите токен yandex:\n')
	yadisk = YaDisk(access_yadisk_token)
	yadisk.upload_photos()
	
	
if __name__ == '__main__':
	os.system('cls||clear')
	start_programm()

