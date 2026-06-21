<script setup lang="ts">
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'

const { t, locale } = useI18n()
const mobileMenuOpen = ref(false)

const toggleLocale = () => {
  locale.value = locale.value === 'zh' ? 'en' : 'zh'
}

const navItems = [
  { key: 'home', path: '/' },
  { key: 'teams', path: '/teams' },
  { key: 'compare', path: '/compare' },
  { key: 'groups', path: '/groups' },
  { key: 'ratings', path: '/ratings' },
  { key: 'statistics', path: '/statistics' },
]
</script>

<template>
  <header class="sticky top-0 z-50 glass border-b border-white/5">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-14">
        <!-- Logo -->
        <router-link to="/" class="flex items-center space-x-2.5">
          <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-primary to-primary-dark flex items-center justify-center">
            <span class="text-sm font-bold text-bg">⚽</span>
          </div>
          <div class="hidden sm:block">
            <div class="text-sm font-bold text-text-primary leading-tight">{{ t('home.title') }}</div>
            <div class="text-[10px] text-text-muted leading-tight">AI Model Prediction Arena</div>
          </div>
        </router-link>

        <!-- Desktop Nav -->
        <nav class="hidden md:flex items-center space-x-0.5">
          <router-link
            v-for="item in navItems"
            :key="item.key"
            :to="item.path"
            class="px-3 py-1.5 rounded-lg text-sm font-medium text-text-secondary hover:text-text-primary hover:bg-white/5 transition-all"
            :class="{ 'text-primary bg-primary/10': $route.path === item.path || ($route.path.startsWith(item.path) && item.path !== '/') }"
          >
            {{ t(`nav.${item.key}`) }}
          </router-link>
        </nav>

        <!-- Right Actions -->
        <div class="flex items-center space-x-2">
          <button
            @click="toggleLocale"
            class="px-2.5 py-1 rounded-lg text-xs font-medium text-text-secondary hover:text-text-primary hover:bg-white/5 transition-all border border-white/10"
          >
            {{ locale === 'zh' ? 'EN' : '中文' }}
          </button>

          <!-- Mobile menu button -->
          <button
            @click="mobileMenuOpen = !mobileMenuOpen"
            class="md:hidden p-1.5 rounded-lg hover:bg-white/5 text-text-secondary"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path v-if="!mobileMenuOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
              <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>

      <!-- Mobile Nav -->
      <div v-if="mobileMenuOpen" class="md:hidden pb-3 border-t border-white/5 mt-1">
        <router-link
          v-for="item in navItems"
          :key="item.key"
          :to="item.path"
          @click="mobileMenuOpen = false"
          class="block px-3 py-2 rounded-lg text-sm text-text-secondary hover:text-text-primary hover:bg-white/5 transition-all mt-1"
          :class="{ 'text-primary bg-primary/10': $route.path === item.path }"
        >
          {{ t(`nav.${item.key}`) }}
        </router-link>
      </div>
    </div>
  </header>
</template>
