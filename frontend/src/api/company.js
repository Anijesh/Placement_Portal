import axios from "axios"

const API = "http://127.0.0.1:5001/api/company"

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

export function createJob(jobData) {
  return axios.post(`${API}/create/job`, jobData, getAuthHeaders())
}

export function fetchJobs() {
  return axios.get(`${API}/job/list`, getAuthHeaders())
}

export function fetchApplications(jobId) {
  return axios.get(`${API}/job/application/${jobId}/list`, getAuthHeaders())
}

export function shortlistApplication(appId, feedback = "") {
  return axios.put(`${API}/application/${appId}/shortlist`, { feedback }, getAuthHeaders())
}

export function rejectApplication(appId, feedback = "") {
  return axios.put(`${API}/application/${appId}/reject`, { feedback }, getAuthHeaders())
}

export function acceptApplication(appId) {
  return axios.put(`${API}/application/${appId}/accept`, {}, getAuthHeaders())
}

export function closeJob(jobId) {
  return axios.put(`${API}/job/${jobId}/close`, {}, getAuthHeaders())
}

export function reopenJob(jobId) {
  return axios.put(`${API}/job/${jobId}/reopen`, {}, getAuthHeaders())
}

export function scheduleInterview(appId, data) {
  return axios.put(`${API}/application/${appId}/interview`, data, getAuthHeaders())
}

export function exportCSV() {
  return axios.get(`${API}/export/csv`, getAuthHeaders())
}
