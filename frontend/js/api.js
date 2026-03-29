/**
 * NexGen Hospital — API Client (FINAL)
 */

const API = (() => {

  const BASE = 'http://127.0.0.1:8000';

  // ================= TOKEN =================
  const token = () => localStorage.getItem('nexgen_token');

  const headers = () => ({
    'Content-Type': 'application/json',
    ...(token() ? { Authorization: `Bearer ${token()}` } : {})
  });

  // ================= CORE REQUEST =================
  async function apiCall(url, options = {}) {
  let token = localStorage.getItem("nexgen_token");

  options.headers = {
    ...options.headers,
    Authorization: "Bearer " + token
  };

  let res = await fetch(url, options);

  // 🔁 auto refresh
  if (res.status === 401) {
    const refresh = localStorage.getItem("nexgen_refresh");

    const r = await fetch("/api/auth/refresh", {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({ refresh_token: refresh })
    });

    const data = await r.json();

    if (data.access_token) {
      localStorage.setItem("nexgen_token", data.access_token);
      return apiCall(url, options);
    }
  }

  return res;
}
  }

  // ================= GENERIC =================
  const get    = (p)    => request('GET', p);
  const post   = (p, b) => request('POST', p, b);
  const put    = (p, b) => request('PUT', p, b);
  const patch  = (p, b) => request('PATCH', p, b);
  const del    = (p)    => request('DELETE', p);

  // ================= AUTH =================
  async function login(username, password) {
    const res = await post('/auth/login', { username, password });

    if (res.success) {
      const d = res.data;

      localStorage.setItem('nexgen_token', d.token);
      localStorage.setItem('nexgen_username', d.username);
      localStorage.setItem('nexgen_role', d.role);
      localStorage.setItem('nexgen_name', d.fullName);

      return d;
    }

    throw new Error(res.message || 'Login failed');
  }

  function logout() {
    ['nexgen_token','nexgen_username','nexgen_role','nexgen_name']
      .forEach(k => localStorage.removeItem(k));

    window.location.href = 'login.html';
  }

  function getUser() {
    return {
      username: localStorage.getItem('nexgen_username'),
      role: localStorage.getItem('nexgen_role'),
      token: localStorage.getItem('nexgen_token')
    };
  }

  function requireRole(...roles) {
    const user = getUser();

    if (!user.token) {
      window.location.href = 'login.html';
      return false;
    }

    if (roles.length && !roles.includes(user.role)) {
      window.location.href = roleHome(user.role);
      return false;
    }

    return true;
  }

  function roleHome(role) {
    return role === 'ADMIN'   ? 'admin.html'
         : role === 'DOCTOR'  ? 'doctor.html'
         : role === 'PATIENT' ? 'patient.html'
         : 'login.html';
  }

  // ================= ADMIN APIs =================

  async function getPatients() {
    const res = await get('/admin/patients');
    return res.data || [];
  }

  async function addPatient(data) {
    return await post('/admin/patients', data);
  }

  async function getDoctors() {
    const res = await get('/admin/doctors');
    return res.data || [];
  }

  async function addDoctor(data) {
    return await post('/admin/doctors', data);
  }

  async function getAppointments() {
    const res = await get('/admin/appointments');
    return res.data || [];
  }

  async function addAppointment(data) {
    return await post('/admin/appointments', data);
  }

  async function getRecords() {
    const res = await get('/admin/records');
    return res.data || [];
  }

  async function getDashboard() {
    const res = await get('/admin/dashboard');
    return res.data || {};
  }

  // ================= EXPORT =================
  return {
    get, post, put, patch, del,
    login, logout, getUser, requireRole, roleHome,

    // Admin APIs
    getPatients,
    addPatient,
    getDoctors,
    addDoctor,
    getAppointments,
    addAppointment,
    getRecords,
    getDashboard
  };

})();


// ================= SIMPLE TOAST =================
function toast(msg, type = 'success') {
  const colors = {
    success: '#00e5a0',
    error: '#ff4757',
    info: '#00d4ff'
  };

  const el = document.createElement('div');
  el.style = `
    position:fixed;
    bottom:20px;
    right:20px;
    background:#0b1120;
    border-left:4px solid ${colors[type]};
    color:white;
    padding:12px 18px;
    border-radius:8px;
    z-index:9999;
  `;
  el.textContent = msg;

  document.body.appendChild(el);

  setTimeout(() => el.remove(), 3000);
}