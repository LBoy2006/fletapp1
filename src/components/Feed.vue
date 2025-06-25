<!--Feed.vue-->
<template>
  <div class="h-full p-0 flex flex-col space-y-1 p-2">
    <!-- 🔒 Фиксированная шапка -->
    <div class="sticky top-0 z-10 bg-[var(--page-bg-color)] px-0 py-4 pb-0 relative overflow-visible">
      <div class="relative flex items-center justify-between px-3">
        <!-- Слева -->
        <span class="text-lg font-bold text-white">Feed</span>

        <!-- Центрированный блок -->
        <div class="absolute left-1/2 transform -translate-x-1/2 flex flex-col items-center">
          <span class="text-2xl font-dela text-white">1chn</span>
          <span class="text-sm text-gray-400">[ван чан]</span>
        </div>
      </div>
    </div>

     <!-- 🛠️ Блок "в разработке" -->
    <div class="card-base flex flex-1 mx-2 items-center justify-center text-center">

      <div class="flex flex-col items-center space-y-4 max-w-xs">
        <!-- Эмодзи или картинка -->
        <div class="text-6xl">🚫</div> <!-- Можно заменить на <img> -->

        <!-- Тексты -->
        <div>
          <p class="text-lg font-semibold">Лента находится<br>в разработке</p>
          <p class="text-sm text-gray-400 mt-2">
            Скоро любой агент сможет публиковать свои находки, отчёты и результаты
          </p>
        </div>
      </div>
    </div>
  </div>

</template>




