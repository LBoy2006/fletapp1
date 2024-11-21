

import requests

import time

"""def fetch_nft_metadata( token_id):  # получение данных NFT
    url = f"https://polygon-mainnet.g.alchemy.com/v2/{alchemy_api}/getNFTMetadata?contractAddress=0xebeafdfd15bd0bfaedac3eb8e70b4836df6774b5&tokenId={token_id}&refreshCache=false"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)

    return response.json()
nft_metadata = fetch_nft_metadata("201173")
nftelement = nft_metadata["metadata"]["attributes"][2]["value"]
nftname = nft_metadata["metadata"]["attributes"][4]["value"]
cypet_attack = nft_metadata["metadata"]["attributes"][5]["value"]
cypet_health = nft_metadata["metadata"]["attributes"][6]["value"]

print(nftelement, nftname, cypet_health , cypet_attack)"""

class Cypet:


    def __init__(self, id : str):
        self.id = id

        def fetch_nft_metadata(id):  # получение данных NFT
            url = f"https://storage.googleapis.com/trace_cypets_metadata/{id}"
            headers = {"accept": "application/json"}
            response = requests.get(url, headers=headers)

            print(response.json())
            return response.json()


        nft_metadata = fetch_nft_metadata(id)

        """
        Инициализация нового Cypet.

        :param name: Имя питомца (строка).
        :param element: Стихия питомца (строка, например, "Огонь", "Вода").
        :param health: Очки здоровья питомца (целое число).
        :param attack: Сила атаки питомца (целое число).
        """


        self.name = nft_metadata["attributes"][4]["value"]
        self.element = nft_metadata["attributes"][2]["value"]
        self.health = nft_metadata["attributes"][6]["value"]
        self.attack = nft_metadata["attributes"][5]["value"]

        self.img = nft_metadata["image"]                                #f"https://storage.googleapis.com/trace_cypets_metadata/{id}_img.png"



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

c = Cypet("201174")

print(c)


