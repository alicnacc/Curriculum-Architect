import { createSlice, PayloadAction } from '@reduxjs/toolkit'

interface LearningResource {
  id: number
  module_id: number
  title: string
  description?: string
  url: string
  resource_type: 'video' | 'article' | 'interactive' | 'quiz' | 'simulation'
  status: 'pending' | 'in_progress' | 'completed' | 'skipped'
  order: number
  created_at: string
  updated_at?: string
}

interface CurriculumModule {
  id: number
  curriculum_id: number
  title: string
  description?: string
  order: number
  created_at: string
  updated_at?: string
  resources: LearningResource[]
}

interface Curriculum {
  id: number
  user_id: number
  title: string
  description?: string
  created_at: string
  updated_at?: string
  modules: CurriculumModule[]
}

interface CurriculumState {
  curriculums: Curriculum[]
  currentCurriculum: Curriculum | null
  isLoading: boolean
  error: string | null
}

const initialState: CurriculumState = {
  curriculums: [],
  currentCurriculum: null,
  isLoading: false,
  error: null,
}

const curriculumSlice = createSlice({
  name: 'curriculum',
  initialState,
  reducers: {
    fetchCurriculumsStart: (state) => {
      state.isLoading = true
      state.error = null
    },
    fetchCurriculumsSuccess: (state, action: PayloadAction<Curriculum[]>) => {
      state.isLoading = false
      state.curriculums = action.payload
      state.error = null
    },
    fetchCurriculumsFailure: (state, action: PayloadAction<string>) => {
      state.isLoading = false
      state.error = action.payload
    },
    setCurrentCurriculum: (state, action: PayloadAction<Curriculum>) => {
      state.currentCurriculum = action.payload
    },
    addCurriculum: (state, action: PayloadAction<Curriculum>) => {
      state.curriculums.push(action.payload)
    },
    updateCurriculum: (state, action: PayloadAction<Curriculum>) => {
      const index = state.curriculums.findIndex(c => c.id === action.payload.id)
      if (index !== -1) {
        state.curriculums[index] = action.payload
      }
    },
    removeCurriculum: (state, action: PayloadAction<number>) => {
      state.curriculums = state.curriculums.filter(c => c.id !== action.payload)
      if (state.currentCurriculum?.id === action.payload) {
        state.currentCurriculum = null
      }
    },
    updateResourceStatus: (state, action: PayloadAction<{ resourceId: number; status: string }>) => {
      const { resourceId, status } = action.payload
      
      // Update in current curriculum
      if (state.currentCurriculum) {
        state.currentCurriculum.modules.forEach(module => {
          module.resources.forEach(resource => {
            if (resource.id === resourceId) {
              resource.status = status as any
            }
          })
        })
      }
      
      // Update in curriculums list
      state.curriculums.forEach(curriculum => {
        curriculum.modules.forEach(module => {
          module.resources.forEach(resource => {
            if (resource.id === resourceId) {
              resource.status = status as any
            }
          })
        })
      })
    },
    clearError: (state) => {
      state.error = null
    },
  },
})

export const {
  fetchCurriculumsStart,
  fetchCurriculumsSuccess,
  fetchCurriculumsFailure,
  setCurrentCurriculum,
  addCurriculum,
  updateCurriculum,
  removeCurriculum,
  updateResourceStatus,
  clearError,
} = curriculumSlice.actions

export default curriculumSlice.reducer 