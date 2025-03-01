// Mobile UI interactions for game application

document.addEventListener('DOMContentLoaded', function() {
    // Mobile navigation toggle
    const menuBtn = document.getElementById('menuBtn');
    const mobileNav = document.getElementById('mobileNav');
    
    if (menuBtn && mobileNav) {
        menuBtn.addEventListener('click', function() {
            mobileNav.classList.toggle('active');
        });

        // Close nav when clicking outside
        document.addEventListener('click', function(event) {
            if (!mobileNav.contains(event.target) && !menuBtn.contains(event.target)) {
                mobileNav.classList.remove('active');
            }
        });
    }

    // Handle tab switching in dashboard if present
    const tabButtons = document.querySelectorAll('.tab-button');
    if (tabButtons.length > 0) {
        tabButtons.forEach(button => {
            button.addEventListener('click', function() {
                // Remove active class from all buttons
                tabButtons.forEach(btn => btn.classList.remove('active'));
                
                // Add active class to clicked button
                this.classList.add('active');
                
                // Show corresponding content
                const tabId = this.getAttribute('data-tab');
                const tabContents = document.querySelectorAll('.tab-content');
                tabContents.forEach(content => {
                    content.style.display = 'none';
                });
                document.getElementById(tabId).style.display = 'block';
            });
        });
    }

    // Add pull-to-refresh functionality
    let touchStartY = 0;
    let touchEndY = 0;
    
    document.addEventListener('touchstart', function(e) {
        touchStartY = e.touches[0].clientY;
    }, false);
    
    document.addEventListener('touchmove', function(e) {
        touchEndY = e.touches[0].clientY;
    }, false);
    
    document.addEventListener('touchend', function(e) {
        const mainContent = document.querySelector('.main-content');
        if (mainContent && mainContent.scrollTop === 0 && touchEndY > touchStartY + 100) {
            // Show refresh indicator
            const refreshIndicator = document.createElement('div');
            refreshIndicator.className = 'refresh-indicator';
            refreshIndicator.innerHTML = '<i class="fas fa-sync-alt fa-spin"></i> Refreshing...';
            refreshIndicator.style.cssText = 'position: absolute; top: 60px; left: 0; right: 0; text-align: center; padding: 10px; background-color: rgba(0,0,0,0.1);';
            document.body.appendChild(refreshIndicator);
            
            // Simulate page refresh
            setTimeout(() => {
                location.reload();
            }, 1000);
        }
    }, false);

    // Initialize any charts if they exist
    if (typeof Chart !== 'undefined') {
        const ctx = document.getElementById('performanceChart');
        if (ctx) {
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                    datasets: [{
                        label: 'Score',
                        data: [65, 59, 80, 81, 56, 55, 72],
                        fill: false,
                        borderColor: '#3498db',
                        tension: 0.1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false
                }
            });
        }
    }
});

/**
 * Show toast notification
 * @param {string} message - Message to display
 * @param {string} type - Type of notification (success, error, warning, info)
 */
function showToast(message, type = 'info') {
    // Create toast element
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = message;
    toast.style.cssText = `
        position: fixed;
        bottom: 80px;
        left: 50%;
        transform: translateX(-50%);
        background-color: rgba(0, 0, 0, 0.8);
        color: white;
        padding: 12px 20px;
        border-radius: 4px;
        font-size: 14px;
        z-index: 1000;
        min-width: 250px;
        text-align: center;
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.2);
    `;
    
    // Add type-specific styling
    if (type === 'success') {
        toast.style.backgroundColor = 'rgba(46, 204, 113, 0.9)';
    } else if (type === 'error') {
        toast.style.backgroundColor = 'rgba(231, 76, 60, 0.9)';
    } else if (type === 'warning') {
        toast.style.backgroundColor = 'rgba(241, 196, 15, 0.9)';
    }
    
    // Add to DOM
    document.body.appendChild(toast);
    
    // Animate in
    setTimeout(() => {
        toast.style.opacity = '1';
    }, 10);
    
    // Remove after delay
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transition = 'opacity 0.3s ease';
        setTimeout(() => {
            document.body.removeChild(toast);
        }, 300);
    }, 3000);
}

/**
 * Handle form submission with validation
 * @param {HTMLFormElement} form - Form to validate and submit
 * @param {Function} callback - Callback function after successful submission
 */
function handleFormSubmit(form, callback) {
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Validate form
        const isValid = validateForm(form);
        
        if (isValid) {
            // Simulate form submission
            const formData = new FormData(form);
            const data = {};
            
            formData.forEach((value, key) => {
                data[key] = value;
            });
            
            // Show loading state
            const submitButton = form.querySelector('button[type="submit"]');
            const originalText = submitButton.textContent;
            submitButton.textContent = 'Loading...';
            submitButton.disabled = true;
            
            // Simulate API call
            setTimeout(() => {
                submitButton.textContent = originalText;
                submitButton.disabled = false;
                
                // Call the callback with the form data
                if (typeof callback === 'function') {
                    callback(data);
                }
                
                showToast('Form submitted successfully!', 'success');
                form.reset();
            }, 1500);
        }
    });
}

/**
 * Validate form fields
 * @param {HTMLFormElement} form - Form to validate
 * @return {boolean} - Whether the form is valid
 */
function validateForm(form) {
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;
    
    // Remove existing error messages
    const existingErrors = form.querySelectorAll('.form-error');
    existingErrors.forEach(error => error.remove());
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            isValid = false;
            
            // Add error message
            const errorMessage = document.createElement('div');
            errorMessage.className = 'form-error';
            errorMessage.textContent = 'This field is required';
            errorMessage.style.cssText = 'color: var(--accent-color); font-size: 12px; margin-top: 5px;';
            
            field.parentNode.appendChild(errorMessage);
            field.style.borderColor = 'var(--accent-color)';
            
            // Reset on input
            field.addEventListener('input', function() {
                this.style.borderColor = '';
                const error = this.parentNode.querySelector('.form-error');
                if (error) {
                    error.remove();
                }
            }, { once: true });
        }
        
        // Email validation
        if (field.type === 'email' && field.value.trim()) {
            const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailPattern.test(field.value)) {
                isValid = false;
                
                // Add error message
                const errorMessage = document.createElement('div');
                errorMessage.className = 'form-error';
                errorMessage.textContent = 'Please enter a valid email address';
                errorMessage.style.cssText = 'color: var(--accent-color); font-size: 12px; margin-top: 5px;';
                
                field.parentNode.appendChild(errorMessage);
                field.style.borderColor = 'var(--accent-color)';
            }
        }
    });
    
    return isValid;
}

/**
 * Load data dynamically 
 * @param {string} url - URL to fetch data from
 * @param {Function} renderFunction - Function to render the data
 */
function loadData(url, renderFunction) {
    // Show loading indicator
    const loadingIndicator = document.createElement('div');
    loadingIndicator.className = 'loading-indicator';
    loadingIndicator.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Loading...';
    loadingIndicator.style.cssText = 'text-align: center; padding: 20px;';
    
    const container = document.querySelector('.main-content');
    if (container) {
        container.appendChild(loadingIndicator);
    }
    
    // Simulate API call
    setTimeout(() => {
        // Mock data - replace with actual API call
        const mockData = {
            games: [
                { id: 1, title: 'Adventure Quest', players: 4, status: 'active' },
                { id: 2, title: 'Space Invaders', players: 2, status: 'waiting' },
                { id: 3, title: 'Puzzle Master', players: 3, status: 'completed' }
            ],
            stats: {
                gamesPlayed: 42,
                wins: 28,
                winRate: '67%',
                points: 1250
            }
        };
        
        // Remove loading indicator
        if (loadingIndicator.parentNode) {
            loadingIndicator.parentNode.removeChild(loadingIndicator);
        }
        
        // Render the data
        if (typeof renderFunction === 'function') {
            renderFunction(mockData);
        }
    }, 1500);
}

/**
 * Initialize swipe detection
 * @param {Element} element - Element to detect swipes on
 * @param {Object} callbacks - Callback functions for different swipe directions
 */
function initSwipeDetection(element, callbacks) {
    let startX, startY, endX, endY;
    const minSwipeDistance = 50;
    
    element.addEventListener('touchstart', function(e) {
        startX = e.touches[0].clientX;
        startY = e.touches[0].clientY;
    });
    
    element.addEventListener('touchend', function(e) {
        endX = e.changedTouches[0].clientX;
        endY = e.changedTouches[0].clientY;
        
        const diffX = startX - endX;
        const diffY = startY - endY;
        
        // Check if swipe is horizontal or vertical
        if (Math.abs(diffX) > Math.abs(diffY)) {
            // Horizontal swipe
            if (Math.abs(diffX) > minSwipeDistance) {
                if (diffX > 0 && callbacks.left) {
                    // Swipe left
                    callbacks.left();
                } else if (diffX < 0 && callbacks.right) {
                    // Swipe right
                    callbacks.right();
                }
            }
        } else {
            // Vertical swipe
            if (Math.abs(diffY) > minSwipeDistance) {
                if (diffY > 0 && callbacks.up) {
                    // Swipe up
                    callbacks.up();
                } else if (diffY < 0 && callbacks.down) {
                    // Swipe down
                    callbacks.down();
                }
            }
        }
    });
}