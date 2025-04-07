// const API_URL = 'http://localhost:8000'
const API_URL = 'https://fruitsback.fpr.lol'

export const getAuthHeaders = () => {
  const token = localStorage.getItem('token')
  return token ? { Authorization: `Bearer ${token}` } : {}
}

export { API_URL }
