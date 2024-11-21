
import os

import requests



class Cypet:


    def __init__(self, id : str, name, health, attack, img):
        self.id = id
        self.name = name
        self.health = health
        self.attack = attack
        self.element = ""
        self.img = img

    """def fetch_nft_metadata(id):  # получение данных NFT
            url = f"https://storage.googleapis.com/trace_cypets_metadata/{id}"
            headers = {"accept": "application/json"}
            response = requests.get(url, headers=headers)

            print(response.json())
            return response.json()

        def download_image_to_assets(image_url):
           
            # Загружает изображение по URL и сохраняет в папку assets.
            # 
            # :param image_url: Ссылка на изображение
            # :param filename: Имя файла для сохранения
            # :param assets_folder: Папка для сохранения (по умолчанию "assets")
            
            assets_folder = "assets"
            filename=image_url.split("/")[-1]+".png"
            # Проверяем, существует ли папка assets, если нет - создаём
            if not os.path.exists(assets_folder):
                os.makedirs(assets_folder)

            # Путь для сохранения изображения
            file_path = os.path.join(assets_folder, filename)
            # Проверяем, существует ли файл
            if os.path.exists(file_path):
                print(f"Файл уже существует: {file_path}")
                return filename

            # Загружаем изображение
            response = requests.get(image_url, stream=True)
            if response.status_code == 200:
                with open(file_path, "wb") as file:
                    for chunk in response.iter_content(1024):
                         file.write(chunk)
                print(f"Изображение успешно сохранено: {file_path}")
            else:
                raise Exception(f"Ошибка загрузки изображения: {response.status_code}")
            return filename

        nft_metadata = fetch_nft_metadata(id)

       
        # Инициализация нового Cypet.

        # :param name: Имя питомца (строка).
        # :param element: Стихия питомца (строка, например, "Огонь", "Вода").
        # :param health: Очки здоровья питомца (целое число).
        # :param attack: Сила атаки питомца (целое число).
        


        self.name = nft_metadata["attributes"][4]["value"]
        self.element = nft_metadata["attributes"][2]["value"]
        self.health = nft_metadata["attributes"][6]["value"]
        self.attack = nft_metadata["attributes"][5]["value"]

        self.img = download_image_to_assets(nft_metadata["image"])       """                        #f"https://storage.googleapis.com/trace_cypets_metadata/{id}_img.png"



    def take_damage(self, damage):
        """
        Уменьшает здоровье питомца при атаке.

        :param damage: Урон, который получает питомец (целое число).
        """
        self.health -= damage
        if self.health < 0:
            self.health = 0  # Здоровье не может быть меньше 0

    def is_alive(self):
        """
        Проверяет, жив ли питомец.

        :return: True, если здоровье больше 0, иначе False.
        """
        return self.health > 0

    def attack_target(self, target):
        """
        Атакует другого Cypet.

        :param target: Объект класса Cypet, который будет атакован.
        """
        print(f"{self.name}({self.health}HP) атакует {target.name}({target.health}HP), нанося {self.attack} урона!")
        target.take_damage(self.attack)

    def __str__(self):
        """
        Возвращает строковое представление питомца.
        """
        return f"{self.name} ({self.element}): {self.health} HP, {self.attack} ATK"



