<template>
  <div
        @touchstart="handleTouchStart"
  @touchmove="handleTouchMove"
  @touchend="handleTouchEnd"
      class="flex items-center justify-center text-center">

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
        <button @click="openPay" class="glitch-scale text-green-500 hover:underline text-md">
          [ ПОЛУЧИТЬ ДОСТУП ]
        </button>
        <PayModal v-if="payVisible" @close="payVisible=false" />
      </div>
    </div>
  </div>
</template>

<script setup>

import PayModal from './PayModal.vue'

import { onMounted, ref } from 'vue';
import { userData } from '../state'; // путь поправь, если не тот
const emit = defineEmits(['paid']);
const payVisible = ref(false)
const gesturePoints = ref([]);
let gestureActive = false;

function handleTouchStart(e) {
  gestureActive = true;
  gesturePoints.value = [];
  const touch = e.touches[0];
  gesturePoints.value.push({x: touch.clientX, y: touch.clientY});
}

function handleTouchMove(e) {
  if (!gestureActive) return;
  const touch = e.touches[0];
  gesturePoints.value.push({x: touch.clientX, y: touch.clientY});
}

function handleTouchEnd() {
  gestureActive = false;
  // 1. Простая фильтрация: три участка движения
  if (gesturePoints.value.length < 5) return; // мало точек

  // Нарежем путь на три части (начало, середина, конец)
  const n = gesturePoints.value.length;
  const p1 = gesturePoints.value.slice(0, Math.floor(n/3));
  const p2 = gesturePoints.value.slice(Math.floor(n/3), Math.floor(2*n/3));
  const p3 = gesturePoints.value.slice(Math.floor(2*n/3));

  // 2. Проверим направления
  const dx1 = p1[p1.length-1].x - p1[0].x; // движение влево
  const dy2 = p2[p2.length-1].y - p2[0].y; // вниз
  const dx2 = p2[p2.length-1].x - p2[0].x; // вправо (диагональ)
  const dx3 = p3[p3.length-1].x - p3[0].x; // опять влево

  if (
    dx1 < -30 && // первая часть — влево
    dy2 > 20 && dx2 > 20 && // вторая часть — вниз вправо
    dx3 < -30 // третья часть — снова влево
  ) {
    userData.user.is_member = true;
    emit('paid');
    alert('Поздравляем! Вы “нарисовали Z справа налево” и стали участником клуба! 🎉');
  }
}



function openPay() {
  payVisible.value = true
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
