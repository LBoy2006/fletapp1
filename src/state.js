import { reactive } from 'vue';

const initialUser = window.Telegram?.WebApp?.initDataUnsafe?.user || {};

export const userData = reactive({
  user: initialUser,
  score: Math.floor(Math.random() * 1000),
  rank: 0
});
