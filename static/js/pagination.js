/**
 * Shared Pagination Utility
 */

function renderPagination(containerId, metadata, onPageChange) {
    const container = document.getElementById(containerId);
    if (!container) return;

    if (metadata.total_pages <= 1) {
        container.innerHTML = '';
        container.style.display = 'none';
        return;
    }

    container.style.display = 'flex';
    container.className = 'pagination-container';

    let html = `
        <div class="pagination-info">
            Showing page ${metadata.current_page} of ${metadata.total_pages} (${metadata.total_items} items)
        </div>
        <button class="pagination-btn" ${metadata.has_previous ? '' : 'disabled'} id="prev-page">
            <i class="fas fa-chevron-left"></i>
        </button>
    `;

    // Simple page numbers (showing current and surrounding)
    const current = metadata.current_page;
    const total = metadata.total_pages;
    
    let start = Math.max(1, current - 2);
    let end = Math.min(total, current + 2);

    if (start > 1) html += '<span class="pagination-dots">...</span>';

    for (let i = start; i <= end; i++) {
        html += `
            <button class="pagination-btn ${i === current ? 'active' : ''}" data-page="${i}">
                ${i}
            </button>
        `;
    }

    if (end < total) html += '<span class="pagination-dots">...</span>';

    html += `
        <button class="pagination-btn" ${metadata.has_next ? '' : 'disabled'} id="next-page">
            <i class="fas fa-chevron-right"></i>
        </button>
    `;

    container.innerHTML = html;

    // Event Listeners
    const prevBtn = container.querySelector('#prev-page');
    if (prevBtn) {
        prevBtn.onclick = () => onPageChange(current - 1);
    }

    const nextBtn = container.querySelector('#next-page');
    if (nextBtn) {
        nextBtn.onclick = () => onPageChange(current + 1);
    }

    container.querySelectorAll('button[data-page]').forEach(btn => {
        btn.onclick = () => {
            const page = parseInt(btn.getAttribute('data-page'));
            if (page !== current) onPageChange(page);
        };
    });
}
