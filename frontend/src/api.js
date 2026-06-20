// In local dev, fall back to the relative `/api` path (Vite proxies it to the
// Django server). In production, set VITE_API_URL at build time to the deployed
// backend's API base, e.g. https://your-backend.onrender.com/api
const API_BASE = import.meta.env.VITE_API_URL || '/api';

function getToken() {
  return localStorage.getItem('token');
}

async function request(endpoint, options = {}) {
  const token = getToken();
  const headers = { 'Content-Type': 'application/json', ...options.headers };
  if (token) headers['Authorization'] = `Token ${token}`;

  const res = await fetch(`${API_BASE}${endpoint}`, { ...options, headers });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || JSON.stringify(err));
  }
  return res.json();
}

export const api = {
  login: (data) => request('/login/', { method: 'POST', body: JSON.stringify(data) }),
  signup: (data) => request('/signup/', { method: 'POST', body: JSON.stringify(data) }),
  getProfile: () => request('/profile/'),
  updateProfile: (data) => request('/profile/', { method: 'PATCH', body: JSON.stringify(data) }),
  getJobs: (params) => request('/jobs/?' + new URLSearchParams(params || {})),
  getJob: (id) => request(`/jobs/${id}/`),
  getSkillGap: (jobId) => request(`/jobs/${jobId}/skill-gap/`),
  getOutcomes: () => request('/outcomes/'),
  submitOutcome: (data) => request('/outcomes/submit/', { method: 'POST', body: JSON.stringify(data) }),
  getSkills: () => request('/skills/'),
};
