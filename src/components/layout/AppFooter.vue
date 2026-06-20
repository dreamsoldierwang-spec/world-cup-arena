<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
</script>

<template>
  <footer class="glass border-t border-white/5 py-8 mt-auto">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex flex-col md:flex-row items-center justify-between">
        <div class="flex items-center space-x-2 mb-4 md:mb-0">
          <span class="text-2xl">⚽</span>
          <span class="font-bold gradient-text">{{ t('home.title') }}</span>
        </div>
        <div class="text-sm text-text-muted text-center md:text-right">
          <p>2026 FIFA World Cup Arena - Data for reference only</p>
          <p class="mt-1">Data updated: 2026-06-20</p>
        </div>
      </div>
    </div>
  </footer>
</template>
