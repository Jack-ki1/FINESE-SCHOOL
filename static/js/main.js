/**
 * FINESE SCHOOL - Shared JavaScript Utilities
 * AI Assistant for Data Professionals
 */

// ── Safe Fetch Wrapper ─────────────────────────────────────────
async function safeFetch(url, options = {}) {
    try {
        const res = await fetch(url, options);
        if (!res.ok) {
            const err = await res.json().catch(() => ({error: res.statusText}));
            throw new Error(err.error || res.statusText);
        }
        return await res.json();
    } catch (err) {
        console.error(`Fetch error [${url}]:`, err);
        showToast(err.message, 'danger');
        return {error: err.message};
    }
}

// ── Toast Notifications ────────────────────────────────────────
function showToast(message, type = 'info') {
    const container = document.getElementById('toastContainer');
    if (!container) return;

    const icons = {
        success: 'bi-check-circle-fill',
        danger: 'bi-exclamation-triangle-fill',
        warning: 'bi-exclamation-circle-fill',
        info: 'bi-info-circle-fill',
    };

    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-bg-${type} border-0`;
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body"><i class="bi ${icons[type] || icons.info} me-1"></i>${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>`;
    container.appendChild(toast);

    const bsToast = new bootstrap.Toast(toast, {delay: 4000});
    bsToast.show();
    toast.addEventListener('hidden.bs.toast', () => toast.remove());
}

// ── HTML Escaping (XSS Prevention) ─────────────────────────────
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// ── Auto-resize Textarea ───────────────────────────────────────
document.addEventListener('input', function(e) {
    if (e.target.matches('[data-autoresize]')) {
        e.target.style.height = 'auto';
        e.target.style.height = e.target.scrollHeight + 'px';
    }
});

// ── Copy to Clipboard ──────────────────────────────────────────
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showToast('Copied to clipboard!', 'success');
    }).catch(() => {
        showToast('Failed to copy', 'danger');
    });
}

// ── Format File Size ───────────────────────────────────────────
function formatFileSize(bytes) {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
}

// ── Debounce ───────────────────────────────────────────────────
function debounce(func, wait = 300) {
    let timeout;
    return function(...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), wait);
    };
}

console.log('FINESE SCHOOL v1.0.0 - AI Assistant for Data Professionals loaded');
