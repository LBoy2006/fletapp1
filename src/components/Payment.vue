<template>
  <div class="modal-overlay">
    <div class="payment-modal p-4 text-center space-y-4">
      <p>Вы не являетесь членом клуба 1chn.</p>
      <button
        @click="pay"
        class="bg-blue-600 text-white px-4 py-2 rounded"
      >
        Оплатить
      </button>
    </div>
  </div>
</template>
<script setup>
import { userData } from '../state'
import { API_BASE } from '../api'
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
</script>
