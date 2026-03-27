import axios from "axios";

const API = "http://127.0.0.1:5001/api/admin";

const getAuthHeaders = () => {
  const token = localStorage.getItem("token");
  return {
    headers: {
      Authorization: `Bearer ${token}`
    }
  };
};

export function fetchStats() {
  return axios.get(`${API}/stats`, getAuthHeaders());
}

export function fetchCompanies() {
  return axios.get(`${API}/companies`, getAuthHeaders());
}

export function approveCompany(id) {
  return axios.put(`${API}/companies/${id}/approve`, {}, getAuthHeaders());
}

export function rejectCompany(id) {
  return axios.put(`${API}/companies/${id}/reject`, {}, getAuthHeaders());
}

export function activateCompany(id) {
  return axios.put(`${API}/companies/${id}/activate`, {}, getAuthHeaders());
}

export function deactivateCompany(id) {
  return axios.put(`${API}/companies/${id}/deactivate`, {}, getAuthHeaders());
}

export function fetchStudents() {
  return axios.get(`${API}/students`, getAuthHeaders());
}

export function activateStudent(id) {
  return axios.put(`${API}/students/${id}/activate`, {}, getAuthHeaders());
}

export function deactivateStudent(id) {
  return axios.put(`${API}/students/${id}/deactivate`, {}, getAuthHeaders());
}

export function searchStudents(query) {
  return axios.get(`${API}/students/search?q=${query}`, getAuthHeaders());
}

export function searchCompanies(query) {
  return axios.get(`${API}/companies/search?q=${query}`, getAuthHeaders());
}

export function fetchJobs() {
  return axios.get(`${API}/job/list`, getAuthHeaders());
}

export function approveJob(id) {
  return axios.put(`${API}/job/${id}/approve`, {}, getAuthHeaders());
}

export function rejectJob(id) {
  return axios.put(`${API}/job/${id}/reject`, {}, getAuthHeaders());
}

export function fetchApplications() {
  return axios.get(`${API}/application/list`, getAuthHeaders());
}

export function fetchPlacements() {
  return axios.get(`${API}/placement/list`, getAuthHeaders());
}
