class Cypet:
    def __init__(self, name : str, element: str, health : int, attack: int):
        """
        Инициализация нового Cypet.

        :param name: Имя питомца (строка).
        :param element: Стихия питомца (строка, например, "Огонь", "Вода").
        :param health: Очки здоровья питомца (целое число).
        :param attack: Сила атаки питомца (целое число).
        """
        self.name = name
        self.element = element
        self.health = health
        self.attack = attack

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
