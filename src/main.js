import { createApp, ref, onMounted } from 'vue';
import App from './App.vue';
import JoinClub from './components/JoinClub.vue';
import './style.css';
import { userData } from './state';

const Root = {
  components: { App, JoinClub },
  setup() {
    const loading = ref(true);
    const member = ref(false);

    onMounted(async () => {
      // Authentication disabled for now. Always enable member mode.
      // Uncomment the code below to restore Telegram WebApp authentication.
      /*
      if (window.Telegram?.WebApp) {
        try {
          const resp = await fetch('http://localhost:8000/auth/telegram', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ init_data: Telegram.WebApp.initData })
          });
          if (resp.ok) {
            const data = await resp.json();
            member.value = data.is_member;
            if (data.user) {
              userData.user = data.user;
            }
          }
        } catch (e) {
          console.error(e);
        }
      }
      */
      member.value = true;
      loading.value = false;
    });

    return { loading, member };
  },
  template: `
    <div v-if="loading">Loading...</div>
    <App v-if="!loading && member" />
    <JoinClub v-else-if="!loading" />
  `
};

createApp(Root).mount('#app');
