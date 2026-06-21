<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import * as echarts from 'echarts'

interface SingleData {
  name: string
  value: number
  color?: string
}

interface MultiSeriesData {
  dimensions: string[]
  series: {
    name: string
    data: number[]
    color?: string
  }[]
}

const props = defineProps<{
  data: SingleData[] | MultiSeriesData
  title?: string
  horizontal?: boolean
}>()

const chartRef = ref<HTMLDivElement>()
let chart: echarts.ECharts | null = null

const isMultiSeries = (data: SingleData[] | MultiSeriesData): data is MultiSeriesData => {
  return 'dimensions' in data && 'series' in data
}

const initChart = () => {
  if (!chartRef.value) return
  chart = echarts.init(chartRef.value)
  updateChart()
}

const updateChart = () => {
  if (!chart) return

  if (isMultiSeries(props.data)) {
    // Multi-series comparison mode
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
      legend: {
        top: 0,
        textStyle: {
          fontSize: 12,
          color: '#94a3b8',
        },
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        top: '15%',
        containLabel: true,
      },
      xAxis: {
        type: 'category',
        data: props.data.dimensions,
        axisLabel: { color: '#94a3b8', fontSize: 12 },
        axisLine: { lineStyle: { color: 'rgba(255, 255, 255, 0.1)' } },
      },
      yAxis: {
        type: 'value',
        axisLine: { lineStyle: { color: 'rgba(255, 255, 255, 0.1)' } },
        splitLine: { lineStyle: { color: 'rgba(255, 255, 255, 0.05)' } },
        axisLabel: { color: '#94a3b8' },
      },
      series: props.data.series.map((s) => ({
        type: 'bar',
        name: s.name,
        data: s.data,
        itemStyle: {
          color: s.color,
          borderRadius: [4, 4, 0, 0],
        },
        barGap: '10%',
        label: {
          show: true,
          position: 'top',
          color: '#f1f5f9',
          fontSize: 11,
        },
      })),
    }
    chart.setOption(option, true)
  } else {
    // Single series mode
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
            axisLine: { lineStyle: { color: 'rgba(255, 255, 255, 0.1)' } },
            splitLine: { lineStyle: { color: 'rgba(255, 255, 255, 0.05)' } },
            axisLabel: { color: '#94a3b8' },
          }
        : {
            type: 'category',
            data: props.data.map((d) => d.name),
            axisLabel: { rotate: 45, color: '#94a3b8' },
            axisLine: { lineStyle: { color: 'rgba(255, 255, 255, 0.1)' } },
          },
      yAxis: props.horizontal
        ? {
            type: 'category',
            data: props.data.map((d) => d.name),
            axisLabel: { color: '#94a3b8' },
            axisLine: { lineStyle: { color: 'rgba(255, 255, 255, 0.1)' } },
          }
        : {
            type: 'value',
            axisLine: { lineStyle: { color: 'rgba(255, 255, 255, 0.1)' } },
            splitLine: { lineStyle: { color: 'rgba(255, 255, 255, 0.05)' } },
            axisLabel: { color: '#94a3b8' },
          },
      series: [
        {
          type: 'bar',
          data: props.data.map((d) => ({
            value: d.value,
            itemStyle: {
              color:
                d.color ||
                new echarts.graphic.LinearGradient(0, 0, 1, 0, [
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
        },
      ],
    }
    chart.setOption(option, true)
  }
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
