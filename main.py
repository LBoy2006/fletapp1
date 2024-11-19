import flet as ft
import asyncio
import random


animation_in_progress = False


def main(page: ft.Page):
    page.title = "Cypets Battle"
    page.window.width = 420  # Ширина окна
    page.window.height = 730  # Высота окна
    page.window.resizable = False
    page.window.maximizable = False
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.bgcolor = ft.colors.GREEN_ACCENT

    main_st = ft.Stack(
        width=100,
        height=150,
        controls=[
            ft.Container(
                width=80,
                height=120,
                border_radius=10,
                bgcolor=ft.colors.GREEN,
                top=5,
                left=5,
            ),
            # Левый верхний круглый контейнер (серый)
            ft.Container(
                content=ft.Text(
                    value="20",
                    size=10,
                    color=ft.colors.WHITE,
                    text_align=ft.alignment.center,
                ),
                alignment=ft.alignment.center,
                width=20,
                height=20,
                border=ft.border.all(2, ft.colors.WHITE),
                bgcolor=ft.colors.GREY,
                border_radius=10,  # Делает контейнер круглым
                top=0,  # Отступ от верхнего края
                left=0,  # Отступ от левого края
            ),
            # Правый верхний круглый контейнер (красный)
            ft.Container(
                content=ft.Text(
                    value="20",
                    size=10,
                    color=ft.colors.WHITE,
                    text_align=ft.alignment.center,
                ),
                alignment=ft.alignment.center,
                border=ft.border.all(2, ft.colors.WHITE),
                width=20,
                height=20,
                bgcolor=ft.colors.RED,
                border_radius=10,  # Делает контейнер круглым
                top=0,  # Отступ от верхнего края
                right=0,  # Отступ от правого края
            ),
        ],
        alignment=ft.alignment.center,
    )

    # Контейнеры игрока
    container_l = ft.Container(
        content=main_st,
        margin=0,
        padding=0,
        alignment=ft.alignment.center,
        bgcolor=ft.colors.WHITE,
        width=90,
        height=130,
        border_radius=10,
        ink=True,
        top=450,
        left=60,
        animate_position=ft.animation.Animation(300, ft.AnimationCurve.EASE_IN_BACK),
        animate_rotation=ft.animation.Animation(300),
    )

    container_f = ft.Container(
        content=main_st,
        margin=0,
        padding=0,
        alignment=ft.alignment.center,
        bgcolor=ft.colors.RED,  # Фронтальный игрок выделен красным
        width=90,
        height=130,
        border_radius=10,
        ink=True,
        top=310,
        left=110,
        animate_position=ft.animation.Animation(300, ft.AnimationCurve.EASE_IN_BACK),
        animate_rotation=ft.animation.Animation(300),
    )

    container_r = ft.Container(
        content=main_st,
        margin=0,
        padding=0,
        alignment=ft.alignment.center,
        bgcolor=ft.colors.WHITE,
        width=90,
        height=130,
        border_radius=10,
        ink=True,
        top=450,
        left=160,
        animate_position=ft.animation.Animation(300, ft.AnimationCurve.EASE_IN_BACK),
        animate_rotation=ft.animation.Animation(300),
    )

    # Список контейнеров игрока
    player_containers = [
        container_f,
        container_l,
        container_r,
    ]  # Фронтальный игрок первым
    current_player_index = 0  # Индекс текущего выбранного игрока

    # Контейнеры врагов
    enemy1 = ft.Container(
        bgcolor=ft.colors.WHITE,
        content=main_st,
        width=90,
        height=130,
        border_radius=10,
        ink=True,
        top=0,
        left=160,
        animate_position=ft.animation.Animation(300, ft.AnimationCurve.EASE_IN_BACK),
        animate_rotation=ft.animation.Animation(300),
    )
    enemy2 = ft.Container(
        bgcolor=ft.colors.WHITE,
        content=main_st,
        width=90,
        height=130,
        border_radius=10,
        ink=True,
        top=0,
        left=60,
        animate_position=ft.animation.Animation(300, ft.AnimationCurve.EASE_IN_BACK),
        animate_rotation=ft.animation.Animation(300),
    )
    enemy3 = ft.Container(
        bgcolor=ft.colors.WHITE,
        content=main_st,
        width=90,
        height=130,
        border_radius=10,
        ink=True,
        top=140,
        left=110,
        animate_position=ft.animation.Animation(300, ft.AnimationCurve.EASE_IN_BACK),
        animate_rotation=ft.animation.Animation(300),
    )

    enemies = [enemy1, enemy2, enemy3]  # Список врагов
    current_enemy_index = 0  # Индекс текущего атакующего врага

    kick = ft.Stack(
        [
            ft.Image(src="assets/kick.png", width=50),
            ft.Text(value="10", size=10, color=ft.colors.RED),
        ],
        alignment=ft.alignment.center,
        opacity=0,  # Начинаем с полной прозрачности
        animate_opacity=100,
    )

    def move_on_top(control):
        """Moves draggable card to the top of the stack"""
        st1.controls.append(kick)
        st1.controls.remove(control)
        st1.controls.append(control)
        page.update()

    async def animate_attack(attacker, target):
        move_on_top(attacker)
        """Анимация атаки: перемещение атакующего к цели и возврат обратно с анимацией эффекта."""
        original_top = attacker.top
        original_left = attacker.left

        # Размещаем kick на позиции цели
        kick.top = target.top + (target.height / 2) - 25  # Центрируем относительно цели
        kick.left = target.left + (target.width / 2) - 25

        # Добавляем эффект удара на страницу

        # Перемещаем атакующего к цели
        attacker.rotate = -0.3
        attacker.bgcolor = ft.colors.RED
        attacker.top = target.top
        attacker.left = target.left
        page.update()

        await asyncio.sleep(0.4)

        # Удаляем эффект удара с экрана

        # Возвращаем атакующего на исходную позицию
        attacker.top = original_top
        attacker.left = original_left
        attacker.rotate = 0
        attacker.bgcolor = ft.colors.WHITE
        page.update()
        kick.opacity = 1
        page.update()
        # Анимация исчезновения эффекта удара
        kick.opacity = 0

        st1.controls.remove(kick)
        await asyncio.sleep(0.6)
        page.update()

    def select_next_player():
        """Выделить следующий контейнер игрока по очереди."""
        nonlocal current_player_index

        # Сбрасываем выделение текущего контейнера
        player_containers[current_player_index].bgcolor = ft.colors.WHITE

        # Переходим к следующему контейнеру
        current_player_index = (current_player_index + 1) % len(player_containers)
        player_containers[current_player_index].bgcolor = ft.colors.RED

        page.update()

    async def enemy_attack():
        """Ответная атака врага по случайному игроку."""
        nonlocal current_enemy_index

        # Выбираем случайного игрока
        target_player = random.choice(player_containers)

        # Атакующий враг
        attacking_enemy = enemies[current_enemy_index]

        # Выполняем атаку
        attacking_enemy.bgcolor = ft.colors.RED
        target_player.bgcolor = ft.colors.PURPLE
        page.update()

        await animate_attack(attacking_enemy, target_player)

        # Сбрасываем цвет врага
        attacking_enemy.bgcolor = ft.colors.WHITE
        target_player.bgcolor = ft.colors.WHITE

        page.update()

        # Переходим к следующему врагу
        current_enemy_index = (current_enemy_index + 1) % len(enemies)

    async def attack_enemy(e):
        global animation_in_progress
        if animation_in_progress:
            return  # Если анимация уже идет, ничего не делаем

        # Блокируем взаимодействие
        animation_in_progress = True
        page.update()
        """Обработка атаки выбранным контейнером на врага."""
        target = e.control  # Контейнер, на который кликнули
        target.bgcolor = ft.colors.PURPLE  # Меняем цвет цели
        page.update()

        selected_container = player_containers[
            current_player_index
        ]  # Текущий выбранный контейнер
        await animate_attack(selected_container, target)

        # Сбрасываем цвет цели
        target.bgcolor = ft.colors.WHITE
        page.update()
        # Ответная атака врага
        await asyncio.sleep(1)
        await enemy_attack()

        # Переходим к следующему игроку
        await asyncio.sleep(1)
        select_next_player()
        # Разрешаем взаимодействие после завершения анимации
        animation_in_progress = False
        page.update()

    # Привязываем клик на врагов
    for enemy in enemies:
        enemy.on_click = attack_enemy

    # Игровое поле
    st1 = ft.Stack(
        controls=[
            container_l,
            container_f,
            container_r,
            enemy1,
            enemy2,
            enemy3,
        ],
        width=300,
        height=600,
    )

    # Добавляем элементы на страницу
    page.add(st1)


ft.app(
    target=main, #view=ft.AppView.WEB_BROWSER
)
