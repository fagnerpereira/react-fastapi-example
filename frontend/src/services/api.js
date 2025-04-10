const API_URL = import.meta.env.VITE_API_URL

export const getAuthHeaders = () => {
  const token = localStorage.getItem('token')
  return token ? { Authorization: `Bearer ${token}` } : {}
}

export { API_URL }
