import axios from 'axios'

const API = axios.create({
  baseURL: 'http://localhost:8000/api',
  timeout: 120000
})

export default API
