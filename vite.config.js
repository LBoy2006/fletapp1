import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
  plugins: [vue()],
  base: './',
  server: {
    allowedHosts: [
      'lboy2006.github.io/fletapp1'
    ],
    // если у тебя уже есть другие опции — просто добавь allowedHosts в server
  },
});
