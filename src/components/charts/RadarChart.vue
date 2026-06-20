<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import * as echarts from 'echarts'
import type { Ratings } from '@/stores/teamStore'

interface ChartData {
  name: string
  nameEn: string
  ratings: Ratings
  color?: string
}

const props = defineProps<{
  data: ChartData[]
  locale: string
}>()

const chartRef = ref<HTMLDivElement>()
let chart: echarts.ECharts | null = null

const getDimensions = (locale: string) => ({
  attack: locale === 'zh' ? '进攻力' : 'Attack',
  defense: locale === 'zh' ? '防守力' : 'Defense',
  midfield: locale === 'zh' ? '中场控制' : 'Midfield',
  physical: locale === 'zh' ? '体能' : 'Physical',
  tactics: locale === 'zh' ? '战术纪律' : 'Tactics',
  experience: locale === 'zh' ? '大赛经验' : 'Experience',
})

const initChart = () => {
  if (!chartRef.value) return
  chart = echarts.init(chartRef.value)
  updateChart()
}

const updateChart = () => {
  if (!chart) return
  const dims = getDimensions(props.locale)

  const series: echarts.RadarSeriesOption[] = props.data.map((item) => ({
    name: props.locale === 'zh' ? item.name : item.nameEn,
    type: 'radar' as const,
    data: [{
      value: [
        item.ratings.attack,
        item.ratings.defense,
        item.ratings.midfield,
        item.ratings.physical,
        item.ratings.tactics,
        item.ratings.experience,
      ],
      name: props.locale === 'zh' ? item.name : item.nameEn,
    }],
    areaStyle: {
      opacity: 0.25,
    },
    lineStyle: {
      width: 2,
    },
    symbol: 'circle',
    symbolSize: 6,
    color: item.color || undefined,
  }))

  const option: echarts.EChartsOption = {
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(17, 24, 39, 0.9)',
      borderColor: 'rgba(251, 191, 36, 0.3)',
      textStyle: {
        color: '#f1f5f9',
      },
    },
    legend: {
      bottom: 0,
      textStyle: {
        fontSize: 12,
        color: '#94a3b8',
      },
    },
    radar: {
      indicator: [
        { name: dims.attack, max: 100 },
        { name: dims.defense, max: 100 },
        { name: dims.midfield, max: 100 },
        { name: dims.physical, max: 100 },
        { name: dims.tactics, max: 100 },
        { name: dims.experience, max: 100 },
      ],
      shape: 'polygon',
      splitNumber: 5,
      axisName: {
        color: '#94a3b8',
        fontSize: 12,
      },
      splitLine: {
        lineStyle: {
          color: 'rgba(255, 255, 255, 0.08)',
        },
      },
      splitArea: {
        show: true,
        areaStyle: {
          color: ['rgba(251, 191, 36, 0.02)', 'rgba(251, 191, 36, 0.05)'],
        },
      },
      axisLine: {
        lineStyle: {
          color: 'rgba(255, 255, 255, 0.08)',
        },
      },
    },
    series,
  }

  chart.setOption(option, true)
}

onMounted(() => {
  initChart()
  window.addEventListener('resize', () => chart?.resize())
})

watch(() => props.data, updateChart, { deep: true })
watch(() => props.locale, updateChart)
</script>

<template>
  <div ref="chartRef" class="w-full h-96"></div>
</template>
