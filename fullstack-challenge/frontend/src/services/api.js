import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000'
})

export const fetchProviders = (q = '') => api.get('/providers', { params: { q } })
export const createProvider = (payload) => api.post('/providers', payload)
export const updateProvider = (id, payload) => api.put(`/providers/${id}`, payload)
export const deleteProvider = (id) => api.delete(`/providers/${id}`)
