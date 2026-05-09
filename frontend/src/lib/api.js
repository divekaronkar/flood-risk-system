import axios from 'axios'

// On Windows, `localhost` can resolve to IPv6 (::1) while backend is bound to 127.0.0.1.
// Default to 127.0.0.1 to avoid "Network Error" in the browser.
const API_BASE = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

export const api = axios.create({
  baseURL: `${API_BASE}/api`,
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

