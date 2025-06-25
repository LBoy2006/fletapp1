<template>
  <div class="flex items-center justify-center text-center">

    <!-- Canvas for falling matrix symbols -->
    <canvas class="fixed inset-0 w-full h-full z-10" id="matrix"></canvas>

    <!-- Overlay Content -->
    <div class="modal-overlay fixed inset-0 backdrop-blur-sm flex items-center justify-center z-10">
      <div class="space-y-6  text-center pb-20">
        <div class="glitch text-md pb-5" data-text="Запись не найдена">Запись не найдена</div>
        <div class="text-sm text-orange-300">Это раздел профиля</div>
        <p class="text-m pb-5 flicker">
          Доступ к системе закрыт<br />
          Активируйте профиль, чтобы <br />
          начать операцию
        </p>
        <button @click="pay" class="glitch-scale text-green-500 hover:underline text-md">
          [ ПОЛУЧИТЬ ДОСТУП ]
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { userData } from '../state'
import { API_BASE } from '../api'
import { onMounted } from 'vue'

const emit = defineEmits(['paid'])

async function pay() {
  if (!userData.user.id) return
  try {
    await fetch(`${API_BASE}/users/${userData.user.id}/pay`, { method: 'POST' })
    userData.user.is_member = true
    emit('paid')
  } catch (e) {
    console.error(e)
  }
}

onMounted(() => {
  const canvas = document.getElementById('matrix')
  if (!canvas) return
  const ctx = canvas.getContext('2d')

  canvas.width = window.innerWidth
  canvas.height = window.innerHeight

  const letters = "アカサタナハマヤラワ0123456789"
  const fontSize = 36
  const columns = Math.floor(canvas.width / fontSize)
  const drops = Array.from({ length: columns }).fill(1)

  function draw() {
    ctx.fillStyle = "rgba(0, 0, 0, 0.05)"
    ctx.fillRect(0, 0, canvas.width, canvas.height)

    ctx.fillStyle = "#ff8800"
    ctx.font = `${fontSize}px monospace`

    for (let i = 0; i < drops.length; i++) {
      const text = letters.charAt(Math.floor(Math.random() * letters.length))
      ctx.fillText(text, i * fontSize, drops[i] * fontSize)

      if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
        drops[i] = 0
      }

      drops[i]++
    }
  }

  setInterval(draw, 33)
})
</script>

<style scoped>
.glitch {
  color: white;
  font-family: monospace;
  font-size: 1.5rem;
  position: relative;
  text-align: center;
}
.glitch::before,
.glitch::after {
  content: attr(data-text);
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  text-align: center;
  white-space: nowrap;
  pointer-events: none;
}
.glitch::before {
  animation: glitchTop 1s infinite linear;
  color: #0ff;
  z-index: -3;
}
.glitch::after {
  animation: glitchBottom 1s infinite linear;
  color: #f0f;
  z-index: -5;
}
@keyframes glitchTop {
  0% { top: -2px; left: -2px; }
  20% { top: 0; left: 2px; }
  40% { top: -2px; left: -1px; }
  60% { top: 0; left: 1px; }
  100% { top: -2px; left: 2px; }
}
@keyframes glitchBottom {
  0% { top: 2px; left: 2px; }
  20% { top: 0; left: -2px; }
  40% { top: 2px; left: 1px; }
  60% { top: 0; left: -1px; }
  100% { top: 2px; left: -2px; }
}

.flicker {
  animation: flickerAnim 2s infinite;
}

@keyframes flickerAnim {
  0%, 19%, 21%, 23%, 25%, 54%, 56%, 100% {
    opacity: 1;
    text-shadow: 0 0 2px #0f0, 0 0 6px #ff2600;
  }
  20%, 24%, 55% {
    opacity: 0.3;
    text-shadow: none;
  }
  22% {
    opacity: 0.6;
    text-shadow: 0 0 1px #ff5900;
  }
}

.glitch-scale {
  animation: glitchFrame 1.8s infinite steps(2, end);
}

@keyframes glitchFrame {
  0%   { transform: scale(1) translate(0, 0); opacity: 1; }
  10%  { transform: scale(1.05) translate(-2px, 1px); opacity: 0.8; }
  20%  { transform: scale(0.98) translate(3px, -1px); opacity: 1; }
  30%  { transform: scale(1.02) translate(-1px, 2px); opacity: 0.9; }
  50%  { transform: scale(1) translate(0, 0); opacity: 1; }
  100% { transform: scale(1) translate(0, 0); opacity: 1; }
}



</style>
