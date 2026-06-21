# 2026 世界杯竞技场 | World Cup Arena

[![Vue 3](https://img.shields.io/badge/Vue-3.5-42b883?logo=vue.js)](https://vuejs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.7-3178c6?logo=typescript)](https://www.typescriptlang.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-4.0-06b6d4?logo=tailwindcss)](https://tailwindcss.com/)
[![Vite](https://img.shields.io/badge/Vite-8.0-646cff?logo=vite)](https://vitejs.dev/)

> 2026 美加墨世界杯 48 支参赛球队实力全解析
> Comprehensive Power Analysis of All 48 Teams in the 2026 FIFA World Cup

[Live Demo](https://dreamsoldierwang-spec.github.io/world-cup-arena/)

---

## 功能特性 | Features

- **48 支球队完整数据** — 每支球队包含主教练、23 人球员阵容（主力+替补）、职业生涯履历、荣誉记录
- **六维战力分析** — 进攻力、防守力、中场控制、体能、战术纪律、大赛经验
- **数据可视化** — 极坐标柱状图、折线图对比、条形图、迷你进度条等多种图表
- **球队对比** — 支持多支球队六维战力并排对比
- **小组分析** — 12 个小组实力对比，支持组间导航
- **战力排行榜** — 所有球队六维数值一览，支持排序
- **中英文双语** — 一键切换语言
- **深色玻璃拟态 UI** — 现代炫酷的视觉风格

## 技术栈 | Tech Stack

- **Framework**: Vue 3 Composition API + TypeScript
- **Build Tool**: Vite 8
- **Styling**: Tailwind CSS 4 + 自定义玻璃拟态主题
- **Charts**: ECharts 5
- **State**: Pinia
- **Routing**: Vue Router
- **I18n**: Vue I18n
- **Deploy**: GitHub Pages

## 项目结构 | Project Structure

```
world-cup-arena/
├── src/
│   ├── components/
│   │   ├── charts/          # ECharts 图表组件
│   │   └── layout/          # 布局组件（Header）
│   ├── data/
│   │   └── teams.json       # 48 支球队完整数据
│   ├── locales/             # 中英文翻译
│   ├── router/              # 路由配置
│   ├── stores/              # Pinia 状态管理
│   ├── views/               # 页面视图
│   └── App.vue
├── public/
├── index.html
├── vite.config.ts
├── tailwind.config.ts
└── package.json
```

## 本地开发 | Local Development

```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build

# 类型检查
npm run type-check
```

## 数据来源 | Data Sources

球队数据基于 2026 年世界杯预选赛结果、FIFA 排名及公开球员信息整理，包含：
- 48 支参赛球队 × 23 人 = 1104 名真实球员
- 主教练执教履历与战术风格
- 近 10 年大赛战绩
- 六维战力评分（基于球队阵容、历史表现综合评估）

## 许可证 | License

MIT

---

Made with passion for the beautiful game.
