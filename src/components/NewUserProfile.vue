<template>
  <div

        @touchstart="handleTouchStart"
  @touchmove="handleTouchMove"
  @touchend="handleTouchEnd"
      class="flex z-10">

    <!-- Canvas for falling matrix symbols -->
    <canvas class="fixed  w-full h-[calc(100%-70px)] z-10 mx-20 " id="matrix"></canvas>

    <!-- Overlay Content -->
    <div class="modal-overlay h-[calc(100%-70px)] flex flex-col gap-10 backdrop-blur-sm justify-around z-10">
      <div class=" flex flex-row justify-start items-center gap-4">
        <img src='../img/error.webp' class="w-16 h-16  rounded-full object-cover " />
        <div class="flex-row flex-1 flex justify-between gap-3">
          <div class="flex-col justify-between text-start">
            <div class="text-sm text-[#DFDFDF]">номер агента:</div>
            <div class="text-sm text-[#DFDFDF]">дней в клубе:</div>
            <div class="text-sm text-[#DFDFDF]">локация:</div>
            <div class="text-sm text-[#DFDFDF]">статус:</div>
          </div>
           <div class="flex-col justify-between text-end">
            <div class="notfound-glow text-pink-300 text-sm">not found</div>
            <div class="notfound-glow text-pink-300 text-sm">not found</div>
            <div class="notfound-glow text-pink-300 text-sm">not found</div>
            <div class="notfound-glow text-pink-300 text-sm">not found</div>
           </div>
        </div>
      </div>
      <div class="text-center">
        <p class="text-m flicker">
         Добро пожаловать в сеть [1CHN] <br /> Для входа в систему требуется<br /> активация профиля<br /><br />💳 Разовый взнос — 1990₽  <br />+ 30 дней доступа включены
        </p>      </div>

      <div class="text-center">

        <button @click="openPay" class="glitch-scale text-green-500 hover:underline text-md">
          [ ПОЛУЧИТЬ ДОСТУП ]
        </button>
        <PayModal v-if="payVisible" @close="payVisible=false" />
      </div>
      <div class="text-center">

        <button @click="openSup" class="text-white pt-10 hover:underline text-sm">
          [ тех-поддержка ]
        </button>
        <PayModal v-if="payVisible" @close="payVisible=false" />
      </div>

    </div>
  </div>
</template>

<script setup>

import PayModal from './PayModal.vue'
import { onMounted, ref } from 'vue';
import { userData } from '../state';
const emit = defineEmits(['paid', 'swipe']); // <--- Добавил swipe для навигации

const payVisible = ref(false)
const gesturePoints = ref([]);
let gestureActive = false;

let startX = null;
let startY = null;

// Открыть Pay-модалку
function openPay() {
  payVisible.value = true;
}

// Универсальный обработчик для свайпа и рисования "Z"
function handleTouchStart(e) {
  if (e.touches.length !== 1) return;
  startX = e.touches[0].clientX;
  startY = e.touches[0].clientY;

  gestureActive = true;
  gesturePoints.value = [{x: startX, y: startY}];
}

function handleTouchMove(e) {
  if (!gestureActive) return;
  const touch = e.touches[0];
  gesturePoints.value.push({x: touch.clientX, y: touch.clientY});
}

function handleTouchEnd(e) {
  // --- Свайп навигация ---
  if (startX !== null && startY !== null && e.changedTouches) {
    const dx = e.changedTouches[0].clientX - startX;
    const dy = e.changedTouches[0].clientY - startY;
    if (Math.abs(dx) > 40 && Math.abs(dx) > Math.abs(dy)) {
      emit('swipe', dx > 0 ? 'right' : 'left');
      // свайп обработан, не обязательно проверять рисунок если не нужно
      // return;
    }
    startX = null;
    startY = null;
  }

  // --- Пасхалка: рисунок "Z" справа налево ---
  gestureActive = false;
  const points = gesturePoints.value;
  if (points.length > 5) {
    const n = points.length;
    const p1 = points.slice(0, Math.floor(n / 3));
    const p2 = points.slice(Math.floor(n / 3), Math.floor(2 * n / 3));
    const p3 = points.slice(Math.floor(2 * n / 3));

    const dx1 = p1[p1.length - 1].x - p1[0].x; // первая часть — влево
    const dy2 = p2[p2.length - 1].y - p2[0].y; // вниз
    const dx2 = p2[p2.length - 1].x - p2[0].x; // вправо (диагональ)
    const dx3 = p3[p3.length - 1].x - p3[0].x; // снова влево

    if (
      dx1 < -30 &&       // влево
      dy2 > 20 && dx2 > 20 && // вниз вправо
      dx3 < -30          // снова влево
    ) {
      userData.user.is_member = true;
      emit('paid');
      alert('Поздравляем! Вы стали участником клуба! 🎉');
    }
  }
  gesturePoints.value = [];
}

const SUPPORT_LINK = 'https://t.me/your_support_channel';

function openSup() {
  window.open(SUPPORT_LINK, '_blank');
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

.notfound-glow {
  text-shadow:
    0 0 8px #ff0033,
    0 0 12px #ff0033,
    0 0 24px #ff0033,
    0 0 32px #ff0033;
}

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
