<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import * as echarts from 'echarts'

interface ChartData {
  name: string
  value: number
}

const props = defineProps<{
  data: ChartData[]
}>()

const chartRef = ref<HTMLDivElement>()
let chart: echarts.ECharts | null = null

const colors = ['#fbbf24', '#f59e0b', '#ef4444', '#10b981', '#3b82f6', '#8b5cf6']

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
      trigger: 'item',
      formatter: '{b}: {c} ({d}%)',
      backgroundColor: 'rgba(17, 24, 39, 0.9)',
      borderColor: 'rgba(251, 191, 36, 0.3)',
      textStyle: {
        color: '#f1f5f9',
      },
    },
    legend: {
      orient: 'vertical',
      left: 'left',
      textStyle: {
        color: '#94a3b8',
      },
    },
    series: [{
      type: 'pie',
      radius: ['40%', '70%'],
      avoidLabelOverlap: false,
      itemStyle: {
        borderRadius: 10,
        borderColor: '#0a0e1a',
        borderWidth: 2,
      },
      label: {
        show: true,
        formatter: '{b}\n{c}',
        color: '#f1f5f9',
      },
      emphasis: {
        label: {
          show: true,
          fontSize: 16,
          fontWeight: 'bold',
          color: '#f1f5f9',
        },
        itemStyle: {
          shadowBlur: 10,
          shadowColor: 'rgba(251, 191, 36, 0.5)',
        },
      },
      data: props.data.map((d, i) => ({
        ...d,
        itemStyle: { color: colors[i % colors.length] },
      })),
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
