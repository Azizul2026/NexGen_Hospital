/**
 * NexGen Hospital — API Client (FINAL DEMO READY)
 */

const API = (() => {

  // 🌐 BACKEND URL
  const BASE = "https://nexgen-hospital-app.onrender.com";

  // ================= TOKEN =================
  const token = () => localStorage.getItem("nexgen_token");

  const headers = () => ({
    "Content-Type": "application/json",
    ...(token() ? { Authorization: `Bearer ${token()}` } : {})
  });

  // ================= CORE REQUEST =================
  async function request(method, path, body) {
    try {
      const res = await fetch(`${BASE}${path}`, {
        method,
        headers: headers(),
        mode: "cors",
        ...(body && { body: JSON.stringify(body) })
      });

      const text = await res.text();

      let data = {};
      try {
        data = text ? JSON.parse(text) : {};
      } catch {
        throw new Error("Server error");
      }

      if (res.status === 401) {
        logout();
        throw new Error("Session expired");
      }

      if (!res.ok) {
        throw new Error(data.detail || data.message || "Request failed");
      }

      return data;

    } catch (err) {
      console.error("API ERROR:", err);
      throw err;
    }
  }

  // ================= GENERIC =================
  const get   = (p)    => request("GET", p);
  const post  = (p, b) => request("POST", p, b);
  const put   = (p, b) => request("PUT", p, b);
  const patch = (p, b) => request("PATCH", p, b);
  const del   = (p)    => request("DELETE", p);

  // ================= 🔥 AUTH (DEMO SAFE LOGIN) =================
  async function login(username, password) {

    // 🔥 DEMO USERS (NO BACKEND DEPENDENCY)
    const users = [
      { username: "admin", password: "admin123", role: "ADMIN" },
      { username: "doctor1", password: "1234", role: "DOCTOR" },
      { username: "patient1", password: "1234", role: "PATIENT" }
    ];

    const user = users.find(
      u => u.username === username && u.password === password
    );

    // ✅ DIRECT LOGIN (FAST + SAFE)
    if (user) {
      localStorage.setItem("nexgen_token", "demo-token");
      localStorage.setItem("nexgen_username", user.username);
      localStorage.setItem("nexgen_role", user.role);

      window.location.href = roleHome(user.role);
      return;
    }

    // 🔁 FALLBACK TO REAL API (if needed)
    try {
      const res = await post("/api/auth/login", { username, password });

      if (res.success && res.data) {
        const d = res.data;

        localStorage.setItem("nexgen_token", d.token);
        localStorage.setItem("nexgen_username", d.username);
        localStorage.setItem("nexgen_role", d.role);

        window.location.href = roleHome(d.role);
        return d;
      }

      throw new Error("Login failed");

    } catch (err) {
      alert("Invalid login");
    }
  }

  function logout() {
    [
      "nexgen_token",
      "nexgen_username",
      "nexgen_role"
    ].forEach(k => localStorage.removeItem(k));

    window.location.href = "login.html";
  }

  function getUser() {
    return {
      username: localStorage.getItem("nexgen_username"),
      role: localStorage.getItem("nexgen_role"),
      token: localStorage.getItem("nexgen_token")
    };
  }

  function requireRole(...roles) {
    const user = getUser();

    if (!user.token) {
      window.location.href = "login.html";
      return false;
    }

    const role = (user.role || "").toUpperCase();

    if (roles.length && !roles.map(r => r.toUpperCase()).includes(role)) {
      window.location.href = roleHome(role);
      return false;
    }

    return true;
  }

  function roleHome(role) {
    role = (role || "").toUpperCase();

    return role === "ADMIN"   ? "admin.html"
         : role === "DOCTOR"  ? "doctor.html"
         : role === "PATIENT" ? "patient.html"
         : "login.html";
  }

  // ================= ADMIN APIs =================
  async function createUser(data) {
    return await post("/api/admin/create-user", data);
  }

  async function getPatients() {
    const res = await get("/api/admin/patients");
    return res.data || [];
  }

  async function addPatient(data) {
    return await post("/api/admin/patients", data);
  }

  async function getDoctors() {
    const res = await get("/api/admin/doctors");
    return res.data || [];
  }

  async function addDoctor(data) {
    return await post("/api/admin/doctors", data);
  }

  async function getDashboard() {
    const res = await get("/api/admin/dashboard");
    return res.data || {};
  }

  // ================= EXPORT =================
  return {
    get, post, put, patch, del,
    login, logout, getUser, requireRole, roleHome,
    createUser,
    getPatients,
    addPatient,
    getDoctors,
    addDoctor,
    getDashboard
  };

})();


// ================= TOAST =================
function toast(msg, type = "success") {
  const colors = {
    success: "#00e5a0",
    error: "#ff4757",
    info: "#00d4ff"
  };

  const el = document.createElement("div");

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
