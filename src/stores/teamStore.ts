import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import teamsData from '../data/teams.json'

export interface Team {
  id: string
  name: string
  nameEn: string
  fifaCode: string
  flag: string
  fifaRanking: number
  confederation: string
  group: string
  isHost?: boolean
  coach: Coach
  players: Player[]
  recentResults: MatchResult[]
  ratings: Ratings
  worldCupHistory: WorldCupHistory[]
}

export interface Coach {
  name: string
  nameEn: string
  nationality: string
  nationalityEn: string
  age: number
  since: string
  tacticalStyle: string
  achievements: string[]
  career: CareerEvent[]
}

export interface CareerEvent {
  year: string
  event: string
  eventEn: string
}

export interface Player {
  name: string
  nameEn: string
  position: string
  positionEn: string
  age: number
  club: string
  clubCountry: string
  number: number
  isStarter: boolean
  rating: number
  internationalGoals: number
  internationalCaps: number
  career: CareerEvent[]
  honors: string[]
}

export interface MatchResult {
  competition: string
  competitionEn: string
  year: number
  result: string
  resultEn: string
  matches: number
  wins: number
  draws: number
  losses: number
  goalsFor: number
  goalsAgainst: number
}

export interface Ratings {
  attack: number
  defense: number
  midfield: number
  physical: number
  tactics: number
  experience: number
}

export interface WorldCupHistory {
  year: number
  result: string
  resultEn: string
}

export const useTeamStore = defineStore('team', () => {
  const teams = ref<Team[]>(teamsData as Team[])
  const searchQuery = ref('')
  const selectedGroup = ref('')
  const selectedConfederation = ref('')
  const sortBy = ref('fifaRanking')

  const confederations = computed(() => {
    const confs = new Set(teams.value.map(t => t.confederation))
    return Array.from(confs)
  })

  const groups = computed(() => {
    const grps = new Set(teams.value.map(t => t.group))
    return Array.from(grps).sort()
  })

  const filteredTeams = computed(() => {
    let result = teams.value

    if (searchQuery.value) {
      const query = searchQuery.value.toLowerCase()
      result = result.filter(t =>
        t.name.toLowerCase().includes(query) ||
        t.nameEn.toLowerCase().includes(query) ||
        t.fifaCode.toLowerCase().includes(query)
      )
    }

    if (selectedGroup.value) {
      result = result.filter(t => t.group === selectedGroup.value)
    }

    if (selectedConfederation.value) {
      result = result.filter(t => t.confederation === selectedConfederation.value)
    }

    if (sortBy.value === 'fifaRanking') {
      result = [...result].sort((a, b) => a.fifaRanking - b.fifaRanking)
    } else if (sortBy.value === 'name') {
      result = [...result].sort((a, b) => a.name.localeCompare(b.name))
    }

    return result
  })

  const getTeamById = (id: string) => {
    return teams.value.find(t => t.id === id)
  }

  const getTeamsByGroup = (group: string) => {
    return teams.value.filter(t => t.group === group).sort((a, b) => a.fifaRanking - b.fifaRanking)
  }

  const getTopTeams = (count: number = 8) => {
    return [...teams.value].sort((a, b) => a.fifaRanking - b.fifaRanking).slice(0, count)
  }

  return {
    teams,
    searchQuery,
    selectedGroup,
    selectedConfederation,
    sortBy,
    confederations,
    groups,
    filteredTeams,
    getTeamById,
    getTeamsByGroup,
    getTopTeams,
  }
})
