// Main JavaScript file for SkillBridge & CareerForge

// Global functions
function closeModal() {
    // Close any modal or popup
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        modal.style.display = 'none';
    });
    
    // Close any internship details modal
    const detailModals = document.querySelectorAll('.internship-detail-modal');
    detailModals.forEach(modal => {
        modal.style.display = 'none';
    });
    
    // Remove any active states
    const activeElements = document.querySelectorAll('.modal-active');
    activeElements.forEach(element => {
        element.classList.remove('modal-active');
    });
}

function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'block';
        document.body.classList.add('modal-active');
    }
}

// Utility functions
function showLoading(element) {
    if (element) {
        element.innerHTML = '<div class="loading-spinner"><i class="fas fa-spinner fa-spin"></i> Loading...</div>';
    }
}

function hideLoading(element, content) {
    if (element) {
        element.innerHTML = content;
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltips = document.querySelectorAll('[data-tooltip]');
    tooltips.forEach(tooltip => {
        tooltip.addEventListener('mouseenter', function() {
            const text = this.getAttribute('data-tooltip');
            const tooltipElement = document.createElement('div');
            tooltipElement.className = 'tooltip-popup';
            tooltipElement.textContent = text;
            document.body.appendChild(tooltipElement);
            
            const rect = this.getBoundingClientRect();
            tooltipElement.style.left = rect.left + (rect.width / 2) - (tooltipElement.offsetWidth / 2) + 'px';
            tooltipElement.style.top = rect.top - tooltipElement.offsetHeight - 10 + 'px';
        });
        
        tooltip.addEventListener('mouseleave', function() {
            const tooltipElement = document.querySelector('.tooltip-popup');
            if (tooltipElement) {
                tooltipElement.remove();
            }
        });
    });
    
    // Initialize modal close buttons
    const closeButtons = document.querySelectorAll('.close-modal, .modal-close');
    closeButtons.forEach(button => {
        button.addEventListener('click', closeModal);
    });
    
    // Close modal on background click
    document.addEventListener('click', function(event) {
        if (event.target.classList.contains('modal')) {
            closeModal();
        }
    });
    
    // Initialize escape key to close modals
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape') {
            closeModal();
        }
    });
});

// Export functions for global use
window.closeModal = closeModal;
window.openModal = openModal;
window.showLoading = showLoading;
window.hideLoading = hideLoading;
