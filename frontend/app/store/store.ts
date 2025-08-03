import { configureStore } from '@reduxjs/toolkit'
import authReducer from './slices/authSlice'
import curriculumReducer from './slices/curriculumSlice'

export const store = configureStore({
  reducer: {
    auth: authReducer,
    curriculum: curriculumReducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: ['persist/PERSIST'],
      },
    }),
})

export type RootState = ReturnType<typeof store.getState>
export type AppDispatch = typeof store.dispatch 