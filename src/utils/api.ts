import axios from 'axios';
import { GridData } from '../types';

// const api = axios.create({
//   baseURL: 'http://localhost:8000',
// });

const baseURL = 'http://192.168.1.44:8003';

export function getGridData() {
  return axios.get<GridData>(`${baseURL}/gridData`);
}

export function toggleRecording() {
    return axios.get(`${baseURL}/toggleRecord`);
}

export function startRecording() {
    return axios.get(`${baseURL}/startRecord`);
}

export function stopRecording() {
    return axios.get(`${baseURL}/stopRecord`);
}

export function toggleStream() {
    return axios.get(`${baseURL}/toggleStream`);
}

export function startStream() {
    return axios.get(`${baseURL}/startStream`);
}

export function stopStream() {
    return axios.get(`${baseURL}/stopStream`);
}

export function getVersion() {
    return axios.get(`${baseURL}/getVersion`);
}