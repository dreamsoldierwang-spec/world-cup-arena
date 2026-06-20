<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useTeamStore } from '@/stores/teamStore'
import PieChart from '@/components/charts/PieChart.vue'
import BarChart from '@/components/charts/BarChart.vue'

const { t, locale } = useI18n()
const store = useTeamStore()

const confederationNames: Record<string, string> = {
  UEFA: '欧洲',
  CONMEBOL: '南美洲',
  CONCACAF: '中北美',
  CAF: '非洲',
  AFC: '亚洲',
  OFC: '大洋洲',
}

function calcAvgRating(ratings: { attack: number; defense: number; midfield: number; physical: number; tactics: number; experience: number }) {
  return (ratings.attack + ratings.defense + ratings.midfield + ratings.physical + ratings.tactics + ratings.experience) / 6
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

const avgRatingsByConf = computed(() => {
  const confs: Record<string, { total: number; count: number }> = {}
  store.teams.forEach(t => {
    const avg = calcAvgRating(t.ratings)
    if (!confs[t.confederation]) confs[t.confederation] = { total: 0, count: 0 }
    confs[t.confederation].total += avg
    confs[t.confederation].count++
  })
  return Object.entries(confs).map(([name, { total, count }]) => ({
    name: locale.value === 'zh' ? confederationNames[name] || name : name,
    value: Math.round(total / count),
  }))
})

const topRatedTeams = computed(() => {
  return [...store.teams]
    .sort((a, b) => calcAvgRating(b.ratings) - calcAvgRating(a.ratings))
    .slice(0, 10)
    .map(t => ({
      name: locale.value === 'zh' ? t.name : t.nameEn,
      value: Math.round(calcAvgRating(t.ratings)),
    }))
})

const allPlayers = computed(() => {
  return store.teams.flatMap(t => t.players)
})

const ageDistribution = computed(() => {
  const buckets: Record<string, number> = { 'Under 20': 0, '20-25': 0, '25-30': 0, '30-35': 0, 'Over 35': 0 }
  allPlayers.value.forEach(p => {
    if (p.age < 20) buckets['Under 20']++
    else if (p.age < 25) buckets['20-25']++
    else if (p.age < 30) buckets['25-30']++
    else if (p.age < 35) buckets['30-35']++
    else buckets['Over 35']++
  })
  return Object.entries(buckets).map(([name, value]) => ({ name, value }))
})
</script>

<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <h1 class="text-3xl font-bold gradient-text mb-8">{{ t('statistics.title') }}</h1>

    <div class="grid md:grid-cols-2 gap-8">
      <!-- Continental Distribution -->
      <div class="glass-card p-6">
        <h2 class="text-lg font-bold gradient-text mb-4">{{ t('statistics.continentStats') }}</h2>
        <PieChart :data="continentData" />
      </div>

      <!-- Average Rating by Confederation -->
      <div class="glass-card p-6">
        <h2 class="text-lg font-bold gradient-text mb-4">{{ t('statistics.continentStats') }} - {{ t('teamDetail.ratings') }}</h2>
        <BarChart :data="avgRatingsByConf" horizontal />
      </div>

      <!-- Top Rated Teams -->
      <div class="glass-card p-6">
        <h2 class="text-lg font-bold gradient-text mb-4">{{ t('statistics.topRated') }}</h2>
        <BarChart :data="topRatedTeams" horizontal />
      </div>

      <!-- Age Distribution -->
      <div class="glass-card p-6">
        <h2 class="text-lg font-bold gradient-text mb-4">{{ t('statistics.ageDistribution') }}</h2>
        <PieChart :data="ageDistribution" />
      </div>
    </div>
  </div>
</template>
