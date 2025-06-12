export const fetchData = async (endpoint) => {
  const res = await fetch(endpoint);
  return res.json();
};