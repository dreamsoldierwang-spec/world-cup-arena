<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useTeamStore } from '@/stores/teamStore'

const { t, locale } = useI18n()
const store = useTeamStore()

const confederationNames: Record<string, string> = {
  UEFA: '欧洲 (UEFA)',
  CONMEBOL: '南美洲 (CONMEBOL)',
  CONCACAF: '中北美 (CONCACAF)',
  CAF: '非洲 (CAF)',
  AFC: '亚洲 (AFC)',
  OFC: '大洋洲 (OFC)',
}

const groupLabels = computed(() => {
  const groups = new Set(store.teams.map(t => t.group))
  return Array.from(groups).sort()
})
</script>

<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <h1 class="text-2xl font-black text-text-primary mb-2">{{ t('teams.title') }}</h1>
    <p class="text-sm text-text-muted mb-8">Browse all 48 teams, filter by group or confederation</p>

    <!-- Filters -->
    <div class="glass-card p-5 mb-6">
      <div class="grid md:grid-cols-4 gap-4">
        <!-- Search -->
        <div>
          <label class="block text-xs font-medium text-text-muted mb-1.5">{{ t('teams.search') }}</label>
          <input
            v-model="store.searchQuery"
            type="text"
            class="w-full px-3 py-2 bg-bg-elevated border border-white/10 rounded-lg text-sm text-text-primary placeholder-text-dim focus:outline-none focus:border-primary/50 focus:ring-1 focus:ring-primary/20 transition-all"
            :placeholder="t('teams.search')"
          />
        </div>

        <!-- Group Filter -->
        <div>
          <label class="block text-xs font-medium text-text-muted mb-1.5">{{ t('teams.filterByGroup') }}</label>
          <select
            v-model="store.selectedGroup"
            class="w-full px-3 py-2 bg-bg-elevated border border-white/10 rounded-lg text-sm text-text-primary focus:outline-none focus:border-primary/50 transition-all"
          >
            <option value="">{{ t('common.all') }}</option>
            <option v-for="g in groupLabels" :key="g" :value="g">Group {{ g }}</option>
          </select>
        </div>

        <!-- Confederation Filter -->
        <div>
          <label class="block text-xs font-medium text-text-muted mb-1.5">{{ t('teams.filterByConfederation') }}</label>
          <select
            v-model="store.selectedConfederation"
            class="w-full px-3 py-2 bg-bg-elevated border border-white/10 rounded-lg text-sm text-text-primary focus:outline-none focus:border-primary/50 transition-all"
          >
            <option value="">{{ t('common.all') }}</option>
            <option v-for="c in store.confederations" :key="c" :value="c">{{ confederationNames[c] || c }}</option>
          </select>
        </div>

        <!-- Sort -->
        <div>
          <label class="block text-xs font-medium text-text-muted mb-1.5">{{ t('teams.sortBy') }}</label>
          <select
            v-model="store.sortBy"
            class="w-full px-3 py-2 bg-bg-elevated border border-white/10 rounded-lg text-sm text-text-primary focus:outline-none focus:border-primary/50 transition-all"
          >
            <option value="fifaRanking">{{ t('teams.fifaRanking') }}</option>
            <option value="name">{{ t('teams.name') }}</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Teams Grid -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3">
      <router-link
        v-for="team in store.filteredTeams"
        :key="team.id"
        :to="`/teams/${team.id}`"
        class="glass-card p-5 card-hover"
      >
        <div class="flex items-center gap-3">
          <img :src="team.flag" :alt="team.name" class="w-10 h-7 object-cover rounded shadow-sm" />
          <div class="flex-1 min-w-0">
            <div class="font-bold text-text-primary text-sm truncate">{{ locale === 'zh' ? team.name : team.nameEn }}</div>
            <div class="text-xs text-text-muted">{{ team.fifaCode }} · Group {{ team.group }}</div>
          </div>
        </div>
        <div class="mt-3 flex items-center justify-between">
          <div class="text-xs">
            <span class="text-text-muted">FIFA</span>
            <span class="font-bold text-primary ml-1">#{{ team.fifaRanking }}</span>
          </div>
          <div v-if="team.isHost" class="status-badge bg-primary/15 text-primary">
            Host
          </div>
        </div>
        <div class="mt-2 text-[11px] text-text-dim">
          {{ confederationNames[team.confederation] || team.confederation }}
        </div>
        
        <!-- Mini rating bars -->
        <div class="mt-3 flex gap-1">
          <div v-for="(val, key) in team.ratings" :key="key" class="flex-1">
            <div class="h-1 bg-white/5 rounded-full overflow-hidden">
              <div class="h-full rounded-full" :class="{
                'bg-accent-red': key === 'attack',
                'bg-accent-blue': key === 'defense',
                'bg-accent-green': key === 'midfield',
                'bg-accent-cyan': key === 'physical',
                'bg-accent-purple': key === 'tactics',
                'bg-primary': key === 'experience',
              }" :style="{ width: val + '%' }"></div>
            </div>
          </div>
        </div>
      </router-link>
    </div>

    <div v-if="store.filteredTeams.length === 0" class="text-center py-12 text-text-muted">
      {{ t('common.noData') }}
    </div>
  </div>
</template>
