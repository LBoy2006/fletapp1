import flet as ft


def main(page: ft.Page):
    page.title = "Telegram Mini App"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START

    # Define each page content
    pages = {
        "home": ft.Text("Добро пожаловать на Главную"),
        "settings": ft.Text("Страница Настройки"),
        "leaderboard": ft.Text("Страница Лидерборд"),
        "task": ft.Text("Страница Задание"),
        "collections": ft.Text("Страница Мои коллекции"),
    }

    content = ft.Column([], expand=True, alignment=ft.MainAxisAlignment.CENTER)

    def show(name: str):
        content.controls.clear()
        content.controls.append(pages[name])
        page.update()

    # Bottom navigation buttons
    nav = ft.NavigationBar(
        destinations=[
            ft.NavigationDestination(icon=ft.icons.LEADERBOARD, label="Лидерборд"),
            ft.NavigationDestination(icon=ft.icons.TASK, label="Задание"),
            ft.NavigationDestination(icon=ft.icons.HOME, label="Главная"),
            ft.NavigationDestination(icon=ft.icons.COLLECTIONS, label="Коллекции"),
            ft.NavigationDestination(icon=ft.icons.SETTINGS, label="Настройки"),
        ],
        selected_index=2,
        on_change=lambda e: show([
            "leaderboard",
            "task",
            "home",
            "collections",
            "settings",
        ][e.control.selected_index]),
    )

    page.add(content, nav)
    show("home")


if __name__ == "__main__":
    ft.app(target=main, view=ft.WEB_BROWSER)
