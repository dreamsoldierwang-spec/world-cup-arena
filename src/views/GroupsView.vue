<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useTeamStore } from '@/stores/teamStore'
import type { Team } from '@/stores/teamStore'

const { t, locale } = useI18n()
const store = useTeamStore()

const groups = computed(() => {
  const groupMap: Record<string, Team[]> = {}
  store.teams.forEach(team => {
    if (!groupMap[team.group]) groupMap[team.group] = []
    groupMap[team.group].push(team)
  })
  return Object.entries(groupMap)
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([group, teams]) => ({
      group,
      teams: [...teams].sort((a, b) => a.fifaRanking - b.fifaRanking),
    }))
})
</script>

<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <h1 class="text-3xl font-bold gradient-text mb-8">{{ t('groups.title') }}</h1>

    <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
      <router-link
        v-for="groupItem in groups"
        :key="groupItem.group"
        :to="`/groups/${groupItem.group}`"
        class="glass-card p-6 hover:border-amber-500/30 transition-all group"
      >
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-xl font-bold gradient-text">{{ t('groups.group') }} {{ groupItem.group }}</h2>
          <span class="text-sm text-text-muted">{{ groupItem.teams.length }} {{ t('groups.teams') }}</span>
        </div>
        <div class="space-y-3">
          <div
            v-for="team in groupItem.teams"
            :key="team.id"
            class="flex items-center gap-3 p-2 rounded-lg hover:bg-white/5 transition-colors"
          >
            <img :src="team.flag" :alt="team.name" class="w-8 h-5 object-cover rounded" />
            <span class="flex-1 text-sm font-medium text-text-primary">{{ locale === 'zh' ? team.name : team.nameEn }}</span>
            <span class="text-xs text-text-muted">#{{ team.fifaRanking }}</span>
          </div>
        </div>
      </router-link>
    </div>
  </div>
</template>
