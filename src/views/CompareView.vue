<script setup lang="ts">
import { ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useTeamStore } from '@/stores/teamStore'
import LineChart from '@/components/charts/LineChart.vue'
import BarChart from '@/components/charts/BarChart.vue'

const { t, locale } = useI18n()
const store = useTeamStore()

const selectedTeamIds = ref<string[]>([])

const availableTeams = computed(() => {
  return store.teams.slice().sort((a, b) => a.fifaRanking - b.fifaRanking)
})

const selectedTeams = computed(() => {
  return selectedTeamIds.value
    .map(id => store.getTeamById(id))
    .filter(Boolean)
})

const lineData = computed(() => {
  return selectedTeams.value.map((team, index) => ({
    name: team!.name,
    nameEn: team!.nameEn,
    ratings: team!.ratings,
    color: ['#3b82f6', '#ef4444', '#10b981', '#a855f7'][index % 4],
  }))
})

const barData = computed(() => {
  const dimensions = ['attack', 'defense', 'midfield', 'physical', 'tactics', 'experience']
  return {
    dimensions: dimensions.map(dim => t(`teamDetail.${dim}`)),
    series: selectedTeams.value.map((team, index) => {
      const t = team!
      return {
        name: locale.value === 'zh' ? t.name : t.nameEn,
        data: dimensions.map(dim => t.ratings[dim as keyof typeof t.ratings]),
        color: ['#3b82f6', '#ef4444', '#10b981', '#a855f7'][index % 4],
      }
    }),
  }
})

const addTeam = (teamId: string) => {
  if (selectedTeamIds.value.length < 4 && !selectedTeamIds.value.includes(teamId)) {
    selectedTeamIds.value.push(teamId)
  }
}

const removeTeam = (teamId: string) => {
  selectedTeamIds.value = selectedTeamIds.value.filter(id => id !== teamId)
}
</script>

<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <h1 class="text-3xl font-bold gradient-text mb-8">{{ t('compare.title') }}</h1>

    <!-- Team Selection -->
    <div class="glass-card p-6 mb-8">
      <h2 class="text-lg font-bold gradient-text mb-4">{{ t('compare.selectTeams') }} ({{ selectedTeamIds.length }}/4)</h2>

      <!-- Selected Teams -->
      <div v-if="selectedTeams.length > 0" class="flex flex-wrap gap-3 mb-6">
        <div
          v-for="team in selectedTeams"
          :key="team!.id"
          class="flex items-center gap-2 px-4 py-2 bg-amber-500/10 rounded-lg border border-amber-500/20"
        >
          <img :src="team!.flag" class="w-6 h-4 object-cover rounded" />
          <span class="font-medium text-text-primary">{{ locale === 'zh' ? team!.name : team!.nameEn }}</span>
          <button @click="removeTeam(team!.id)" class="text-red-400 hover:text-red-300 ml-1 text-lg leading-none">×</button>
        </div>
      </div>

      <!-- Team Selector -->
      <select
        @change="addTeam(($event.target as HTMLSelectElement).value); ($event.target as HTMLSelectElement).value = ''"
        class="w-full px-3 py-2 bg-white/5 border border-white/10 rounded-lg focus:outline-none focus:ring-2 focus:ring-amber-400 text-text-primary"
        :disabled="selectedTeamIds.length >= 4"
      >
        <option value="" class="bg-bg-card">{{ t('compare.addTeam') }}...</option>
        <option
          v-for="team in availableTeams"
          :key="team.id"
          :value="team.id"
          :disabled="selectedTeamIds.includes(team.id)"
          class="bg-bg-card"
        >
          {{ locale === 'zh' ? team.name : team.nameEn }} (FIFA #{{ team.fifaRanking }})
        </option>
      </select>
    </div>

    <!-- Comparison Charts -->
    <div v-if="selectedTeams.length >= 2" class="space-y-8">
      <!-- Line Chart -->
      <div class="glass-card p-6">
        <h2 class="text-lg font-bold gradient-text mb-4">{{ t('compare.lineCompare') }}</h2>
        <LineChart :data="lineData" :locale="locale" />
      </div>

      <!-- Bar Chart -->
      <div class="glass-card p-6">
        <h2 class="text-lg font-bold gradient-text mb-4">{{ t('compare.barCompare') }}</h2>
        <BarChart :data="barData" />
      </div>

      <!-- History Comparison Table -->
      <div class="glass-card p-6">
        <h2 class="text-lg font-bold gradient-text mb-4">{{ t('compare.historyCompare') }}</h2>
        <div class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead>
              <tr class="bg-white/5">
                <th class="px-4 py-3 text-left text-amber-400 font-medium">{{ t('teams.name') }}</th>
                <th class="px-4 py-3 text-left text-amber-400 font-medium">FIFA {{ t('teams.fifaRanking') }}</th>
                <th class="px-4 py-3 text-left text-amber-400 font-medium">{{ t('teamDetail.attack') }}</th>
                <th class="px-4 py-3 text-left text-amber-400 font-medium">{{ t('teamDetail.defense') }}</th>
                <th class="px-4 py-3 text-left text-amber-400 font-medium">{{ t('teamDetail.midfield') }}</th>
                <th class="px-4 py-3 text-left text-amber-400 font-medium">{{ t('teamDetail.physical') }}</th>
                <th class="px-4 py-3 text-left text-amber-400 font-medium">{{ t('teamDetail.tactics') }}</th>
                <th class="px-4 py-3 text-left text-amber-400 font-medium">{{ t('teamDetail.experience') }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="team in selectedTeams" :key="team!.id" class="border-b border-white/5 hover:bg-white/5 transition-colors">
                <td class="px-4 py-3">
                  <div class="flex items-center gap-2">
                    <img :src="team!.flag" class="w-6 h-4 object-cover rounded" />
                    <span class="font-medium text-text-primary">{{ locale === 'zh' ? team!.name : team!.nameEn }}</span>
                  </div>
                </td>
                <td class="px-4 py-3 text-text-secondary">#{{ team!.fifaRanking }}</td>
                <td class="px-4 py-3 text-text-secondary">{{ team!.ratings.attack }}</td>
                <td class="px-4 py-3 text-text-secondary">{{ team!.ratings.defense }}</td>
                <td class="px-4 py-3 text-text-secondary">{{ team!.ratings.midfield }}</td>
                <td class="px-4 py-3 text-text-secondary">{{ team!.ratings.physical }}</td>
                <td class="px-4 py-3 text-text-secondary">{{ team!.ratings.tactics }}</td>
                <td class="px-4 py-3 text-text-secondary">{{ team!.ratings.experience }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <div v-else class="glass-card p-12 text-center">
      <p class="text-text-muted">{{ t('compare.selectTeams') }} (至少2支)</p>
    </div>
  </div>
</template>
