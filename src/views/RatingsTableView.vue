<script setup lang="ts">
import { computed, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useTeamStore } from '@/stores/teamStore'

const { t, locale } = useI18n()
const store = useTeamStore()

const dimKeys = ['attack', 'defense', 'midfield', 'physical', 'tactics', 'experience'] as const

const dimLabels = computed(() => ({
  attack: t('teamDetail.attack'),
  defense: t('teamDetail.defense'),
  midfield: t('teamDetail.midfield'),
  physical: t('teamDetail.physical'),
  tactics: t('teamDetail.tactics'),
  experience: t('teamDetail.experience'),
}))

const getAvg = (team: typeof store.teams extends (infer U)[] ? U : never) => {
  const vals = dimKeys.map(k => team.ratings[k])
  return Math.round(vals.reduce((a, b) => a + b, 0) / vals.length)
}

// For each dimension, get top 5 teams sorted by team name
const top5PerDim = computed(() => {
  const result: Record<string, typeof store.teams[number][]> = {}
  for (const key of dimKeys) {
    const sorted = [...store.teams].sort((a, b) => b.ratings[key] - a.ratings[key]).slice(0, 5)
    // Sort these top 5 by team name
    sorted.sort((a, b) => {
      const nameA = locale.value === 'zh' ? a.name : a.nameEn
      const nameB = locale.value === 'zh' ? b.name : b.nameEn
      return nameA.localeCompare(nameB)
    })
    result[key] = sorted
  }
  return result
})

const getColorClass = (val: number) => {
  if (val >= 90) return 'text-green-400'
  if (val >= 80) return 'text-emerald-400'
  if (val >= 70) return 'text-amber-400'
  if (val >= 60) return 'text-orange-400'
  return 'text-red-400'
}

const getBarColor = (val: number) => {
  if (val >= 90) return 'bg-green-500'
  if (val >= 80) return 'bg-emerald-500'
  if (val >= 70) return 'bg-amber-500'
  if (val >= 60) return 'bg-orange-500'
  return 'bg-red-500'
}

type SortField = 'fifaRanking' | 'attack' | 'defense' | 'midfield' | 'physical' | 'tactics' | 'experience' | 'avg'
const sortField = ref<SortField>('fifaRanking')
const sortDir = ref<'asc' | 'desc'>('asc')

const sortedTeams = computed(() => {
  const list = [...store.teams]
  list.sort((a, b) => {
    let va: number, vb: number
    if (sortField.value === 'avg') {
      va = getAvg(a)
      vb = getAvg(b)
    } else if (sortField.value === 'fifaRanking') {
      va = a.fifaRanking
      vb = b.fifaRanking
    } else {
      va = a.ratings[sortField.value as keyof typeof a.ratings]
      vb = b.ratings[sortField.value as keyof typeof b.ratings]
    }
    return sortDir.value === 'asc' ? va - vb : vb - va
  })
  return list
})

const toggleSort = (field: SortField) => {
  if (sortField.value === field) {
    sortDir.value = sortDir.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortField.value = field
    sortDir.value = field === 'fifaRanking' ? 'asc' : 'desc'
  }
}

const sortIcon = (field: SortField) => {
  if (sortField.value !== field) return ''
  return sortDir.value === 'asc' ? '▲' : '▼'
}
</script>

<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- Header -->
    <div class="flex items-center gap-4 mb-8">
      <div class="w-1 h-8 bg-gradient-to-b from-amber-400 to-amber-600 rounded-full"></div>
      <div>
        <h1 class="text-3xl font-bold gradient-text">{{ t('ratings.title') }}</h1>
        <p class="text-sm text-text-muted mt-1">{{ t('ratings.subtitle') }}</p>
      </div>
    </div>

    <!-- Top 5 per Dimension Mini Bar Charts -->
    <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3 mb-8">
      <div
        v-for="key in dimKeys"
        :key="key"
        class="glass-card p-4"
      >
        <div class="text-xs text-text-muted mb-2 text-center">{{ dimLabels[key] }}</div>
        <div class="space-y-2">
          <router-link
            v-for="team in top5PerDim[key]"
            :key="team.id"
            :to="`/teams/${team.id}`"
            class="flex items-center gap-2 group"
          >
            <img :src="team.flag" :alt="team.name" class="w-5 h-3 object-cover rounded flex-shrink-0" />
            <span class="text-[11px] text-text-secondary w-12 truncate group-hover:text-amber-400 transition-colors">
              {{ locale === 'zh' ? team.name : team.nameEn }}
            </span>
            <div class="flex-1 bg-white/5 rounded-full h-1.5 overflow-hidden">
              <div
                class="h-full rounded-full transition-all duration-500"
                :class="getBarColor(team.ratings[key])"
                :style="{ width: `${team.ratings[key]}%` }"
              ></div>
            </div>
            <span class="text-[10px] font-mono font-bold w-5 text-right" :class="getColorClass(team.ratings[key])">
              {{ team.ratings[key] }}
            </span>
          </router-link>
        </div>
      </div>
    </div>

    <!-- Table -->
    <div class="glass-card overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead>
            <tr class="border-b border-white/5">
              <th class="text-left px-4 py-4 text-text-muted font-medium text-xs uppercase tracking-wider w-12">#</th>
              <th class="text-left px-4 py-4 text-text-muted font-medium text-xs uppercase tracking-wider min-w-[180px]">
                {{ t('teams.name') }}
              </th>
              <th
                class="px-3 py-4 text-text-muted font-medium text-xs uppercase tracking-wider cursor-pointer hover:text-amber-400 transition-colors whitespace-nowrap text-center"
                @click="toggleSort('fifaRanking')"
              >
                FIFA <span class="text-[10px]">{{ sortIcon('fifaRanking') }}</span>
              </th>
              <th
                v-for="key in dimKeys"
                :key="key"
                class="px-3 py-4 text-text-muted font-medium text-xs uppercase tracking-wider cursor-pointer hover:text-amber-400 transition-colors whitespace-nowrap text-center min-w-[110px]"
                @click="toggleSort(key)"
              >
                {{ dimLabels[key] }} <span class="text-[10px]">{{ sortIcon(key) }}</span>
              </th>
              <th
                class="px-3 py-4 text-text-muted font-medium text-xs uppercase tracking-wider cursor-pointer hover:text-amber-400 transition-colors whitespace-nowrap text-center min-w-[90px]"
                @click="toggleSort('avg')"
              >
                {{ t('ratings.avg') }} <span class="text-[10px]">{{ sortIcon('avg') }}</span>
              </th>
              <th class="px-4 py-4 text-text-muted font-medium text-xs uppercase tracking-wider text-center w-8">{{ t('teams.group') }}</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(team, idx) in sortedTeams"
              :key="team.id"
              class="border-b border-white/[0.03] hover:bg-white/[0.03] transition-colors group"
            >
              <td class="px-4 py-3.5 text-text-muted text-center text-xs">{{ idx + 1 }}</td>
              <td class="px-4 py-3.5">
                <router-link
                  :to="`/teams/${team.id}`"
                  class="flex items-center gap-3 hover:text-amber-400 transition-colors"
                >
                  <img :src="team.flag" :alt="team.name" class="w-8 h-5 object-cover rounded shadow-lg flex-shrink-0" />
                  <div>
                    <div class="font-medium text-text-primary group-hover:text-amber-400 transition-colors leading-tight">
                      {{ locale === 'zh' ? team.name : team.nameEn }}
                    </div>
                    <div v-if="locale === 'zh' && team.nameEn" class="text-[11px] text-text-muted leading-tight mt-0.5">{{ team.nameEn }}</div>
                  </div>
                </router-link>
              </td>
              <td class="px-3 py-3.5 text-center">
                <span class="text-text-muted text-xs font-mono">{{ team.fifaRanking }}</span>
              </td>
              <td
                v-for="key in dimKeys"
                :key="key"
                class="px-3 py-3.5"
              >
                <div class="flex items-center gap-2 justify-center">
                  <span class="font-mono font-bold text-sm" :class="getColorClass(team.ratings[key])">{{ team.ratings[key] }}</span>
                  <div class="w-16 h-1.5 bg-white/5 rounded-full overflow-hidden hidden lg:block">
                    <div
                      class="h-full rounded-full transition-all duration-500"
                      :class="getBarColor(team.ratings[key])"
                      :style="{ width: `${team.ratings[key]}%` }"
                    ></div>
                  </div>
                </div>
              </td>
              <td class="px-3 py-3.5 text-center">
                <span class="font-mono font-bold text-sm" :class="getColorClass(getAvg(team))">{{ getAvg(team) }}</span>
              </td>
              <td class="px-4 py-3.5 text-center">
                <router-link
                  :to="`/groups/${team.group}`"
                  class="inline-flex items-center justify-center w-7 h-5 rounded text-[11px] font-bold bg-white/5 text-text-muted hover:bg-amber-500/20 hover:text-amber-400 transition-all"
                >
                  {{ team.group }}
                </router-link>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Footer Info -->
    <div class="mt-6 text-center">
      <p class="text-xs text-text-muted">{{ t('ratings.footer', { count: sortedTeams.length }) }}</p>
    </div>
  </div>
</template>