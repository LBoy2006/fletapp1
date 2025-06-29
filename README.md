# Telegram Mini App Demo

Этот репозиторий содержит пример мини-приложения для Telegram, созданный с использованием Vue 3 и Tailwind CSS. Приложение состоит из пяти экранов, между которыми можно переключаться через нижнюю панель навигации или свайпами.

## Страницы
1. **Лидерборд**
2. **Задание**
3. **Главная**
4. **Рюкзак**
5. **Настройки**

## Возможности
- Переключение тем (светлая и тёмная)
- Поддержка полноэкранного режима
- Локализация интерфейса (русский и английский)
- Корректное использование `contentSafeAreaInset` для отображения в Telegram
- Управление страницами свайпами на мобильных устройствах

## Запуск
Установите зависимости и запустите локальный сервер:
```bash
npm install
npm run dev
```
Готовую сборку можно получить командой `npm run build`. Проект автоматически деплоится на GitHub Pages через workflow.

## Скриншоты
Файлы изображений находятся в каталоге `assets/` и могут использоваться для демонстрации интерфейса.

## Backend API
Для получения данных профиля используется сервер на FastAPI. По умолчанию
используется база SQLite (`app.db`). Для подключения к другой базе можно
задать переменную `DATABASE_URL`.
Фронтенд получает адрес API из переменной `VITE_API_BASE` (константа `API_BASE` в коде).
По умолчанию используется `https://1chn.api.gptbrainbot.ru`.

Запуск API:
```bash
pip install -r requirements.txt
uvicorn backend.main:app --reload
```

## Миграции базы данных
Для управления схемой базы используется Alembic. Инициализация выполняется командой
```bash
alembic upgrade head
```
При изменении моделей создавайте новую миграцию
```bash
alembic revision --autogenerate -m "my change"
```
