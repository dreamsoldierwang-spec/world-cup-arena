<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useTeamStore } from '@/stores/teamStore'
import RadarChart from '@/components/charts/RadarChart.vue'

const route = useRoute()
const router = useRouter()
const { t, locale } = useI18n()
const store = useTeamStore()

const team = computed(() => store.getTeamById(route.params.id as string))
const activeTab = ref('overview')

const tabs = [
  { key: 'overview', label: 'teamDetail.overview' },
  { key: 'ratings', label: 'teamDetail.ratings' },
  { key: 'squad', label: 'teamDetail.squad' },
  { key: 'history', label: 'teamDetail.history' },
]

const radarData = computed(() => {
  if (!team.value) return []
  return [{
    name: team.value.name,
    nameEn: team.value.nameEn,
    ratings: team.value.ratings,
    color: '#fbbf24',
  }]
})

const ratingLabels = [
  { key: 'attack', color: 'bg-red-500', icon: '⚡' },
  { key: 'defense', color: 'bg-blue-500', icon: '🛡️' },
  { key: 'midfield', color: 'bg-emerald-500', icon: '🎯' },
  { key: 'physical', color: 'bg-yellow-500', icon: '💪' },
  { key: 'tactics', color: 'bg-purple-500', icon: '🧠' },
  { key: 'experience', color: 'bg-orange-500', icon: '⭐' },
]

const positionOrder = ['GK', 'DF', 'MF', 'FW']
const positionLabels: Record<string, string> = {
  GK: '门将',
  DF: '后卫',
  MF: '中场',
  FW: '前锋',
}

const sortedPlayers = computed(() => {
  if (!team.value) return []
  return [...team.value.players].sort((a, b) => {
    const posDiff = positionOrder.indexOf(a.position) - positionOrder.indexOf(b.position)
    if (posDiff !== 0) return posDiff
    return b.rating - a.rating
  })
})

const starters = computed(() => sortedPlayers.value.filter(p => p.isStarter))
const substitutes = computed(() => sortedPlayers.value.filter(p => !p.isStarter))
</script>

<template>
  <div v-if="team" class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- Team Header -->
    <div class="glass-card p-6 mb-6">
      <div class="flex flex-col md:flex-row items-start md:items-center gap-6">
        <img :src="team.flag" :alt="team.name" class="w-24 h-16 object-cover rounded-lg shadow-lg ring-2 ring-white/10" />
        <div class="flex-1">
          <div class="flex items-center gap-3">
            <h1 class="text-3xl font-bold gradient-text">
              {{ locale === 'zh' ? team.name : team.nameEn }}
            </h1>
            <span v-if="team.isHost" class="px-3 py-1 bg-amber-500/20 text-amber-400 text-sm rounded-full font-medium border border-amber-500/30">
              Host
            </span>
          </div>
          <div class="flex flex-wrap gap-4 mt-2 text-sm text-text-secondary">
            <span class="flex items-center gap-1">
              <span class="text-text-muted">FIFA {{ t('teamDetail.fifaRanking') }}:</span>
              <strong class="text-amber-400">#{{ team.fifaRanking }}</strong>
            </span>
            <span class="flex items-center gap-1">
              <span class="text-text-muted">{{ t('teamDetail.group') }}:</span>
              <strong class="text-amber-400">{{ team.group }}</strong>
            </span>
            <span class="flex items-center gap-1">
              <span class="text-text-muted">{{ t('teamDetail.confederation') }}:</span>
              <span>{{ team.confederation }}</span>
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- Tabs -->
    <div class="glass-card mb-6 overflow-hidden">
      <div class="border-b border-white/5">
        <nav class="flex -mb-px">
          <button
            v-for="tab in tabs"
            :key="tab.key"
            @click="activeTab = tab.key"
            class="px-6 py-4 text-sm font-medium border-b-2 transition-colors"
            :class="activeTab === tab.key ? 'border-amber-400 text-amber-400' : 'border-transparent text-text-secondary hover:text-text-primary'"
          >
            {{ t(tab.label) }}
          </button>
        </nav>
      </div>

      <div class="p-6">
        <!-- Overview Tab -->
        <div v-if="activeTab === 'overview'">
          <div class="grid md:grid-cols-2 gap-8">
            <!-- Coach Info -->
            <div>
              <h3 class="text-lg font-bold gradient-text mb-4">{{ t('teamDetail.coach') }}</h3>
              <div class="glass-card p-4">
                <div class="font-bold text-text-primary">{{ locale === 'zh' ? team.coach.name : team.coach.nameEn }}</div>
                <div class="text-sm text-text-secondary mt-1">
                  {{ locale === 'zh' ? team.coach.nationality : team.coach.nationalityEn }} · {{ team.coach.age }}岁 · {{ t('teamDetail.since') }} {{ team.coach.since }}
                </div>
                <div class="text-sm text-text-secondary mt-1">{{ t('teamDetail.tactics') }}: {{ team.coach.tacticalStyle }}</div>
                <div class="mt-3">
                  <div class="text-xs font-medium text-text-muted mb-1">{{ t('teamDetail.honors') }}</div>
                  <div class="flex flex-wrap gap-1">
                    <span v-for="(ach, i) in team.coach.achievements" :key="i" class="px-2 py-1 bg-amber-500/10 text-amber-400 text-xs rounded border border-amber-500/20">
                      {{ ach }}
                    </span>
                  </div>
                </div>
                <div class="mt-3">
                  <div class="text-xs font-medium text-text-muted mb-1">{{ t('teamDetail.career') }}</div>
                  <div class="space-y-1 max-h-40 overflow-y-auto custom-scrollbar">
                    <div v-for="(career, i) in team.coach.career" :key="i" class="text-xs text-text-secondary">
                      <span class="font-medium text-amber-400">{{ career.year }}</span> - {{ locale === 'zh' ? career.event : career.eventEn }}
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Recent Results -->
            <div>
              <h3 class="text-lg font-bold gradient-text mb-4">{{ t('teamDetail.recentResults') }}</h3>
              <div class="space-y-3">
                <div v-for="(result, i) in team.recentResults" :key="i" class="glass-card p-4">
                  <div class="flex items-center justify-between">
                    <div>
                      <div class="font-medium text-text-primary">{{ locale === 'zh' ? result.competition : result.competitionEn }} {{ result.year }}</div>
                      <div class="text-sm text-text-secondary">{{ locale === 'zh' ? result.result : result.resultEn }}</div>
                    </div>
                    <div class="text-right text-sm">
                      <div class="text-text-muted">{{ result.wins }}W {{ result.draws }}D {{ result.losses }}L</div>
                      <div class="text-text-muted">{{ result.goalsFor }}:{{ result.goalsAgainst }}</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Ratings Tab -->
        <div v-if="activeTab === 'ratings'">
          <div class="grid md:grid-cols-2 gap-8">
            <RadarChart :data="radarData" :locale="locale" />
            <div class="space-y-4">
              <h3 class="text-lg font-bold gradient-text">{{ t('teamDetail.ratings') }}</h3>
              <div v-for="label in ratingLabels" :key="label.key" class="flex items-center gap-4">
                <div class="w-8 text-center text-lg">{{ label.icon }}</div>
                <div class="w-20 text-sm font-medium text-text-secondary">{{ t(`teamDetail.${label.key}`) }}</div>
                <div class="flex-1 bg-white/5 rounded-full h-3">
                  <div
                    class="h-3 rounded-full transition-all duration-500"
                    :class="label.color"
                    :style="{ width: `${team.ratings[label.key as keyof typeof team.ratings]}%` }"
                  ></div>
                </div>
                <div class="w-10 text-right font-bold text-amber-400">{{ team.ratings[label.key as keyof typeof team.ratings] }}</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Squad Tab -->
        <div v-if="activeTab === 'squad'">
          <div class="mb-6">
            <h3 class="text-lg font-bold gradient-text mb-4">{{ t('teamDetail.starters') }}</h3>
            <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
              <div v-for="player in starters" :key="player.name" class="glass-card p-4 hover:border-amber-500/30 transition-all">
                <div class="flex items-center gap-3">
                  <div class="w-10 h-10 bg-gradient-to-br from-amber-400 to-orange-500 text-white rounded-full flex items-center justify-center font-bold shadow-lg">
                    {{ player.number }}
                  </div>
                  <div class="flex-1 min-w-0">
                    <div class="font-medium text-text-primary truncate">{{ locale === 'zh' ? player.name : player.nameEn }}</div>
                    <div class="text-xs text-text-muted">{{ positionLabels[player.position] || player.position }} · {{ player.age }}岁</div>
                  </div>
                  <div class="text-right">
                    <div class="font-bold text-amber-400">{{ player.rating }}</div>
                  </div>
                </div>
                <div class="mt-2 text-xs text-text-secondary">
                  {{ player.club }} ({{ player.clubCountry }})
                </div>
                <div class="mt-1 text-xs text-text-muted">
                  {{ player.internationalCaps }} {{ t('teamDetail.caps') }} · {{ player.internationalGoals }} {{ t('teamDetail.goals') }}
                </div>
                <!-- Career Timeline -->
                <div class="mt-2 max-h-24 overflow-y-auto custom-scrollbar">
                  <div v-for="(career, i) in player.career" :key="i" class="text-xs text-text-muted">
                    <span class="text-amber-400">{{ career.year }}</span> - {{ locale === 'zh' ? career.event : career.eventEn }}
                  </div>
                </div>
                <!-- Honors -->
                <div v-if="player.honors.length > 0" class="mt-2 flex flex-wrap gap-1">
                  <span v-for="(honor, i) in player.honors" :key="i" class="px-1.5 py-0.5 bg-amber-500/10 text-amber-400 text-xs rounded border border-amber-500/20">
                    {{ honor }}
                  </span>
                </div>
              </div>
            </div>
          </div>

          <div>
            <h3 class="text-lg font-bold gradient-text mb-4">{{ t('teamDetail.substitutes') }}</h3>
            <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
              <div v-for="player in substitutes" :key="player.name" class="glass-card p-4 opacity-70 hover:opacity-100 transition-opacity">
                <div class="flex items-center gap-3">
                  <div class="w-10 h-10 bg-white/10 text-white rounded-full flex items-center justify-center font-bold">
                    {{ player.number }}
                  </div>
                  <div class="flex-1 min-w-0">
                    <div class="font-medium text-text-primary truncate">{{ locale === 'zh' ? player.name : player.nameEn }}</div>
                    <div class="text-xs text-text-muted">{{ positionLabels[player.position] || player.position }} · {{ player.age }}岁</div>
                  </div>
                  <div class="text-right">
                    <div class="font-bold text-text-secondary">{{ player.rating }}</div>
                  </div>
                </div>
                <div class="mt-2 text-xs text-text-secondary">
                  {{ player.club }} ({{ player.clubCountry }})
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- History Tab -->
        <div v-if="activeTab === 'history'">
          <h3 class="text-lg font-bold gradient-text mb-4">{{ t('teamDetail.history') }}</h3>
          <div class="overflow-x-auto">
            <table class="w-full text-sm">
              <thead>
                <tr class="bg-white/5">
                  <th class="px-4 py-3 text-left text-amber-400 font-medium">{{ t('teamDetail.year') }}</th>
                  <th class="px-4 py-3 text-left text-amber-400 font-medium">{{ t('teamDetail.result') }}</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(h, i) in team.worldCupHistory" :key="i" class="border-b border-white/5 hover:bg-white/5 transition-colors">
                  <td class="px-4 py-3 font-medium text-text-primary">{{ h.year }}</td>
                  <td class="px-4 py-3 text-text-secondary">{{ locale === 'zh' ? h.result : h.resultEn }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div v-else class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 text-center">
    <p class="text-text-muted">{{ t('common.noData') }}</p>
    <button @click="router.push('/teams')" class="mt-4 px-4 py-2 bg-amber-500 text-slate-900 rounded-lg hover:bg-amber-400 font-medium transition-colors">
      {{ t('common.back') }}
    </button>
  </div>
</template>
