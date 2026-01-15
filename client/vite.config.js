import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/login': 'http://127.0.0.1:5555',
      '/signup': 'http://127.0.0.1:5555',
      '/check_session': 'http://127.0.0.1:5555',
      '/houses': 'http://127.0.0.1:5555',
      '/bookings': 'http://127.0.0.1:5555',
      '/my-bookings': 'http://127.0.0.1:5555',
      '/favorites': 'http://127.0.0.1:5555',
      '/reviews': 'http://127.0.0.1:5555',
      '/users': 'http://127.0.0.1:5555',

    }
  }
})
