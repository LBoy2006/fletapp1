<template>
  <div class="modal-overlay fixed inset-0 bg-black/30 backdrop-blur-sm flex items-center justify-center">
    <div class="payment-modal p-4 bg-white rounded-lg text-center space-y-4 shadow-lg">
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

<!--<script setup>-->
<!--function pay() {-->
<!--  console.log('Оплата начата');-->
<!--}-->
<!--</script>-->

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
