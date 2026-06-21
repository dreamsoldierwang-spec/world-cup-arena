<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import * as echarts from 'echarts'

interface ChartData {
  name: string
  nameEn: string
  ratings: Record<string, number>
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
  const dimKeys = ['attack', 'defense', 'midfield', 'physical', 'tactics', 'experience']
  const dimNames = dimKeys.map(k => dims[k as keyof typeof dims])

  // Calculate dynamic y-axis range based on all data values
  const allValues = props.data.flatMap(item => dimKeys.map(k => item.ratings[k]))
  const minValue = Math.min(...allValues)
  const maxValue = Math.max(...allValues)
  const yMin = Math.max(0, Math.floor(minValue / 5) * 5 - 5)
  const yMax = Math.ceil(maxValue / 5) * 5 + 5

  const series = props.data.map((item) => ({
    name: props.locale === 'zh' ? item.name : item.nameEn,
    type: 'line' as const,
    data: dimKeys.map(k => item.ratings[k]),
    smooth: true,
    symbol: 'circle',
    symbolSize: 10,
    lineStyle: {
      width: 3,
      color: item.color,
    },
    itemStyle: {
      color: item.color,
      borderWidth: 2,
      borderColor: '#0a0e1a',
    },
    areaStyle: {
      color: item.color ? item.color + '15' : undefined,
    },
    label: {
      show: true,
      position: 'top' as const,
      color: item.color,
      fontSize: 12,
      fontWeight: 'bold' as const,
      formatter: '{c}',
    },
  }))

  const option: echarts.EChartsOption = {
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(17, 24, 39, 0.9)',
      borderColor: 'rgba(251, 191, 36, 0.3)',
      textStyle: {
        color: '#f1f5f9',
      },
    },
    legend: {
      bottom: 0,
      textStyle: {
        fontSize: 13,
        color: '#94a3b8',
      },
      itemWidth: 25,
      itemHeight: 14,
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '12%',
      top: '8%',
      containLabel: true,
    },
    xAxis: {
      type: 'category',
      data: dimNames,
      axisLabel: {
        color: '#94a3b8',
        fontSize: 13,
      },
      axisLine: {
        lineStyle: {
          color: 'rgba(255, 255, 255, 0.1)',
        },
      },
    },
    yAxis: {
      type: 'value',
      min: yMin,
      max: yMax,
      axisLabel: {
        color: '#94a3b8',
      },
      axisLine: {
        lineStyle: {
          color: 'rgba(255, 255, 255, 0.1)',
        },
      },
      splitLine: {
        lineStyle: {
          color: 'rgba(255, 255, 255, 0.05)',
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
