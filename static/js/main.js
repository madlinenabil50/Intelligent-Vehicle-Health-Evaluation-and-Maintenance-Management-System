/* IVHEMMS System — main.js
   Unified state management, routing, and all page wiring.
   Uses localStorage for demo data (no backend required). */

(function () {
    'use strict';

    const STORAGE_KEY = 'IVHEMMS_v1';

    /* ──────────────────────────────────────────────
       PATH / ROOT HELPERS
       Pages live at depth:
         - login.html, register.html, forgot-password.html → root (depth 0)
         - pages/admin/admin-dashboard.html              → depth 2
    ──────────────────────────────────────────────── */
    function rootPrefix() {
        const path = location.pathname.replace(/\\/g, '/').toLowerCase();
        if (path.includes('/pages/')) return '../../';
        return '';
    }

    function toRoot(p) { return rootPrefix() + p; }

    const ROLE_TO_DASH = {
        admin: 'pages/admin/admin-dashboard.html',
        client: 'pages/client/client-dashboard.html',
        technician: 'pages/technician/technician-dashboard.html',
        inventory: 'pages/inventory/inventory-dashboard.html',
        manager: 'pages/manager/manager-dashboard.html',
        'service-manager': 'pages/manager/manager-dashboard.html',
        'general-manager': 'pages/manager/general-manager-dashboard.html',
        'stock-keeper': 'pages/inventory/inventory-dashboard.html',
        'fleet-manager': 'pages/manager/manager-dashboard.html',
        'finance-manager': 'pages/finance/finance-dashboard.html',
        'data-analyst': 'pages/analytics/data-dashboard.html',
    };

    /* ──────────────────────────────────────────────
       STATE
    ──────────────────────────────────────────────── */
    function loadState() {
        try { const r = localStorage.getItem(STORAGE_KEY); return r ? JSON.parse(r) : null; } catch { return null; }
    }

    function saveState(s) { try { localStorage.setItem(STORAGE_KEY, JSON.stringify(s)); } catch { } }

    function seed() {
        const s = {
            currentUser: null,
            users: [
                { email: 'admin@ivhemms.com', password: 'password', role: 'admin', name: 'Admin User', phone: '+1 555 0100', address: '1 Admin Way' },
                { email: 'client@ivhemms.com', password: 'password', role: 'client', name: 'Jane Doe', phone: '+1 555 0200', address: '42 Oak St' },
                { email: 'tech@ivhemms.com', password: 'password', role: 'technician', name: 'Mike Thompson', phone: '+1 555 0300', address: '7 Garage Rd' },
                { email: 'manager@ivhemms.com', password: 'password', role: 'manager', name: 'Sarah Brown', phone: '+1 555 0400', address: '15 Service Blvd' },
                { email: 'gm@ivhemms.com', password: 'password', role: 'general-manager', name: 'James Lee', phone: '+1 555 0500', address: '88 HQ Tower' },
                { email: 'stock@ivhemms.com', password: 'password', role: 'stock-keeper', name: 'Carlos Rivera', phone: '+1 555 0600', address: '22 Warehouse Ave' },
                { email: 'finance@ivhemms.com', password: 'password', role: 'finance-manager', name: 'Priya Sharma', phone: '+1 555 0700', address: '9 Finance St' },
                { email: 'analyst@ivhemms.com', password: 'password', role: 'data-analyst', name: 'Alex Kim', phone: '+1 555 0800', address: '3 Data Ln' },
            ],
            vehicles: [
                { id: 'V001', clientEmail: 'client@ivhemms.com', make: 'Ford', model: 'Bronco', year: 2021, plate: 'XYZ-1234', vin: '1FMEE5DP4MLA00001', color: 'Blue', status: 'Healthy' },
                { id: 'V002', clientEmail: 'client@ivhemms.com', make: 'Honda', model: 'Civic', year: 2018, plate: 'ABC-9876', vin: 'JHMFC1F35JX000002', color: 'Silver', status: 'Service Required' },
            ],
            workOrders: [
                { id: 'WO-4592', vehicleId: 'V001', vehicle: '2021 Ford Bronco', license: 'XYZ-1234', service: 'Engine Diagnostics', status: 'In Progress', priority: 'High', techEmail: 'tech@ivhemms.com', complaint: 'Check engine light on, shudders at speed.', notes: [{ at: 'Mar 5, 09:30 AM', text: 'OBD-II scan — P0301 misfire code. Checking plugs.' }], checklist: [] },
                { id: 'WO-4595', vehicleId: 'V002', vehicle: '2018 Honda Civic', license: 'ABC-9876', service: 'Brake Pad Replacement', status: 'Waiting on Parts', priority: 'Medium', techEmail: 'tech@ivhemms.com', complaint: 'Grinding noise during braking.', notes: [], checklist: [] },
                { id: 'WO-4601', vehicleId: 'V001', vehicle: '2021 Ford Bronco', license: 'XYZ-1234', service: 'Full Service Inspection', status: 'Queued', priority: 'Low', techEmail: '', complaint: 'Routine annual check.', notes: [], checklist: [] },
                { id: 'WO-4588', vehicleId: 'V002', vehicle: '2018 Honda Civic', license: 'ABC-9876', service: 'Oil Change', status: 'Completed', priority: 'Low', techEmail: 'tech@ivhemms.com', complaint: 'Routine oil change.', notes: [{ at: 'Mar 1, 02:00 PM', text: 'Completed. Used Mobil 1 5W-30.' }], checklist: [] },
            ],
            appointments: [
                { id: 'APT-001', clientEmail: 'client@ivhemms.com', vehicleId: 'V001', service: 'Oil Change', date: '2026-03-15', time: '10:00', notes: 'Need synthetic oil.', status: 'Confirmed' },
                { id: 'APT-002', clientEmail: 'client@ivhemms.com', vehicleId: 'V002', service: 'Brake Inspection', date: '2026-03-22', time: '14:00', notes: '', status: 'Pending' },
            ],
            inventory: [
                { id: 'OIL-5W30', name: 'Synthetic Oil 5W-30', category: 'Fluids', qty: 45, unit: 'L', price: 8.50, minStock: 20 },
                { id: 'BP-1002', name: 'Brake Pads (Front)', category: 'Brakes', qty: 6, unit: 'Units', price: 45.00, minStock: 15 },
                { id: 'SP-102', name: 'Spark Plugs (Set)', category: 'Ignition', qty: 24, unit: 'Sets', price: 12.00, minStock: 10 },
                { id: 'AF-205', name: 'Air Filter', category: 'Filters', qty: 18, unit: 'Units', price: 15.00, minStock: 10 },
                { id: 'COL-001', name: 'Coolant (1L)', category: 'Fluids', qty: 8, unit: 'L', price: 6.50, minStock: 12 },
                { id: 'TRW-88', name: 'Wiper Blades (Pair)', category: 'Accessories', qty: 30, unit: 'Pairs', price: 18.00, minStock: 10 },
                { id: 'BAT-95R', name: 'Heavy Duty Battery', category: 'Electrical', qty: 4, unit: 'Units', price: 150.00, minStock: 5 },
                { id: 'FP-400', name: 'Fuel Pump Assembly', category: 'Fuel System', qty: 3, unit: 'Units', price: 210.00, minStock: 2 },
                { id: 'ALT-120', name: '120A Alternator', category: 'Electrical', qty: 2, unit: 'Units', price: 185.00, minStock: 3 },
                { id: 'RH-505', name: 'Radiator Hose (Upper)', category: 'Cooling', qty: 12, unit: 'Units', price: 24.00, minStock: 5 },
                { id: 'SB-99', name: 'Serpentine Belt', category: 'Engine', qty: 15, unit: 'Units', price: 35.00, minStock: 8 },
            ],
            partsRequests: [
                { id: 'PR-001', woId: 'WO-4595', techEmail: 'tech@ivhemms.com', part: 'Brake Pads (Front)', qty: 2, priority: 'High', status: 'Pending', at: '2026-03-05' },
                { id: 'PR-002', woId: 'WO-4592', techEmail: 'tech@ivhemms.com', part: '120A Alternator', qty: 1, priority: 'Medium', status: 'Pending', at: '2026-03-06' },
                { id: 'PR-003', woId: 'WO-4601', techEmail: 'tech@ivhemms.com', part: 'Fuel Pump Assembly', qty: 1, priority: 'Low', status: 'Pending', at: '2026-03-06' },
            ],
            invoices: [
                { id: 'INV-2001', clientEmail: 'client@ivhemms.com', woId: 'WO-4588', amount: 95.00, tax: 9.50, total: 104.50, status: 'Paid', dueDate: '2026-02-28', issuedDate: '2026-02-20' },
                { id: 'INV-2002', clientEmail: 'client@ivhemms.com', woId: 'WO-4592', amount: 340.00, tax: 34.00, total: 374.00, status: 'Pending', dueDate: '2026-03-20', issuedDate: '2026-03-05' },
                { id: 'INV-2003', clientEmail: 'client@ivhemms.com', woId: 'WO-4595', amount: 210.00, tax: 21.00, total: 231.00, status: 'Sent', dueDate: '2026-03-25', issuedDate: '2026-03-06' },
            ],
            payments: [
                { id: 'PAY-001', invoiceId: 'INV-2001', amount: 104.50, method: 'Card', at: '2026-02-28' },
            ],
            obdReadings: [
                { vehicleId: 'V001', ts: '2026-03-06T01:00:00Z', rpm: 780, speed: 0, coolant: 88, fuel: 72, battery: 14.1, engine_load: 12, o2: 3.2, health: 91, category: 'Good' },
                { vehicleId: 'V002', ts: '2026-03-06T01:00:00Z', rpm: 820, speed: 0, coolant: 95, fuel: 31, battery: 12.6, engine_load: 18, o2: 5.8, health: 54, category: 'Warning' },
            ],
            chatMessages: [],
        };
        saveState(s);
        return s;
    }

    function state() { return loadState() || seed(); }

    /* ──────────────────────────────────────────────
       UTILITIES
    ──────────────────────────────────────────────── */
    function toast(msg, type) {
        const color = type === 'error' ? '#f43f5e' : type === 'warning' ? '#f59e0b' : '#10b981';
        try {
            const wrap = document.createElement('div');
            wrap.className = 'toast-container position-fixed bottom-0 end-0 p-3';
            wrap.style.zIndex = 99999;
            wrap.innerHTML = `
              <div class="toast align-items-center border-0 glass-toast custom-toast" role="alert" style="border-left-color:${color} !important">
                <div class="d-flex">
                  <div class="toast-body fw-semibold">${msg}</div>
                  <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
                </div>
              </div>`;
            document.body.appendChild(wrap);
            const t = wrap.querySelector('.toast');
            const bs = new bootstrap.Toast(t, { delay: 2800 });
            bs.show();
            t.addEventListener('hidden.bs.toast', () => wrap.remove());
        } catch { alert(msg); }
    }

    function dashboardHref() {
        const s = state();
        const role = s.currentUser?.role || 'admin';
        return toRoot(ROLE_TO_DASH[role] || ROLE_TO_DASH.admin);
    }

    function ensureUserPerms(u) {
        if (!u.permissions) {
            const map = {
                admin: ['admin', 'appointments', 'work_orders', 'inventory', 'finance', 'analytics'],
                client: ['appointments'],
                technician: ['work_orders'],
                'service-manager': ['appointments', 'work_orders'],
                'general-manager': ['analytics', 'finance', 'inventory', 'work_orders', 'appointments'],
                'stock-keeper': ['inventory'],
                'finance-manager': ['finance'],
                'data-analyst': ['analytics'],
            };
            u.permissions = map[u.role] || ['appointments'];
        }
        return u;
    }

    function avatarUrl(name, color) {
        const bg = (color || '4361ee').replace('#', '');
        return `https://ui-avatars.com/api/?name=${encodeURIComponent(name || 'User')}&background=${bg}&color=fff&rounded=true`;
    }

    /* ──────────────────────────────────────────────
       TOPBAR BACK BUTTON
    ──────────────────────────────────────────────── */
    function addTopbarBackButton() {
        const isAuthPage = /\/(login|register|forgot-password|change-password)\.html/.test(location.pathname);
        const isDashboard = /\/(admin|client|technician|manager|general-manager|inventory|finance|data)-dashboard\.html/.test(location.pathname) ||
            location.pathname.endsWith('admin-dashboard.html') ||
            location.pathname.endsWith('client-dashboard.html') ||
            location.pathname.endsWith('technician-dashboard.html') ||
            location.pathname.endsWith('manager-dashboard.html') ||
            location.pathname.endsWith('general-manager-dashboard.html') ||
            location.pathname.endsWith('inventory-dashboard.html') ||
            location.pathname.endsWith('finance-dashboard.html') ||
            location.pathname.endsWith('data-dashboard.html');
        const isIndex = /\/(index\.html|)$/.test(location.pathname);

        if (isAuthPage || isDashboard || isIndex) return;

        const topbar = document.querySelector('.topbar');
        if (!topbar) return;
        const title = topbar.querySelector('h1,h2,h3,h4,h5,h6');
        if (!title || title.querySelector('.topbar-back-btn')) return;

        const a = document.createElement('a');
        a.href = '#';
        a.className = 'topbar-back-btn';
        a.innerHTML = '<i class="bi bi-arrow-left"></i>';
        a.addEventListener('click', (e) => {
            e.preventDefault();
            if (window.history.length > 1) window.history.back();
            else location.href = dashboardHref();
        });
        title.classList.add('d-flex', 'align-items-center');
        title.prepend(a);
    }

    /* ──────────────────────────────────────────────
       THEME TOGGLE
    ──────────────────────────────────────────────── */
    function wireTheme() {
        const btn = document.getElementById('themeSwitch');
        if (!btn) return;
        const k = 'ai_theme';
        const saved = localStorage.getItem(k) || 'light';
        document.documentElement.setAttribute('data-theme', saved);
        
        // Update icon on load
        const icon = btn.querySelector('i');
        if (icon) {
            icon.className = saved === 'dark' ? 'bi bi-moon-stars' : 'bi bi-sun';
        }

        btn.addEventListener('click', () => {
            const cur = document.documentElement.getAttribute('data-theme') || 'light';
            const next = cur === 'dark' ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', next);
            localStorage.setItem(k, next);
            if (icon) {
                icon.className = next === 'dark' ? 'bi bi-moon-stars' : 'bi bi-sun';
            }
        });
    }

    /* ──────────────────────────────────────────────
       SIDEBAR TOGGLE (mobile)
    ──────────────────────────────────────────────── */
    function wireSidebarToggle() {
        const btn = document.getElementById('sidebarToggle');
        const sidebar = document.querySelector('.sidebar');
        if (!btn || !sidebar) return;

        // Create overlay
        let overlay = document.querySelector('.sidebar-overlay');
        if (!overlay) {
            overlay = document.createElement('div');
            overlay.className = 'sidebar-overlay';
            document.body.appendChild(overlay);
        }

        btn.addEventListener('click', () => {
            sidebar.classList.toggle('show');
            overlay.classList.toggle('show');
        });
        overlay.addEventListener('click', () => {
            sidebar.classList.remove('show');
            overlay.classList.remove('show');
        });
    }

    /* ──────────────────────────────────────────────
       TOPBAR: user info
    ──────────────────────────────────────────────── */
    function triggerLogoutAnimation() {
        // Inject CSS if not already there
        if (!document.getElementById('logout-anim-css')) {
            const link = document.createElement('link');
            link.id = 'logout-anim-css';
            link.rel = 'stylesheet';
            link.href = rootPrefix() + 'assets/css/logout-animation.css';
            document.head.appendChild(link);
        }

        // Create overlay if not already there
        let overlay = document.querySelector('.logout-overlay');
        if (!overlay) {
            overlay = document.createElement('div');
            overlay.className = 'logout-overlay';
            overlay.innerHTML = `
                <div class="garage-door">
                    <div class="door-slat-shine"></div>
                    <div class="workshop-sign">
                        <h2>IVHEMMS</h2>
                        <p>WORKSHOP CLOSED</p>
                    </div>
                    <div class="door-handle"></div>
                </div>
            `;
            document.body.appendChild(overlay);
        }

        // Trigger animation
        overlay.classList.add('active');
        setTimeout(() => {
            overlay.querySelector('.garage-door').classList.add('closed');
        }, 100);

        // Redirect after 3 seconds
        setTimeout(() => {
            const s = state();
            s.currentUser = null;
            saveState(s);
            
            fetch('/api/logout', { method: 'POST' }).finally(() => {
                location.href = rootPrefix() + 'login.html';
            });
        }, 3000);
    }

    function populateTopbarUser() {
        const s = state();
        const user = s.currentUser;

        if (user) {
            const nameEl = document.querySelector('.topbar-username');
            const imgEl = document.querySelector('.user-profile img');
            const roleEl = document.querySelector('.topbar-role');

            if (nameEl) nameEl.textContent = user.name || 'User';
            if (roleEl) roleEl.textContent = user.role || '';
            
            if (imgEl) {
                if (user.profile_picture) {
                    imgEl.src = user.profile_picture;
                } else {
                    imgEl.src = avatarUrl(user.name, '4361ee');
                }
            }

            // --- Role-based element visibility ---
            if (user.role !== 'admin') {
                document.querySelectorAll('.admin-only').forEach(el => {
                    el.style.setProperty('display', 'none', 'important');
                });
            }
        }

        // Always wire logout links if they exist
        document.querySelectorAll('.logout-link').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                triggerLogoutAnimation();
            });
        });
    }

    /* ──────────────────────────────────────────────
       LOGIN
    ──────────────────────────────────────────────── */
    function wireLogin() {
        // Form submission is now handled by standard HTML POST to server.py
        // We do not preventDefault() here anymore.
        const URLParams = new URL(location.href).searchParams;
        if (URLParams.get('error') === '1') {
            toast('Invalid email or password.', 'error');
        }
    }

    /* ──────────────────────────────────────────────
       REGISTER
    ──────────────────────────────────────────────── */
    function wireRegister() {
        // Form submission is now handled by standard HTML POST to server.py
        const URLParams = new URL(location.href).searchParams;
        if (URLParams.get('error') === 'mismatch') {
            toast('Passwords do not match.', 'error');
        } else if (URLParams.get('error') === 'short') {
            toast('Password must be at least 6 characters.', 'error');
        } else if (URLParams.get('error') === 'exists') {
            toast('An account with this email already exists.', 'error');
        } else if (URLParams.get('error') === 'db') {
            toast('Database connection error occurred.', 'error');
        }
    }

    /* ──────────────────────────────────────────────
       FORGOT PASSWORD
    ──────────────────────────────────────────────── */
    function wireForgotPassword() {
        const form = document.getElementById('forgotForm');
        if (!form) return;
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            const card = document.getElementById('forgotCard');
            const success = document.getElementById('forgotSuccess');
            if (card) card.style.display = 'none';
            if (success) success.style.display = 'block';
        });
    }

    /* ──────────────────────────────────────────────
       ADMIN: USER MANAGEMENT
    ──────────────────────────────────────────────── */
    function wireAdminUsers() {
        const table = document.getElementById('adminUsersTable');
        if (!table) return;

        const search = document.getElementById('adminUserSearch');
        const btnCreate = document.getElementById('btnCreateUser');
        const modalEl = document.getElementById('userModal');
        const permModalEl = document.getElementById('permModal');

        const s = state();
        s.users = (s.users || []).map(ensureUserPerms);
        saveState(s);

        const bsModal = modalEl && window.bootstrap ? new bootstrap.Modal(modalEl) : null;
        const bsPermModal = permModalEl && window.bootstrap ? new bootstrap.Modal(permModalEl) : null;

        function badgeList(perms) {
            const p = (perms || []).slice(0, 3);
            const more = (perms || []).length - p.length;
            return p.map(x => `<span class="badge badge-outline badge-outline-primary me-1">${x}</span>`).join('')
                + (more > 0 ? `<span class="badge badge-outline-primary ms-1">+${more}</span>` : '');
        }

        function render(rows) {
            const tbody = table.querySelector('.data-body-container');
            if (!tbody) return;
            tbody.innerHTML = rows.map(u => `
              <div class="data-row">
                <div class="data-cell">
                  <div class="d-flex align-items-center gap-2">
                    <img src="${avatarUrl(u.name)}" width="32" height="32" class="rounded-circle" alt="">
                    <span class="fw-bold">${u.name || '-'}</span>
                  </div>
                </div>
                <div class="data-cell data-cell-muted">${u.email || '-'}</div>
                <div class="data-cell"><span class="badge badge-outline text-white" style="border-color:rgba(255,255,255,.15)">${u.role}</span></div>
                <div class="text-end">
                  <button class="row-action-btn" data-action="edit" data-email="${encodeURIComponent(u.email)}" title="Edit"><i class="bi bi-pencil"></i></button>
                  <button class="row-action-btn danger" data-action="delete" data-email="${encodeURIComponent(u.email)}" title="Delete"><i class="bi bi-trash"></i></button>
                </div>
              </div>
            `).join('');
        }

        function refresh() {
            const q = (search?.value || '').trim().toLowerCase();
            const s2 = state();
            const users = (s2.users || []).map(ensureUserPerms);
            render(q ? users.filter(u => (u.name + u.email + u.role).toLowerCase().includes(q)) : users);
        }

        // Modal form elements
        const f = document.getElementById('userForm');
        const titleEl = document.getElementById('userModalTitle');
        const emailOriginal = document.getElementById('userFormEmailOriginal');
        const nameEl2 = document.getElementById('userFormName');
        const emailEl = document.getElementById('userFormEmail');
        const passEl = document.getElementById('userFormPassword');
        const roleEl = document.getElementById('userFormRole');

        if (btnCreate) btnCreate.addEventListener('click', () => {
            if (titleEl) titleEl.textContent = 'New User';
            if (emailOriginal) emailOriginal.value = '';
            [nameEl2, emailEl, passEl].forEach(el => { if (el) el.value = ''; });
            if (roleEl) roleEl.value = 'client';
            bsModal?.show();
        });

        if (f) f.addEventListener('submit', (e) => {
            e.preventDefault();
            const s3 = state();
            s3.users = (s3.users || []).map(ensureUserPerms);
            const original = (emailOriginal?.value || '').toLowerCase();
            const email = (emailEl?.value || '').trim();
            const role = roleEl?.value || 'client';
            const name = nameEl2?.value?.trim() || 'User';

            const exists = s3.users.some(u => u.email.toLowerCase() === email.toLowerCase() && u.email.toLowerCase() !== original);
            if (exists) { toast('Email already exists.', 'error'); return; }

            if (original) {
                const u = s3.users.find(x => x.email.toLowerCase() === original);
                if (u) { u.email = email; u.name = name; u.password = passEl?.value || u.password; u.role = role; ensureUserPerms(u); }
                toast('User updated.');
            } else {
                const nu = { email, name, password: passEl?.value || 'password', role };
                ensureUserPerms(nu);
                s3.users.push(nu);
                toast('User created.');
            }
            saveState(s3);
            bsModal?.hide();
            refresh();
        });

        // Perm modal
        const permUserEmail = document.getElementById('permUserEmail');
        const permEmailHidden = document.getElementById('permEmail');
        const permForm = document.getElementById('permForm');
        const permKeys = ['appointments', 'work_orders', 'inventory', 'finance', 'analytics', 'admin'];

        function openPerms(user) {
            if (permUserEmail) permUserEmail.textContent = user.email;
            if (permEmailHidden) permEmailHidden.value = user.email;
            const perms = new Set(user.permissions || []);
            permKeys.forEach(k => {
                const el = document.getElementById('perm_' + k);
                if (el) el.checked = perms.has(k);
            });
            bsPermModal?.show();
        }

        if (permForm) permForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const s4 = state();
            const email = (permEmailHidden?.value || '').toLowerCase();
            const u = s4.users.find(x => x.email.toLowerCase() === email);
            if (!u) { toast('User not found.', 'error'); return; }
            u.permissions = permKeys.filter(k => document.getElementById('perm_' + k)?.checked);
            saveState(s4);
            toast('Permissions saved.');
            bsPermModal?.hide();
            refresh();
        });

        table.addEventListener('click', (e) => {
            const btn = e.target.closest('[data-action]');
            if (!btn) return;
            const action = btn.dataset.action;
            const email = decodeURIComponent(btn.dataset.email || '');
            const s5 = state();
            const u = s5.users.map(ensureUserPerms).find(x => x.email === email);
            if (!u) return;
            if (action === 'edit') {
                if (titleEl) titleEl.textContent = 'Edit User';
                if (emailOriginal) emailOriginal.value = u.email;
                if (nameEl2) nameEl2.value = u.name;
                if (emailEl) emailEl.value = u.email;
                if (passEl) passEl.value = u.password || '';
                if (roleEl) roleEl.value = u.role;
                bsModal?.show();
            } else if (action === 'delete') {
                if (s5.currentUser?.email === email) { toast('Cannot delete current user.', 'error'); return; }
                s5.users = s5.users.filter(x => x.email !== email);
                saveState(s5);
                toast('User deleted.');
                refresh();
            }
        });

        if (search) search.addEventListener('input', refresh);
        refresh();
    }

    /* ──────────────────────────────────────────────
       WORK ORDERS (technician / manager)
    ──────────────────────────────────────────────── */
    function wireWorkOrders() {
        if (!location.pathname.includes('work-orders')) return;
        const table = document.getElementById('workOrdersTable');
        if (!table) return;
        const tbody = table.querySelector('tbody');
        if (!tbody) return;
        const woFilter = document.getElementById('woFilter');
        const woSearch = document.getElementById('woSearch');

        function stClass(st) {
            const map = { 
                'In Progress': 'in-progress', 
                'Completed': 'completed', 
                'Queued': 'pending', 
                'Pending': 'pending', 
                'Closed': 'completed',
                'Waiting on Parts': 'waiting-parts'
            };
            return map[st] || 'pending';
        }

        let currentTechnicians = [];
        let currentUserRole = '';
        let allWorkOrders = [];

        async function fetchWorkOrders() {
            try {
                // Determine user role from state
                const s = state();
                currentUserRole = s.currentUser?.role || '';

                const res = await fetch('/api/work-orders');
                if (res.ok) {
                    const data = await res.json();
                    if (data.work_orders && data.technicians) {
                        allWorkOrders = data.work_orders;
                        currentTechnicians = data.technicians;
                    } else {
                        allWorkOrders = data;
                    }
                    renderWorkOrders();
                } else {
                    tbody.innerHTML = '<tr><td colspan="5" class="text-center text-danger">Failed to load work orders.</td></tr>';
                }
            } catch (e) {
                console.error(e);
                tbody.innerHTML = '<tr><td colspan="5" class="text-center text-danger">Network error.</td></tr>';
            }
        }

        function renderWorkOrders() {
            if (!allWorkOrders || !allWorkOrders.length) {
                tbody.innerHTML = '<tr><td colspan="5" class="text-center text-muted py-4">No work orders found.</td></tr>';
                return;
            }

            const isManager = ['admin', 'manager', 'service-manager'].includes(currentUserRole);
            const statusFilter = woFilter?.value?.toLowerCase() || 'all';
            const searchQuery = (woSearch?.value || '').toLowerCase();

            let filtered = allWorkOrders;

            if (statusFilter !== 'all') {
                filtered = filtered.filter(wo => (wo.Status || '').toLowerCase() === statusFilter);
            }
            if (searchQuery) {
                filtered = filtered.filter(wo => 
                    String(wo.JobCard_ID).includes(searchQuery) ||
                    (wo.Make || '').toLowerCase().includes(searchQuery) ||
                    (wo.Model || '').toLowerCase().includes(searchQuery) ||
                    (wo.PlateNumber || '').toLowerCase().includes(searchQuery) ||
                    (wo.service_type || '').toLowerCase().includes(searchQuery)
                );
            }

            if (filtered.length === 0) {
                tbody.innerHTML = '<tr><td colspan="5" class="text-center text-muted py-4">No work orders match the filters.</td></tr>';
                return;
            }

            tbody.innerHTML = filtered.map(wo => {
                let techMarkup = '';
                if (isManager && (wo.Status === 'Pending' || wo.Status === 'Queued' || wo.Status === 'In Progress')) {
                    const options = currentTechnicians.map(t => 
                        `<option value="${t.user_id}" ${t.user_id === wo.Technician_ID ? 'selected' : ''}>${t.name}</option>`
                    ).join('');
                    techMarkup = `
                        <select class="form-select form-select-sm d-inline-block w-auto" onchange="window.assignTech(${wo.JobCard_ID}, this.value)">
                            <option value="">Unassigned</option>
                            ${options}
                        </select>
                    `;
                } else {
                    techMarkup = wo.TechnicianName || '<span class="text-muted">Unassigned</span>';
                }

                // Removed the extra 'Open' button column and merged it into Actions header
                // Previous HTML had 6 <td> but table only has 5 headers (WO ID, Vehicle, Service, Status, Actions)
                let statusMarkup = `<span class="status-badge ${stClass(wo.Status)}">${wo.Status}</span>`;
                if (!isManager && wo.Technician_ID && (state().currentUser?.user_id === wo.Technician_ID)) {
                    // Assigned technician can change status (except if Closed)
                    if (wo.Status !== 'Closed') {
                        const statuses = ['Pending', 'Queued', 'In Progress', 'Waiting on Parts', 'Completed'];
                        statusMarkup = `
                            <select class="form-select form-select-sm d-inline-block w-auto" style="min-width:120px;" onchange="window.updateWOStatus(${wo.JobCard_ID}, this.value)">
                                ${statuses.map(s => `<option value="${s}" ${s === wo.Status ? 'selected' : ''}>${s}</option>`).join('')}
                                <option value="Closed" disabled>Closed</option>
                            </select>
                        `;
                    }
                }

                let actionsMarkup = `<a class="btn btn-sm btn-primary" href="work-order-details.html?id=${wo.JobCard_ID}">Open</a>`;
                if (isManager) {
                   actionsMarkup = techMarkup + ' ' + actionsMarkup;
                }

                return `
                  <tr>
                    <td><span class="fw-bold">#${wo.JobCard_ID}</span></td>
                    <td>${wo.Make} ${wo.Model}<br><small class="text-muted">${wo.PlateNumber}</small></td>
                    <td>${wo.service_type || wo.ReportedIssues || '-'}</td>
                    <td>${statusMarkup}</td>
                    <td>${actionsMarkup}</td>
                  </tr>
                `;
            }).join('');
        }

        window.assignTech = async function(jobcardId, techId) {
            try {
                const res = await fetch('/api/assign-wo', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ jobcard_id: jobcardId, technician_id: techId || '' })
                });
                if (res.ok) {
                    toast('Technician assignment updated', 'success');
                    fetchWorkOrders(); // refresh
                } else {
                    const data = await res.json();
                    toast('Error: ' + (data.error || 'Failed to assign'), 'error');
                }
            } catch (e) {
                console.error(e);
                toast('Network error', 'error');
            }
        };

        window.updateWOStatus = async function(jobcardId, status) {
            try {
                const res = await fetch('/api/update-wo-status', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ jobcard_id: jobcardId, status: status })
                });
                if (res.ok) {
                    toast('Work order status updated', 'success');
                    fetchWorkOrders(); // refresh
                } else {
                    const data = await res.json();
                    toast('Error: ' + (data.error || 'Failed to update status'), 'error');
                }
            } catch (e) {
                console.error(e);
                toast('Network error', 'error');
            }
        };

        if (woFilter) woFilter.addEventListener('change', renderWorkOrders);
        if (woSearch) woSearch.addEventListener('input', renderWorkOrders);

        fetchWorkOrders();
    }

    /* ──────────────────────────────────────────────
       WORK ORDER DETAILS
    ──────────────────────────────────────────────── */
    function wireWorkOrderDetails() {
        if (!location.pathname.includes('work-order-details')) return;
        const url = new URL(location.href);
        const id = url.searchParams.get('wo') || 'WO-4592';
        const s = state();
        const wo = s.workOrders.find(w => w.id === id) || s.workOrders[0];
        if (!wo) return;

        const setEl = (sel, val) => { const el = document.querySelector(sel); if (el) el.textContent = val; };
        setEl('#wo-id', wo.id);
        setEl('#wo-vehicle', wo.vehicle);
        setEl('#wo-service', wo.service);
        setEl('#wo-status', wo.status);
        setEl('#wo-priority', wo.priority);
        setEl('#wo-license', wo.license);
        setEl('#wo-complaint', wo.complaint || '-');

        const notesContainer = document.getElementById('wo-notes');
        if (notesContainer) {
            notesContainer.innerHTML = (wo.notes || []).map(n =>
                `<div class="alert alert-secondary"><strong>${n.at}:</strong> ${n.text}</div>`
            ).join('') || '<p class="text-muted">No notes yet.</p>';
        }

        // Add note form
        const noteForm = document.getElementById('addNoteForm');
        if (noteForm) {
            noteForm.addEventListener('submit', (e) => {
                e.preventDefault();
                const txt = noteForm.querySelector('textarea')?.value?.trim();
                if (!txt) return;
                const s2 = state();
                const wo2 = s2.workOrders.find(w => w.id === id);
                if (wo2) {
                    wo2.notes = wo2.notes || [];
                    wo2.notes.push({ at: new Date().toLocaleString(), text: txt });
                    saveState(s2);
                    toast('Note added.');
                    location.reload();
                }
            });
        }

        // Complete button
        const completeBtn = document.getElementById('completeOrderBtn');
        if (completeBtn) {
            completeBtn.addEventListener('click', () => {
                const s3 = state();
                const wo3 = s3.workOrders.find(w => w.id === id);
                if (wo3) { wo3.status = 'Completed'; saveState(s3); toast('Work order marked complete!'); setTimeout(() => history.back(), 400); }
            });
        }
    }

    /* ──────────────────────────────────────────────
       APPOINTMENTS (Admin/Manager)
    ──────────────────────────────────────────────── */
    function wireAppointments() {
        if (!location.pathname.includes('manage-appointments')) return;

        const table = document.querySelector('.table.align-middle');
        if (!table) return;
        const tbody = table.querySelector('tbody');
        if (!tbody) return;

        async function fetchAppointments() {
            try {
                const res = await fetch('/api/admin/appointments');
                if (res.ok) {
                    const data = await res.json();
                    renderAppointments(data);
                } else {
                    tbody.innerHTML = '<tr><td colspan="7" class="text-center text-danger">Failed to load appointments.</td></tr>';
                }
            } catch (e) {
                console.error(e);
                tbody.innerHTML = '<tr><td colspan="7" class="text-center text-danger">Network error.</td></tr>';
            }
        }

        function renderAppointments(apps) {
            if (!apps || !apps.length) {
                tbody.innerHTML = '<tr><td colspan="7" class="text-center text-muted py-4">No appointments found.</td></tr>';
                return;
            }

            tbody.innerHTML = apps.map(a => {
                const dateObj = new Date(a.StartTime);
                const dateStr = dateObj.toLocaleDateString() + ' · ' + dateObj.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

                let statusCls = 'pending';
                if (a.Status === 'Confirmed') statusCls = 'completed';
                if (a.Status === 'Cancelled') statusCls = 'cancelled';

                let actionBtns = '';
                if (a.Status === 'Pending') {
                    actionBtns = `
                        <button class="row-action-btn success action-review" data-id="${a.Appointment_ID}" data-action="approve" title="Approve & Assign Work Order"><i class="bi bi-check-circle"></i></button>
                        <button class="row-action-btn danger action-review" data-id="${a.Appointment_ID}" data-action="reject" title="Reject"><i class="bi bi-x-circle"></i></button>
                    `;
                }

                return `
                <tr>
                    <td class="fw-bold">APT-${a.Appointment_ID}</td>
                    <td>${a.ClientName || 'Unknown Client'}<br><small class="text-muted">${a.ClientEmail || '-'}</small></td>
                    <td>${a.service_type || '-'}</td>
                    <td>${a.Make} ${a.Model} (${a.PlateNumber})</td>
                    <td>${dateStr}</td>
                    <td><span class="status-badge ${statusCls}">${a.Status}</span></td>
                    <td>${actionBtns}</td>
                </tr>
                `;
            }).join('');

            // Attach listeners
            tbody.querySelectorAll('.action-review').forEach(btn => {
                btn.addEventListener('click', async (e) => {
                    const id = btn.dataset.id;
                    const action = btn.dataset.action;
                    if (!confirm(`Are you sure you want to ${action} this appointment?`)) return;

                    btn.disabled = true;
                    try {
                        const res = await fetch('/api/appointments/review', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ appointment_id: id, action: action })
                        });
                        if (res.ok) {
                            toast(`Appointment ${action}d successfully. ${action === 'approve' ? 'Job Card generated.' : ''}`);
                            fetchAppointments();
                        } else {
                            toast('Failed to process review', 'error');
                        }
                    } catch (err) {
                        toast('Network error', 'error');
                    }
                    btn.disabled = false;
                });
            });
        }

        fetchAppointments();
    }


    /* ──────────────────────────────────────────────
       INVENTORY
    ──────────────────────────────────────────────── */
    function wireInventory() {
        const table = document.getElementById('inventoryTable');
        if (!table) return;
        const search = document.getElementById('invSearch');
        const s = state();

        function render(rows) {
            const tbody = table.querySelector('tbody');
            if (!tbody) return;
            tbody.innerHTML = rows.map(item => {
                const low = item.qty <= item.minStock;
                return `
                  <tr>
                    <td class="fw-mono">${item.id}</td>
                    <td class="fw-bold">${item.name}</td>
                    <td><span class="badge bg-secondary">${item.category}</span></td>
                    <td>${item.qty} ${item.unit} ${low ? '<span class="badge bg-danger ms-1">Low</span>' : ''}</td>
                    <td>$${item.price.toFixed(2)}</td>
                    <td>${item.minStock}</td>
                    <td>
                      <button class="row-action-btn inv-edit" data-id="${item.id}" title="Edit"><i class="bi bi-pencil"></i></button>
                      <button class="row-action-btn danger inv-del" data-id="${item.id}" title="Delete"><i class="bi bi-trash"></i></button>
                    </td>
                  </tr>
                `;
            }).join('') || `<tr><td colspan="7" class="text-center text-muted py-4">No items found.</td></tr>`;
        }

        function refresh() {
            const rows = q ? state().inventory.filter(i => (i.id + i.name + i.category).toLowerCase().includes(q)) : state().inventory;
            render(rows);
        }

        if (search) search.addEventListener('input', refresh);

        table.addEventListener('click', (e) => {
            const delBtn = e.target.closest('.inv-del');
            if (delBtn) {
                const s2 = state();
                s2.inventory = s2.inventory.filter(i => i.id !== delBtn.dataset.id);
                saveState(s2);
                toast('Item removed.');
                refresh();
            }
        });

        refresh();

        // Add item form
        const addForm = document.getElementById('addInventoryForm');
        if (addForm) {
            addForm.addEventListener('submit', (e) => {
                e.preventDefault();
                const s2 = state();
                const item = {
                    id: addForm.querySelector('#invSku')?.value || '',
                    name: addForm.querySelector('#invName')?.value || '',
                    category: addForm.querySelector('#invCategory')?.value || '',
                    qty: parseInt(addForm.querySelector('#invQty')?.value || 0),
                    unit: addForm.querySelector('#invUnit')?.value || 'Units',
                    price: parseFloat(addForm.querySelector('#invPrice')?.value || 0),
                    minStock: parseInt(addForm.querySelector('#invMinStock')?.value || 0),
                };
                s2.inventory.push(item);
                saveState(s2);
                toast('Item added to inventory.');
                const modal = bootstrap.Modal.getInstance(document.getElementById('addItemModal'));
                modal?.hide();
                refresh();
            });
        }
    }

    /* ──────────────────────────────────────────────
       INVOICES (finance/admin)
    ──────────────────────────────────────────────── */
    function wireInvoices() {
        const tbody = document.querySelector('#invoicesTable tbody');
        if (!tbody) return;

        function statusBadge(s) {
            const map = { paid: 'completed', unpaid: 'pending', partial: 'in-progress' };
            const cls = map[(s || '').toLowerCase()] || 'pending';
            return `<span class="status-badge ${cls}">${s || 'Unknown'}</span>`;
        }

        async function fetchAdminInvoices() {
            try {
                const res = await fetch('/api/admin/invoices');
                if (res.ok) {
                    const invoices = await res.json();
                    renderInvoices(invoices);
                } else {
                    tbody.innerHTML = '<tr><td colspan="7" class="text-center text-danger">Error loading invoices.</td></tr>';
                }
            } catch (e) {
                console.error(e);
                tbody.innerHTML = '<tr><td colspan="7" class="text-center text-danger">Network error.</td></tr>';
            }
        }

        function renderInvoices(rows) {
            if (!rows.length) {
                tbody.innerHTML = '<tr><td colspan="7" class="text-center text-muted py-4">No invoices found.</td></tr>';
                return;
            }
            tbody.innerHTML = rows.map(inv => {
                const date = inv.DueDate ? new Date(inv.DueDate).toLocaleDateString() : '-';
                const partsCost = parseFloat(inv.SubtotalParts || 0);
                const laborCost = parseFloat(inv.SubtotalLabor || 0);
                return `
                <tr>
                    <td class="fw-bold">INV-${inv.Invoice_ID}</td>
                    <td>${inv.ClientEmail || '-'}</td>
                    <td><span class="badge bg-secondary">Job #${inv.JobCard_ID || '-'}</span></td>
                    <td class="fw-bold">$${parseFloat(inv.Total).toFixed(2)}</td>
                    <td>${statusBadge(inv.Status)}</td>
                    <td>${date}</td>
                    <td>
                      <!-- Just visually represent actions for now -->
                      <button class="row-action-btn send-inv" title="Send Reminder"><i class="bi bi-send"></i></button>
                    </td>
                </tr>
                `;
            }).join('');

            tbody.querySelectorAll('.send-inv').forEach(btn => {
                btn.addEventListener('click', () => alert('Reminder sent to client.'));
            });
        }

        fetchAdminInvoices();
    }

    /* ──────────────────────────────────────────────
       CHATBOT
    ──────────────────────────────────────────────── */
    function wireChatbot() {
        const container = document.getElementById('chatMessages');
        const input = document.getElementById('chatInput');
        const sendBtn = document.getElementById('chatSend');
        if (!container || !sendBtn) return;

        const botReplies = [
            "I can help you with vehicle maintenance, service bookings, and more!",
            "To book a service appointment, go to the Booking section in your dashboard.",
            "Your vehicle health status is updated automatically from OBD sensor data.",
            "Need to check your service history? Head to the Service History page.",
            "For payment assistance, visit the Payments section or call our support line.",
            "I'm still learning! For complex issues, our service managers are available 24/7.",
            "You can add or manage your vehicles from the 'My Vehicles' section.",
        ];

        let replyIdx = 0;

        function addMessage(text, role) {
            const div = document.createElement('div');
            div.className = `chat-bubble ${role}`;
            div.textContent = text;
            container.appendChild(div);

            if (role === 'user') {
                // Add typing indicator
                const typing = document.createElement('div');
                typing.className = 'chat-bubble bot';
                typing.innerHTML = '<i class="bi bi-three-dots-fill" style="animation: float 1s infinite"></i>';
                container.appendChild(typing);
                container.scrollTop = container.scrollHeight;

                setTimeout(() => {
                    container.removeChild(typing);
                    addMessage(botReplies[replyIdx % botReplies.length], 'bot');
                    replyIdx++;
                }, 1000);
            }

            container.scrollTop = container.scrollHeight;
        }

        sendBtn.addEventListener('click', () => {
            const text = input.value.trim();
            if (!text) return;
            addMessage(text, 'user');
            input.value = '';
        });

        input.addEventListener('keydown', (e) => { if (e.key === 'Enter') sendBtn.click(); });

        // Quick chips
        document.querySelectorAll('.chat-quick-chip').forEach(chip => {
            chip.addEventListener('click', () => {
                addMessage(chip.textContent.trim(), 'user');
            });
        });

        // Initial bot greeting
        addMessage('Hello! I\'m IVHEMMS Assistant. How can I help you today?', 'bot');
    }

    /* ──────────────────────────────────────────────
       VEHICLE MANAGEMENT (client)
    ──────────────────────────────────────────────── */
    function wireAddVehicle() {
        // Form submission is now handled by standard HTML POST to server.py
        // We do not preventDefault() here anymore.
        const URLParams = new URL(location.href).searchParams;
        if (URLParams.get('error') === 'db') {
            toast('Database connection error occurred while adding vehicle.', 'error');
        }
    }

    /* ──────────────────────────────────────────────
       PROFILE
    ──────────────────────────────────────────────── */
    function wireProfile() {
        const form = document.getElementById('profileForm');
        const user = state().currentUser;
        if (!user) return;

        // Fill in read fields
        const setVal = (id, val) => { const el = document.getElementById(id); if (el) el.value = val || ''; };
        setVal('profileName', user.name);
        setVal('profileEmail', user.email);
        setVal('profilePhone', user.phone || '');
        setVal('profileAddress', user.address || '');

        const avatarImg = document.getElementById('profileAvatar');
        if (avatarImg) avatarImg.src = avatarUrl(user.name);

        if (!form) return;
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            const s = state();
            const u = s.users.find(x => x.email === user.email);
            if (u) {
                u.name = document.getElementById('profileName')?.value || u.name;
                u.phone = document.getElementById('profilePhone')?.value || u.phone;
                u.address = document.getElementById('profileAddress')?.value || u.address;
                s.currentUser = { ...s.currentUser, name: u.name };
                saveState(s);
                toast('Profile updated!');
            }
        });
    }

    /* ──────────────────────────────────────────────
       ADMIN VEHICLES
    ──────────────────────────────────────────────── */
    function wireAdminVehicles() {
        const table = document.getElementById('adminVehiclesTable');
        const search = document.getElementById('adminVehicleSearch');
        if (!table) return;

        let vehiclesData = [];

        function render(rows) {
            const tbody = table.querySelector('.data-body-container');
            if (!tbody) return;
            tbody.innerHTML = rows.map(v => `
              <div class="data-row">
                <div class="data-cell fw-bold">#${v.User_ID || '-'}</div>
                <div class="data-cell text-uppercase">${v.VIN || '-'}</div>
                <div class="data-cell fw-bold text-uppercase">${v.PlateNumber || '-'}</div>
                <div class="data-cell">
                  <div class="d-flex align-items-center gap-2">
                    <div class="vehicle-icon" style="width:32px;height:32px;border-radius:8px;"><i class="bi bi-car-front"></i></div>
                    <span class="fw-bold">${v.Make || ''} ${v.Model || ''}</span>
                  </div>
                </div>
                <div class="data-cell">${v.Year || '-'}</div>
                <div class="text-end">
                  <button class="row-action-btn danger" data-action="delete" data-vin="${encodeURIComponent(v.VIN)}" title="Delete"><i class="bi bi-trash"></i></button>
                </div>
              </div>
            `).join('') || `<div class="p-4 text-center text-muted">No vehicles found.</div>`;
        }

        function refresh() {
            const q = (search?.value || '').trim().toLowerCase();
            render(q ? vehiclesData.filter(v => (v.Make + v.Model + v.VIN + v.PlateNumber).toLowerCase().includes(q)) : vehiclesData);
        }

        async function fetchVehicles() {
            try {
                const res = await fetch('/api/vehicles');
                if (res.ok) {
                    vehiclesData = await res.json();
                    refresh();
                } else {
                    toast('Error fetching vehicles', 'error');
                }
            } catch (e) {
                console.error(e);
                toast('Network error', 'error');
            }
        }

        if (search) search.addEventListener('input', refresh);

        table.addEventListener('click', async (e) => {
            const btn = e.target.closest('[data-action="delete"]');
            if (!btn) return;
            const vin = decodeURIComponent(btn.dataset.vin || '');
            if (!confirm(`Delete vehicle with VIN ${vin}?`)) return;

            try {
                const res = await fetch('/api/vehicles', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ vin })
                });
                if (res.ok) {
                    toast('Vehicle deleted.');
                    fetchVehicles();
                } else {
                    toast('Failed to delete vehicle.', 'error');
                }
            } catch (err) {
                console.error(err);
                toast('Network error', 'error');
            }
        });

        fetchVehicles();
    }

    /* ──────────────────────────────────────────────
       CLIENT VEHICLES (My Garage)
    ──────────────────────────────────────────────── */
    function wireMyVehicles() {
        const container = document.getElementById('vehicleCards');
        if (!container) return;

        async function fetchMyVehicles() {
            try {
                const res = await fetch('/api/vehicles');
                if (res.ok) {
                    const vehicles = await res.json();
                    renderVehicles(vehicles);
                } else if (res.status === 403) {
                    // Session expired or not logged in - redirect to login
                    window.location.href = toRoot('login.html');
                } else {
                    toast('Error fetching vehicles', 'error');
                }
            } catch (e) {
                console.error(e);
                toast('Network error', 'error');
            }
        }

        function renderVehicles(vehicles) {
            if (vehicles.length === 0) {
                container.innerHTML = '<div class="col-12 text-center text-muted p-5">You have no vehicles in your garage. <br><br> <a href="./add-vehicle.html" class="btn btn-primary mt-3">Add your first vehicle</a></div>';
                return;
            }

            container.innerHTML = vehicles.map(v => {
                // mock health & fuel based on year/mileage for demo
                const hs = v.Year ? (v.Year % 100) : 85;
                const fuel = v.Mileage ? ((v.Mileage % 100) || 60) : 60;
                const plate = v.PlateNumber || 'N/A';
                const make = v.Make || '';
                const model = v.Model || '';
                const year = v.Year || '';
                const mileage = v.Mileage || 0;

                return `
                <div class="col-lg-6">
                    <div class="card border-0 rounded-4 overflow-hidden">
                        <div class="card-header bg-transparent pt-4 pb-3 border-0 d-flex align-items-center gap-3">
                            <div class="vehicle-icon" style="width:52px;height:52px;border-radius:14px;"><i class="bi bi-car-front" style="font-size:1.5rem;"></i></div>
                            <div>
                                <h5 class="fw-bold mb-0">${year} ${make} ${model}</h5>
                                <small class="text-muted">Plate: ${plate}</small>
                            </div>
                            <span class="status-badge completed ms-auto">Healthy</span>
                        </div>
                        <div class="card-body pt-0">
                            <div class="row g-3">
                                <div class="col-6">
                                    <div class="obd-sensor-card p-3">
                                        <div class="obd-value">${hs}%</div>
                                        <div class="obd-label">Health Score</div>
                                    </div>
                                </div>
                                <div class="col-6">
                                    <div class="obd-sensor-card p-3">
                                        <div class="obd-value" style="font-size:1.2rem;">${fuel}%</div>
                                        <div class="obd-label">Fuel Level</div>
                                    </div>
                                </div>
                            </div>
                            <div class="mt-3 d-flex flex-wrap gap-2 text-muted small">
                                <span><i class="bi bi-palette me-1"></i>${v.Color || '-'}</span>
                                <span><i class="bi bi-fuel-pump me-1"></i>Petrol</span>
                                <span><i class="bi bi-speedometer me-1"></i>${mileage} km</span>
                            </div>
                            <div class="d-flex gap-2 mt-3">
                                <a href="./booking.html?vehicle_id=${v.Vehicle_ID || ''}" class="btn btn-primary btn-sm"><i class="bi bi-calendar-plus me-1"></i> Book Service</a>
                            </div>
                        </div>
                    </div>
                </div>
                `;
            }).join('');
        }

        fetchMyVehicles();
    }


    /* ──────────────────────────────────────────────
       AI CHATBOT
    ──────────────────────────────────────────────── */
    function wireChatbot() {
        const chatMessages = document.getElementById('chatMessages');
        const chatInput = document.getElementById('chatInput');
        const chatSend = document.getElementById('chatSend');
        const quickChips = document.querySelectorAll('.chat-quick-chip');

        if (!chatMessages || !chatInput || !chatSend) return;

        let isAssistantTyping = false;
        let greetingSent = false;

        function appendMessage(text, isUser = false) {
            const msgDiv = document.createElement('div');
            msgDiv.className = `d-flex ${isUser ? 'justify-content-end' : 'justify-content-start'} mb-3 px-3`;
            
            const innerMsg = document.createElement('div');
            innerMsg.style.maxWidth = '80%';
            innerMsg.style.padding = '12px 16px';
            innerMsg.style.borderRadius = isUser ? '16px 16px 4px 16px' : '16px 16px 16px 4px';
            innerMsg.style.background = isUser ? 'var(--primary-color)' : 'var(--sidebar-hover)';
            innerMsg.style.color = isUser ? '#fff' : 'var(--text-color)';
            innerMsg.style.border = isUser ? 'none' : '1px solid var(--border-color)';
            innerMsg.innerHTML = text.replace(/\n/g, '<br>');
            
            msgDiv.appendChild(innerMsg);
            chatMessages.appendChild(msgDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }

        async function sendMessage(text) {
            if (!text.trim() || isAssistantTyping) return;
            
            isAssistantTyping = true;
            appendMessage(text, true);
            chatInput.value = '';
            
            // Show loading
            const loadingDiv = document.createElement('div');
            loadingDiv.className = 'px-3 mb-3 text-muted small fade-in';
            loadingDiv.id = 'chatLoading';
            loadingDiv.innerHTML = '<i class="bi bi-three-dots anim-pulse"></i> Assistant is thinking...';
            chatMessages.appendChild(loadingDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;

            try {
                const res = await fetch('/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ prompt: text })
                });
                
                const data = await res.json();
                document.getElementById('chatLoading')?.remove();
                
                if (data.response) {
                    appendMessage(data.response);
                } else {
                    appendMessage("Sorry, I encountered an error. Please try again.");
                }
            } catch (err) {
                document.getElementById('chatLoading')?.remove();
                appendMessage("Network error or server timeout. Please refresh and try again.");
                console.error('Chat System Error:', err);
            } finally {
                isAssistantTyping = false;
            }
        }

        chatSend.addEventListener('click', () => sendMessage(chatInput.value));
        chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') sendMessage(chatInput.value);
        });

        quickChips.forEach(chip => {
            chip.addEventListener('click', () => {
                const text = chip.innerText.trim();
                sendMessage(text);
            });
        });

        // Greeting
        if (chatMessages.children.length === 0) {
            setTimeout(() => {
                appendMessage("Hello! I'm your IVHEMMS Assistant. How can I help you today?");
            }, 500);
        }
    }

    /* ──────────────────────────────────────────────
       BOOTSTRAP
    ──────────────────────────────────────────────── */
    document.addEventListener('DOMContentLoaded', () => {
        if (!document.body.classList.contains('vms-app')) document.body.classList.add('vms-app');

        wireTheme();
        wireSidebarToggle();
        populateTopbarUser();
        addTopbarBackButton();

        wireLogin();
        wireRegister();
        wireForgotPassword();

        wireAdminUsers();
        wireAdminVehicles();
        wireWorkOrders();
        wireWorkOrderDetails();
        // wireAppointments(); // Handled by page-specific script in manage-appointments.html
        wireInventory();
        wireInvoices();
        wireChatbot();
        wireAddVehicle();
        wireMyVehicles();
        wireProfile();
    });


    // Help with chart theming
    window.getChartTheme = function() {
        const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
        const textColor = isDark ? 'rgba(255, 255, 255, 0.6)' : 'rgba(15, 23, 42, 0.6)';
        const gridColor = isDark ? 'rgba(255, 255, 255, 0.05)' : 'rgba(15, 23, 42, 0.05)';
        return { textColor, gridColor };
    };
})();
