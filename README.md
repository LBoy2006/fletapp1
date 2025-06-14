# Telegram Mini App Demo

This project contains a simple example of a Telegram mini‑app. It showcases five
pages that can be switched using a bottom navigation bar:

1. “Лидерборд”
2. “Задание”
3. “Главная”
4. “Рюкзак”
5. “Настройки”

The layout uses [Tailwind CSS](https://tailwindcss.com/) and integrates the
Telegram Web Apps script. The example respects `contentSafeAreaInset` so UI
elements never overlap Telegram controls. Open `index.html` in a browser (or
within Telegram as a mini‑app) to try it out. На мобильных устройствах страницы
можно переключать, свайпая вправо или влево. Перелистывание сопровождается
плавной анимацией.


## External assets

The main stylesheet is now `style.css` and the main script is `script.js`. To serve them via a CDN, host these files on a service such as jsDelivr or GitHub Pages and update the paths in `index.html` accordingly. This demo loads both files from GitHub via jsDelivr using `https://cdn.jsdelivr.net/gh/LBoy2006/fletapp1@main/<file>`. Replace `@main` with a specific tag to pin to a release if desired.
