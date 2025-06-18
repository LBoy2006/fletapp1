import { reactive } from 'vue';

export const userData = reactive({
  user: {},
  score: Math.floor(Math.random() * 1000),
  rank: 0
});
