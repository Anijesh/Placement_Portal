import axios from "axios"

const API = "http://127.0.0.1:5001/api/student"

const getAuthHeaders = () => {
  const token = localStorage.getItem("token")
  return {
    headers: {
      Authorization: `Bearer ${token}`
    }
  }
}

export function fetchProfile() {
  return axios.get(`${API}/profile`, getAuthHeaders())
}

export function updateProfile(data) {
  return axios.put(`${API}/profile`, data, getAuthHeaders())
}

export function fetchJobs() {
  return axios.get(`${API}/jobs/list`, getAuthHeaders())
}

export function applyJob(jobId) {
  return axios.post(`${API}/job/${jobId}/apply`, {}, getAuthHeaders())
}

export function fetchApplications() {
  return axios.get(`${API}/application/list`, getAuthHeaders())
}

export function fetchPlacements() {
  return axios.get(`${API}/placements`, getAuthHeaders())
}

export function exportCSV() {
  return axios.get(`${API}/export/csv`, getAuthHeaders())
}
