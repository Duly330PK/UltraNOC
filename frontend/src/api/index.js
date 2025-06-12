export async function fetchDevices() {
  return fetch("/api/v1/devices").then(res => res.json());
}
