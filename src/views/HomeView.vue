<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'
import { useTeamStore } from '@/stores/teamStore'
import PieChart from '@/components/charts/PieChart.vue'
import BarChart from '@/components/charts/BarChart.vue'

const { t, locale } = useI18n()
const router = useRouter()
const store = useTeamStore()

const topTeams = computed(() => store.getTopTeams(8))

const confederationNames: Record<string, string> = {
  UEFA: '欧洲',
  CONMEBOL: '南美洲',
  CONCACAF: '中北美',
  CAF: '非洲',
  AFC: '亚洲',
  OFC: '大洋洲',
}

const continentData = computed(() => {
  const counts: Record<string, number> = {}
  store.teams.forEach(t => {
    counts[t.confederation] = (counts[t.confederation] || 0) + 1
  })
  return Object.entries(counts).map(([name, value]) => ({
    name: locale.value === 'zh' ? confederationNames[name] || name : name,
    value,
  }))
})

const rankingData = computed(() => {
  return [...store.teams]
    .sort((a, b) => a.fifaRanking - b.fifaRanking)
    .slice(0, 10)
    .map(t => ({
      name: locale.value === 'zh' ? t.name : t.nameEn,
      value: t.fifaRanking,
    }))
})
</script>

<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- Hero Section -->
    <div class="glass-card p-8 mb-8 relative overflow-hidden">
      <!-- Background decoration -->
      <div class="absolute top-0 right-0 w-64 h-64 bg-primary/5 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2"></div>
      
      <div class="relative z-10">
        <div class="tag-pill bg-primary/10 text-primary mb-4">
          <span class="w-1.5 h-1.5 rounded-full bg-primary mr-2"></span>
          AI Model Prediction Arena - Not betting advice
        </div>
        
        <h1 class="text-4xl md:text-5xl font-black mb-3">
          <span class="gradient-text">WORLD CUP ARENA</span>
        </h1>
        <p class="text-lg text-text-secondary mb-2 font-medium">
          {{ t('home.subtitle') }}
        </p>
        <p class="text-sm text-text-muted mb-8 max-w-2xl">
          Comprehensive analysis of all 48 teams in the 2026 FIFA World Cup. Explore team strengths, player rosters, historical performance, and multi-dimensional power ratings.
        </p>

        <!-- Action Buttons -->
        <div class="flex flex-wrap gap-3">
          <router-link
            to="/teams"
            class="px-5 py-2.5 bg-primary text-bg font-semibold rounded-lg hover:bg-primary-light transition-colors"
          >
            {{ t('home.viewAll') }}
          </router-link>
          <router-link
            to="/compare"
            class="px-5 py-2.5 bg-white/5 text-text-primary font-medium rounded-lg border border-white/10 hover:bg-white/10 transition-colors"
          >
            {{ t('nav.compare') }}
          </router-link>
        </div>
      </div>

      <!-- Stats Cards -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mt-8 relative z-10">
        <div class="glass-card p-4 text-center">
          <div class="text-2xl font-black text-primary">48</div>
          <div class="text-xs text-text-muted mt-1">{{ t('home.totalTeams') }}</div>
        </div>
        <div class="glass-card p-4 text-center">
          <div class="text-2xl font-black text-primary">104</div>
          <div class="text-xs text-text-muted mt-1">{{ t('home.totalMatches') }}</div>
        </div>
        <div class="glass-card p-4 text-center">
          <div class="text-2xl font-black text-primary">3</div>
          <div class="text-xs text-text-muted mt-1">{{ t('home.hostCountries') }}</div>
        </div>
        <div class="glass-card p-4 text-center">
          <div class="text-2xl font-black text-primary">39</div>
          <div class="text-xs text-text-muted mt-1">{{ t('home.duration') }}</div>
        </div>
      </div>
    </div>

    <!-- Charts Section -->
    <div class="grid md:grid-cols-2 gap-6 mb-8">
      <div class="glass-card p-6">
        <h2 class="section-title">{{ t('home.continentDistribution') }}</h2>
        <p class="section-subtitle">Distribution of 48 teams across 6 confederations</p>
        <PieChart :data="continentData" />
      </div>
      <div class="glass-card p-6">
        <h2 class="section-title">{{ t('home.rankingDistribution') }}</h2>
        <p class="section-subtitle">Top 10 teams by FIFA ranking</p>
        <BarChart :data="rankingData" horizontal />
      </div>
    </div>

    <!-- Top Teams -->
    <div class="glass-card p-6">
      <div class="flex items-center justify-between mb-6">
        <div>
          <h2 class="section-title mb-0">{{ t('home.topTeams') }}</h2>
          <p class="section-subtitle mb-0 mt-1">Highest ranked teams in the tournament</p>
        </div>
        <router-link
          to="/teams"
          class="text-primary hover:text-primary-light text-sm font-medium"
        >
          {{ t('home.viewAll') }} →
        </router-link>
      </div>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
        <router-link
          v-for="team in topTeams"
          :key="team.id"
          :to="`/teams/${team.id}`"
          class="flex items-center space-x-3 p-3 rounded-lg bg-white/5 border border-white/5 hover:border-primary/30 hover:bg-white/10 transition-all"
        >
          <img :src="team.flag" :alt="team.name" class="w-8 h-5 object-cover rounded" />
          <div class="min-w-0">
            <div class="font-medium text-text-primary text-sm truncate">{{ locale === 'zh' ? team.name : team.nameEn }}</div>
            <div class="text-xs text-text-muted">FIFA #{{ team.fifaRanking }}</div>
          </div>
        </router-link>
      </div>
    </div>
  </div>
</template>
