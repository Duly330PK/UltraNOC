import { fetchData } from './apiClient';
export const getDevices = () => fetchData('/api/v1/devices');