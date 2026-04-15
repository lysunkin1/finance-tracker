// ── Toast notifications ─────────────────────────────────────────
function showToast(msg, type = 'success') {
    const el = document.createElement('div');
    el.className = `fixed top-5 right-5 z-50 px-5 py-3 rounded-xl text-white text-sm font-medium shadow-xl transition-all duration-300 ${
        type === 'success' ? 'bg-green-500' : 'bg-red-500'
    }`;
    el.textContent = msg;
    document.body.appendChild(el);
    setTimeout(() => el.remove(), 3000);
}

// ── API helper ───────────────────────────────────────────────────
const api = {
    async request(method, path, body = null) {
        const token = localStorage.getItem('access_token');
        const headers = { 'Content-Type': 'application/json' };
        if (token) headers['Authorization'] = `Bearer ${token}`;

        const opts = { method, headers };
        if (body !== null) opts.body = JSON.stringify(body);

        const res = await fetch(path, opts);

        if (res.status === 401) {
            localStorage.clear();
            window.location.href = '/ui/login.html';
            return;
        }
        if (res.status === 204) return null;

        const data = await res.json().catch(() => null);
        if (!res.ok) {
            const detail = data?.detail;
            const msg = typeof detail === 'string' ? detail
                : Array.isArray(detail) ? detail.map(e => e.msg).join(', ')
                : 'Request failed';
            throw new Error(msg);
        }
        return data;
    },
    get:    (path)       => api.request('GET',    path),
    post:   (path, body) => api.request('POST',   path, body),
    patch:  (path, body) => api.request('PATCH',  path, body),
    delete: (path)       => api.request('DELETE', path),
};

// ── Auth utils ───────────────────────────────────────────────────
function requireAuth() {
    if (!localStorage.getItem('access_token')) {
        window.location.href = '/ui/login.html';
        return false;
    }
    return true;
}
function logout() {
    localStorage.clear();
    window.location.href = '/ui/login.html';
}
function getUsername() {
    return localStorage.getItem('username') || 'User';
}

// ── Currency formatter ───────────────────────────────────────────
function fmt(amount) {
    return Number(amount).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

// ── Sidebar nav ──────────────────────────────────────────────────
function renderNav(activePage) {
    const items = [
        { href: '/ui/',                   icon: '📊', label: 'Dashboard',    id: 'dashboard' },
        { href: '/ui/transactions.html',  icon: '💳', label: 'Transactions', id: 'transactions' },
        { href: '/ui/categories.html',    icon: '🏷️', label: 'Categories',   id: 'categories' },
        { href: '/ui/tags.html',          icon: '🔖', label: 'Tags',         id: 'tags' },
    ];
    document.getElementById('nav').innerHTML = `
        <aside class="w-64 bg-gray-900 min-h-screen flex flex-col fixed left-0 top-0 z-20 shadow-2xl">
            <div class="p-5 border-b border-gray-800">
                <div class="flex items-center gap-3">
                    <div class="w-10 h-10 bg-blue-600 rounded-xl flex items-center justify-center text-xl shrink-0">💰</div>
                    <div class="min-w-0">
                        <p class="text-white font-bold text-sm leading-tight">Finance Tracker</p>
                        <p class="text-gray-400 text-xs truncate">${getUsername()}</p>
                    </div>
                </div>
            </div>
            <nav class="flex-1 p-3 space-y-0.5">
                ${items.map(i => `
                    <a href="${i.href}" class="flex items-center gap-3 px-4 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                        activePage === i.id
                            ? 'bg-blue-600 text-white'
                            : 'text-gray-400 hover:text-white hover:bg-gray-800'
                    }">
                        <span class="text-base">${i.icon}</span>${i.label}
                    </a>`).join('')}
            </nav>
            <div class="p-3 border-t border-gray-800">
                <button onclick="logout()" class="w-full flex items-center gap-3 px-4 py-2.5 text-gray-400 hover:text-white hover:bg-gray-800 rounded-lg text-sm transition-colors">
                    <span>🚪</span>Logout
                </button>
            </div>
        </aside>`;
}
