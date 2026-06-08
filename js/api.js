// ── Celebrity Management Platform — API Layer ──────────────────────────────
const API_BASE = "http://127.0.0.1:8000/api";

if ("serviceWorker" in navigator && window.isSecureContext) {
  window.addEventListener("load", () => {
    navigator.serviceWorker.register("/sw.js").catch(() => {});
  });
}

// ── Token helpers ────────────────────────────────────────────────────────────
const Auth = {
  getAccess: () => localStorage.getItem("access_token"),
  getRefresh: () => localStorage.getItem("refresh_token"),
  getUser: () => JSON.parse(localStorage.getItem("user") || "null"),
  isLoggedIn: () => !!localStorage.getItem("access_token"),
  isAdmin: () => {
    const u = Auth.getUser();
    return u && (u.is_staff || u.is_superuser);
  },
  save: (data) => {
    localStorage.setItem("access_token", data.access);
    localStorage.setItem("refresh_token", data.refresh);
    localStorage.setItem("user", JSON.stringify(data.user));
  },
  clear: () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("user");
  },
};

// ── Core fetch wrapper ───────────────────────────────────────────────────────
async function apiFetch(path, options = {}) {
  const headers = { "Content-Type": "application/json", ...(options.headers || {}) };
  const token = Auth.getAccess();
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const res = await fetch(`${API_BASE}${path}`, { ...options, headers });

  if (res.status === 401) {
    // Try refresh
    const refresh = Auth.getRefresh();
    if (refresh) {
      const r2 = await fetch(`${API_BASE}/auth/token/refresh/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ refresh }),
      });
      if (r2.ok) {
        const tokens = await r2.json();
        localStorage.setItem("access_token", tokens.access);
        headers["Authorization"] = `Bearer ${tokens.access}`;
        const retry = await fetch(`${API_BASE}${path}`, { ...options, headers });
        if (!retry.ok) throw await retry.json();
        return retry.json();
      }
    }
    Auth.clear();
    window.location.href = "/login.html";
    return;
  }

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Unknown error" }));
    throw err;
  }

  if (res.status === 204) return null;
  return res.json();
}

function get(path) { return apiFetch(path); }
function post(path, body) { return apiFetch(path, { method: "POST", body: JSON.stringify(body) }); }
function put(path, body) { return apiFetch(path, { method: "PUT", body: JSON.stringify(body) }); }
function del(path) { return apiFetch(path, { method: "DELETE" }); }

// ── Media URL helper ─────────────────────────────────────────────────────────
function mediaURL(path) {
  if (!path) return "https://placehold.co/600x400/1a1a2e/a78bfa?text=No+Image";
  if (path.startsWith("http")) return path;
  return `http://127.0.0.1:8000${path}`;
}

// ── Auth API ─────────────────────────────────────────────────────────────────
const AuthAPI = {
  register: (data) => post("/auth/register/", data),
  login: async (data) => {
    const res = await post("/auth/login/", data);
    Auth.save(res);
    return res;
  },
  profile: () => get("/auth/profile/"),
  logout: () => { Auth.clear(); window.location.href = "/login.html"; },
};

// ── Celebs API ───────────────────────────────────────────────────────────────
const CelebsAPI = {
  list: (search = "") => get(`/celebs/${search ? "?search=" + search : ""}`),
  detail: (slug) => get(`/celebs/${slug}/`),
};

// ── Memberships API ──────────────────────────────────────────────────────────
const MembershipsAPI = {
  tiers: (celebSlug) => get(`/memberships/tiers/${celebSlug ? "?celebrity=" + celebSlug : ""}`),
  purchase: (tierId) => post("/memberships/purchase/", { tier_id: tierId }),
  mine: () => get("/memberships/mine/"),
};

// ── Donations API ────────────────────────────────────────────────────────────
const DonationsAPI = {
  foundations: (celebSlug) => get(`/donations/foundations/${celebSlug ? "?celebrity=" + celebSlug : ""}`),
  donate: (data) => post("/donations/donate/", data),
  mine: () => get("/donations/mine/"),
  recent: (foundationId) => get(`/donations/foundations/${foundationId}/recent/`),
};

// ── Events API ───────────────────────────────────────────────────────────────
const EventsAPI = {
  list: (celebSlug, status = "") => {
    let qs = celebSlug ? `?celebrity=${celebSlug}` : "?";
    if (status) qs += `&status=${status}`;
    return get(`/events/${qs}`);
  },
  detail: (celebSlug, slug) => get(`/events/${celebSlug}/${slug}/`),
  register: (eventId) => post("/events/register/", { event_id: eventId }),
  mine: () => get("/events/mine/"),
};

// ── UI Utility helpers ───────────────────────────────────────────────────────
function showToast(msg, type = "success") {
  const t = document.createElement("div");
  const color = type === "success" ? "bg-violet-600" : type === "error" ? "bg-red-600" : "bg-amber-500";
  t.className = `fixed top-6 right-6 z-[9999] px-5 py-3 rounded-xl shadow-2xl text-white text-sm font-semibold ${color} transition-all duration-300`;
  t.textContent = msg;
  document.body.appendChild(t);
  setTimeout(() => { t.style.opacity = "0"; setTimeout(() => t.remove(), 400); }, 3000);
}

function setLoading(el, loading, originalText = "Submit") {
  if (loading) {
    el.disabled = true;
    el.innerHTML = `<svg class="animate-spin h-4 w-4 inline mr-2" viewBox="0 0 24 24" fill="none"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"/></svg>Processing…`;
  } else {
    el.disabled = false;
    el.textContent = originalText;
  }
}

function formatMoney(val) {
  return `$${parseFloat(val).toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
}

function formatDate(iso) {
  if (!iso) return "—";
  return new Date(iso).toLocaleDateString("en-US", { year: "numeric", month: "short", day: "numeric" });
}

function requireAuth(redirectTo = null) {
  if (!Auth.isLoggedIn()) {
    const back = redirectTo || window.location.href;
    window.location.href = `/login.html?next=${encodeURIComponent(back)}`;
    return false;
  }
  return true;
}

function updateNavAuth() {
  const navAuth = document.getElementById("nav-auth");
  if (!navAuth) return;
  if (Auth.isLoggedIn()) {
    const user = Auth.getUser();
    navAuth.innerHTML = `
      <a href="/dashboard.html" class="text-gray-300 hover:text-violet-400 transition text-sm">${user.name}</a>
      ${Auth.isAdmin() ? '<a href="/admin-panel/index.html" class="text-amber-400 hover:text-amber-300 text-sm ml-4">Admin</a>' : ""}
      <button onclick="AuthAPI.logout()" class="ml-4 bg-violet-700 hover:bg-violet-600 text-white px-4 py-1.5 rounded-full text-sm transition">Logout</button>
    `;
  } else {
    navAuth.innerHTML = `
      <a href="/login.html" class="text-gray-300 hover:text-violet-400 transition text-sm">Login</a>
      <a href="/register.html" class="ml-4 bg-violet-600 hover:bg-violet-500 text-white px-4 py-1.5 rounded-full text-sm transition">Sign Up</a>
    `;
  }
}

function getParam(key) {
  return new URLSearchParams(window.location.search).get(key);
}
