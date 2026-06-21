<script setup lang="ts">
import { computed, ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useTeamStore } from '@/stores/teamStore'
import * as echarts from 'echarts'

const route = useRoute()
const router = useRouter()
const { t, locale } = useI18n()
const store = useTeamStore()

const groupId = computed(() => route.params.groupId as string)
const teams = computed(() => store.getTeamsByGroup(groupId.value))

const chartRef = ref<HTMLDivElement>()
let chart: echarts.ECharts | null = null

const dimKeys = ['attack', 'defense', 'midfield', 'physical', 'tactics', 'experience']

const dimLabels = computed(() => [
  t('teamDetail.attack'),
  t('teamDetail.defense'),
  t('teamDetail.midfield'),
  t('teamDetail.physical'),
  t('teamDetail.tactics'),
  t('teamDetail.experience'),
])

const teamColors = ['#3b82f6', '#ef4444', '#10b981', '#a855f7']

// --- Group Navigation ---
const allGroups = computed(() => store.groups)

const currentGroupIndex = computed(() => {
  return allGroups.value.indexOf(groupId.value)
})

const prevGroup = computed(() => {
  if (currentGroupIndex.value > 0) {
    return allGroups.value[currentGroupIndex.value - 1]
  }
  return null
})

const nextGroup = computed(() => {
  if (currentGroupIndex.value < allGroups.value.length - 1) {
    return allGroups.value[currentGroupIndex.value + 1]
  }
  return null
})

const navigateToGroup = (group: string) => {
  router.push(`/groups/${group}`)
}

const dropdownOpen = ref(false)
const dropdownRef = ref<HTMLDivElement>()

const toggleDropdown = () => {
  dropdownOpen.value = !dropdownOpen.value
}

const selectGroup = (g: string) => {
  dropdownOpen.value = false
  navigateToGroup(g)
}

const handleClickOutside = (e: MouseEvent) => {
  if (dropdownRef.value && !dropdownRef.value.contains(e.target as Node)) {
    dropdownOpen.value = false
  }
}

onMounted(() => {
  initChart()
  window.addEventListener('resize', () => chart?.resize())
  document.addEventListener('click', handleClickOutside)
})

// --- Chart ---
const initChart = () => {
  if (!chartRef.value) return
  chart = echarts.init(chartRef.value)
  updateChart()
}

const updateChart = () => {
  if (!chart || teams.value.length === 0) return

  const indicator = dimKeys.map(key => ({
    name: getDimLabel(key),
    max: 100,
  }))

  const series = teams.value.map((team, index) => ({
    type: 'bar' as const,
    name: locale.value === 'zh' ? team.name : team.nameEn,
    coordinateSystem: 'polar' as const,
    data: dimKeys.map(key => team.ratings[key as keyof typeof team.ratings]),
    color: teamColors[index % 4],
    barWidth: 6,
    itemStyle: {
      borderRadius: 3,
    },
  }))

  const option: echarts.EChartsOption = {
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(17, 24, 39, 0.9)',
      borderColor: 'rgba(251, 191, 36, 0.3)',
      textStyle: { color: '#f1f5f9' },
    },
    legend: {
      bottom: 0,
      textStyle: { fontSize: 13, color: '#94a3b8' },
      itemWidth: 20,
      itemHeight: 12,
    },
    polar: {
      radius: [20, '70%'],
    },
    angleAxis: {
      type: 'category',
      data: dimLabels.value,
      axisLabel: { color: '#94a3b8', fontSize: 12 },
      axisLine: { lineStyle: { color: 'rgba(255, 255, 255, 0.1)' } },
    },
    radiusAxis: {
      min: 0,
      max: 100,
      axisLabel: { color: '#94a3b8', fontSize: 11 },
      axisLine: { lineStyle: { color: 'rgba(255, 255, 255, 0.1)' } },
      splitLine: { lineStyle: { color: 'rgba(255, 255, 255, 0.05)' } },
    },
    series,
  }

  chart.setOption(option, true)
}

const getDimLabel = (key: string) => {
  const map: Record<string, { zh: string; en: string }> = {
    attack: { zh: '进攻力', en: 'Attack' },
    defense: { zh: '防守力', en: 'Defense' },
    midfield: { zh: '中场控制', en: 'Midfield' },
    physical: { zh: '体能', en: 'Physical' },
    tactics: { zh: '战术纪律', en: 'Tactics' },
    experience: { zh: '大赛经验', en: 'Experience' },
  }
  return locale.value === 'zh' ? map[key].zh : map[key].en
}

watch(() => teams.value, updateChart, { deep: true })
watch(locale, updateChart)
</script>

<template>
  <div v-if="teams.length > 0" class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- Navigation Bar -->
    <div class="flex flex-wrap items-center gap-3 mb-8">
      <!-- Back Button -->
      <button
        @click="router.push('/groups')"
        class="px-4 py-2 glass-card hover:bg-white/10 transition-colors text-text-primary text-sm flex items-center gap-1.5"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
        {{ t('common.back') }}
      </button>

      <!-- Previous Group -->
      <button
        v-if="prevGroup"
        @click="navigateToGroup(prevGroup)"
        class="px-3 py-2 glass-card hover:bg-white/10 transition-colors text-text-secondary hover:text-text-primary text-sm flex items-center gap-1"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 17l-5-5m0 0l5-5m-5 5h12" />
        </svg>
        <span class="hidden sm:inline">{{ t('groups.prevGroup') }}</span>
        <span class="sm:hidden">{{ prevGroup }}</span>
      </button>

      <!-- Group Dropdown Selector -->
      <div ref="dropdownRef" class="relative">
        <button
          @click="toggleDropdown"
          class="px-5 py-2 glass-card hover:bg-white/10 transition-colors text-text-primary font-bold flex items-center gap-2 min-w-[120px] justify-between"
        >
          <span class="gradient-text text-lg">{{ t('groups.group') }} {{ groupId }}</span>
          <svg
            class="w-4 h-4 text-text-secondary transition-transform duration-200"
            :class="{ 'rotate-180': dropdownOpen }"
            fill="none" stroke="currentColor" viewBox="0 0 24 24"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
          </svg>
        </button>

        <!-- Dropdown Menu -->
        <Transition
          enter-active-class="transition-all duration-200 ease-out"
          enter-from-class="opacity-0 -translate-y-2"
          enter-to-class="opacity-100 translate-y-0"
          leave-active-class="transition-all duration-150 ease-in"
          leave-from-class="opacity-100 translate-y-0"
          leave-to-class="opacity-0 -translate-y-2"
        >
          <div
            v-if="dropdownOpen"
            class="absolute top-full left-0 mt-2 glass-card p-1.5 min-w-[180px] z-50 border border-white/10"
          >
            <button
              v-for="g in allGroups"
              :key="g"
              @click="selectGroup(g)"
              class="w-full px-4 py-2.5 rounded-lg text-left text-sm transition-all flex items-center gap-2"
              :class="g === groupId
                ? 'bg-amber-500/20 text-amber-400 font-bold'
                : 'text-text-secondary hover:text-text-primary hover:bg-white/5'"
            >
              <span class="w-8 h-5 rounded flex items-center justify-center text-xs font-bold"
                :class="g === groupId ? 'bg-amber-500/30 text-amber-400' : 'bg-white/5 text-text-muted'"
              >
                {{ g }}
              </span>
              <span>{{ t('groups.group') }} {{ g }}</span>
              <span v-if="g === groupId" class="ml-auto text-amber-400">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7" />
                </svg>
              </span>
            </button>
          </div>
        </Transition>
      </div>

      <!-- Next Group -->
      <button
        v-if="nextGroup"
        @click="navigateToGroup(nextGroup)"
        class="px-3 py-2 glass-card hover:bg-white/10 transition-colors text-text-secondary hover:text-text-primary text-sm flex items-center gap-1"
      >
        <span class="hidden sm:inline">{{ t('groups.nextGroup') }}</span>
        <span class="sm:hidden">{{ nextGroup }}</span>
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
        </svg>
      </button>

      <!-- Spacer -->
      <div class="flex-1"></div>

      <!-- Group indicator badge -->
      <div class="px-3 py-1.5 glass-card text-xs text-text-muted flex items-center gap-1.5">
        <span>{{ currentGroupIndex + 1 }} / {{ allGroups.length }}</span>
      </div>
    </div>

    <!-- Teams List -->
    <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
      <router-link
        v-for="team in teams"
        :key="team.id"
        :to="`/teams/${team.id}`"
        class="glass-card p-6 hover:border-amber-500/30 transition-all group"
      >
        <div class="flex items-center gap-3 mb-3">
          <img :src="team.flag" :alt="team.name" class="w-12 h-8 object-cover rounded shadow-lg" />
          <div>
            <div class="font-bold text-text-primary group-hover:text-amber-400 transition-colors">{{ locale === 'zh' ? team.name : team.nameEn }}</div>
            <div class="text-sm text-text-muted">FIFA #{{ team.fifaRanking }}</div>
          </div>
        </div>
        <div class="text-xs text-text-muted">
          {{ t('teamDetail.coach') }}: {{ locale === 'zh' ? team.coach.name : team.coach.nameEn }}
        </div>
      </router-link>
    </div>

    <!-- Polar Bar Chart Comparison -->
    <div class="glass-card p-6">
      <h2 class="text-lg font-bold gradient-text mb-4">{{ t('groups.strengthCompare') }}</h2>
      <div ref="chartRef" class="w-full h-96"></div>
    </div>
  </div>

  <div v-else class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 text-center">
    <p class="text-text-muted">{{ t('common.noData') }}</p>
    <button @click="router.push('/groups')" class="mt-4 px-4 py-2 bg-amber-500 text-slate-900 rounded-lg hover:bg-amber-400 font-medium transition-colors">
      {{ t('common.back') }}
    </button>
  </div>
</template>