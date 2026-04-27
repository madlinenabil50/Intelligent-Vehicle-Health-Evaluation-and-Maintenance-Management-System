/**
 * IVHEMMS Topbar Helper
 * - Exposes updateTopbarAvatar on window (required by main.js populateTopbarUser)
 * - Handles profile pictures, name display, welcomeName, admin sidebar
 * - Wires logout links as backup in case main.js wireLogout fails
 * - Restores dark/light theme preference
 */

window.updateTopbarAvatar = async function () {
    try {
        const res = await fetch('/api/session');
        if (!res.ok) return;
        const u = await res.json();

        if (u && (u.user_id || u.email)) {
            const name = (
                u.name ||
                `${u.FirstName || u.firstname || ''} ${u.LastName || u.lastname || ''}`.trim() ||
                u.email ||
                'U'
            );

            // Support both id and class selectors used across templates
            const img      = document.getElementById('userAvatar') || document.querySelector('.user-profile img');
            const nameSpan = document.getElementById('topbarName') || document.querySelector('.topbar-username');
            const welcome  = document.getElementById('welcomeName');

            if (img) {
                let fallbackBg = '4361ee'; // blue  (client / default)
                if (u.role === 'manager' || u.role === 'service-manager') fallbackBg = '8b5cf6'; // purple
                if (u.role === 'admin')   fallbackBg = '4f46e5'; // indigo
                if (u.role === 'top-manager' || u.role === 'top_manager') fallbackBg = '0ea5e9'; // sky

                if (u.ProfilePicture || u.profile_picture) {
                    img.src = u.ProfilePicture || u.profile_picture;
                } else {
                    img.src = `https://ui-avatars.com/api/?name=${encodeURIComponent(name)}&background=${fallbackBg}&color=fff`;
                }
            }

            const firstName = name.split(' ')[0] || name;
            if (nameSpan) nameSpan.textContent = firstName;
            if (welcome)  welcome.textContent  = firstName;

            // Show admin sidebar links if role is admin
            if (u.role === 'admin') {
                ['adminSidebarHeading', 'adminSidebarMenu'].forEach(id => {
                    const el = document.getElementById(id);
                    if (el) el.style.display = 'block';
                });
                document.querySelectorAll('.admin-only').forEach(el => {
                    el.style.removeProperty('display');
                });
            }
        }
    } catch (e) {
        console.warn('[TopbarHelper] updateTopbarAvatar failed:', e);
    }
};

// Also make it callable without the window prefix
const updateTopbarAvatar = window.updateTopbarAvatar;

// ── Logout wiring (backup for main.js wireLogout) ─────────────────────────────
function wireLogoutLinks() {
    document.querySelectorAll('.logout-link').forEach(link => {
        // Only attach if no listener was already added
        if (link.dataset.logoutWired) return;
        link.dataset.logoutWired = 'true';

        link.addEventListener('click', async (e) => {
            e.preventDefault();

            // Prefer main.js animation if available
            if (typeof triggerLogoutAnimation === 'function') {
                triggerLogoutAnimation();
                return;
            }

            // Fallback: direct logout
            try {
                await fetch('/api/logout', { method: 'POST' });
            } catch (_) { /* ignore */ }
            window.location.href = '/';
        });
    });
}

// ── Init on DOM ready ─────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
    window.updateTopbarAvatar();
    wireLogoutLinks();
});
