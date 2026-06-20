<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useTeamStore } from '@/stores/teamStore'
import RadarChart from '@/components/charts/RadarChart.vue'

const route = useRoute()
const router = useRouter()
const { t, locale } = useI18n()
const store = useTeamStore()

const groupId = computed(() => route.params.groupId as string)
const teams = computed(() => store.getTeamsByGroup(groupId.value))

const radarData = computed(() => {
  return teams.value.map((team, index) => ({
    name: team.name,
    nameEn: team.nameEn,
    ratings: team.ratings,
    color: ['#fbbf24', '#f59e0b', '#ef4444', '#10b981'][index % 4],
  }))
})
</script>

<template>
  <div v-if="teams.length > 0" class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="flex items-center gap-4 mb-8">
      <button
        @click="router.push('/groups')"
        class="px-4 py-2 glass-card hover:bg-white/10 transition-colors text-text-primary"
      >
        ← {{ t('common.back') }}
      </button>
      <h1 class="text-3xl font-bold gradient-text">{{ t('groups.group') }} {{ groupId }}</h1>
    </div>

    <!-- Teams List -->
    <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
      <router-link
        v-for="team in teams"
        :key="team.id"
        :to="`/teams/${team.id}`"
        class="glass-card p-6 hover:border-amber-500/30 transition-all"
      >
        <div class="flex items-center gap-3 mb-3">
          <img :src="team.flag" :alt="team.name" class="w-12 h-8 object-cover rounded" />
          <div>
            <div class="font-bold text-text-primary">{{ locale === 'zh' ? team.name : team.nameEn }}</div>
            <div class="text-sm text-text-muted">FIFA #{{ team.fifaRanking }}</div>
          </div>
        </div>
        <div class="text-xs text-text-muted">
          {{ t('teamDetail.coach') }}: {{ locale === 'zh' ? team.coach.name : team.coach.nameEn }}
        </div>
      </router-link>
    </div>

    <!-- Radar Chart Comparison -->
    <div class="glass-card p-6">
      <h2 class="text-lg font-bold gradient-text mb-4">{{ t('groups.strengthCompare') }}</h2>
      <RadarChart :data="radarData" :locale="locale" />
    </div>
  </div>

  <div v-else class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 text-center">
    <p class="text-text-muted">{{ t('common.noData') }}</p>
    <button @click="router.push('/groups')" class="mt-4 px-4 py-2 bg-amber-500 text-slate-900 rounded-lg hover:bg-amber-400 font-medium transition-colors">
      {{ t('common.back') }}
    </button>
  </div>
</template>
