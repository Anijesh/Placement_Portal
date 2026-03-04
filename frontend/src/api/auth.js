import axios from "axios"

const API = "http://127.0.0.1:5001/api/auth"

export function login(data) {
  return axios.post(`${API}/login`, data)
}

export function register(data) {
  return axios.post(`${API}/register`, data)
}

export function getBranches() {
  return axios.get(`http://127.0.0.1:5001/api/branches`)
}