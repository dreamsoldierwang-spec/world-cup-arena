<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import * as echarts from 'echarts'

interface ChartData {
  name: string
  value: number
  color?: string
}

const props = defineProps<{
  data: ChartData[]
  title?: string
  horizontal?: boolean
}>()

const chartRef = ref<HTMLDivElement>()
let chart: echarts.ECharts | null = null

const initChart = () => {
  if (!chartRef.value) return
  chart = echarts.init(chartRef.value)
  updateChart()
}

const updateChart = () => {
  if (!chart) return

  const option: echarts.EChartsOption = {
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
      backgroundColor: 'rgba(17, 24, 39, 0.9)',
      borderColor: 'rgba(251, 191, 36, 0.3)',
      textStyle: {
        color: '#f1f5f9',
      },
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true,
    },
    xAxis: props.horizontal
      ? { 
          type: 'value', 
          max: 100,
          axisLine: { lineStyle: { color: 'rgba(255, 255, 255, 0.1)' } },
          splitLine: { lineStyle: { color: 'rgba(255, 255, 255, 0.05)' } },
          axisLabel: { color: '#94a3b8' },
        }
      : { 
          type: 'category', 
          data: props.data.map(d => d.name), 
          axisLabel: { rotate: 45, color: '#94a3b8' },
          axisLine: { lineStyle: { color: 'rgba(255, 255, 255, 0.1)' } },
        },
    yAxis: props.horizontal
      ? { 
          type: 'category', 
          data: props.data.map(d => d.name),
          axisLabel: { color: '#94a3b8' },
          axisLine: { lineStyle: { color: 'rgba(255, 255, 255, 0.1)' } },
        }
      : { 
          type: 'value', 
          max: 100,
          axisLine: { lineStyle: { color: 'rgba(255, 255, 255, 0.1)' } },
          splitLine: { lineStyle: { color: 'rgba(255, 255, 255, 0.05)' } },
          axisLabel: { color: '#94a3b8' },
        },
    series: [{
      type: 'bar',
      data: props.data.map(d => ({
        value: d.value,
        itemStyle: { 
          color: d.color || new echarts.graphic.LinearGradient(0, 0, 1, 0, [
            { offset: 0, color: '#fbbf24' },
            { offset: 1, color: '#f59e0b' },
          ]),
          borderRadius: [4, 4, 4, 4],
        },
      })),
      barWidth: '60%',
      label: {
        show: true,
        position: props.horizontal ? 'right' : 'top',
        color: '#f1f5f9',
      },
    }],
  }

  chart.setOption(option, true)
}

onMounted(() => {
  initChart()
  window.addEventListener('resize', () => chart?.resize())
})

watch(() => props.data, updateChart, { deep: true })
</script>

<template>
  <div ref="chartRef" class="w-full h-80"></div>
</template>
