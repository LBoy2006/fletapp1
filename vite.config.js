import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
  plugins: [vue()],
  base: './',
  server: {
    allowedHosts: [
      '1chn.gptbrainbot.ru'
    ],
    // если у тебя уже есть другие опции — просто добавь allowedHosts в server
  },
});
