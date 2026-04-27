/**
 * AI Code Reviewer - Main JavaScript
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initNavigation();
    initAlerts();
    initCodeEditor();
    initAnimations();
});

/**
 * Navigation functionality
 */
function initNavigation() {
    const navToggle = document.getElementById('navToggle');
    const navMenu = document.querySelector('.nav-menu');
    
    if (navToggle && navMenu) {
        navToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
            
            // Animate hamburger
            const spans = navToggle.querySelectorAll('span');
            if (navMenu.classList.contains('active')) {
                spans[0].style.transform = 'rotate(45deg) translate(5px, 5px)';
                spans[1].style.opacity = '0';
                spans[2].style.transform = 'rotate(-45deg) translate(5px, -5px)';
            } else {
                spans[0].style.transform = 'none';
                spans[1].style.opacity = '1';
                spans[2].style.transform = 'none';
            }
        });
    }

    // Close menu when clicking outside
    document.addEventListener('click', function(e) {
        if (navMenu && !navToggle.contains(e.target) && !navMenu.contains(e.target)) {
            navMenu.classList.remove('active');
            const spans = navToggle.querySelectorAll('span');
            spans[0].style.transform = 'none';
            spans[1].style.opacity = '1';
            spans[2].style.transform = 'none';
        }
    });

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

/**
 * Alert messages functionality
 */
function initAlerts() {
    const alerts = document.querySelectorAll('.alert');
    
    alerts.forEach(alert => {
        const closeBtn = alert.querySelector('.alert-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', function() {
                alert.style.animation = 'slideOut 0.3s ease forwards';
                setTimeout(() => {
                    alert.remove();
                }, 300);
            });
        }
        
        // Auto dismiss after 5 seconds
        setTimeout(() => {
            if (alert.parentElement) {
                alert.style.animation = 'slideOut 0.3s ease forwards';
                setTimeout(() => {
                    alert.remove();
                }, 300);
            }
        }, 5000);
    });
}

/**
 * Code editor enhancements
 */
function initCodeEditor() {
    const codeEditors = document.querySelectorAll('.code-editor, .code-textarea, textarea[name="code_content"]');
    
    codeEditors.forEach(editor => {
        // Tab key support
        editor.addEventListener('keydown', function(e) {
            if (e.key === 'Tab') {
                e.preventDefault();
                const start = this.selectionStart;
                const end = this.selectionEnd;
                const value = this.value;
                
                this.value = value.substring(0, start) + '    ' + value.substring(end);
                this.selectionStart = this.selectionEnd = start + 4;
            }
        });
        
        // Auto-resize
        const resize = () => {
            this.style.height = 'auto';
            this.style.height = (this.scrollHeight) + 'px';
        };
        
        editor.addEventListener('input', resize);
        resize.call(editor);
    });
}

/**
 * Animation effects
 */
function initAnimations() {
    // Intersection Observer for scroll animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fadeInUp');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe elements with animation class
    document.querySelectorAll('.feature-card, .stat-card, .card').forEach(el => {
        observer.observe(el);
    });

    // Counter animation for stats
    const statValues = document.querySelectorAll('.stat-value');
    
    const counterObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const target = parseInt(entry.target.textContent);
                if (!isNaN(target)) {
                    animateCounter(entry.target, target);
                    counterObserver.unobserve(entry.target);
                }
            }
        });
    }, { threshold: 0.5 });

    statValues.forEach(stat => {
        counterObserver.observe(stat);
    });
}

/**
 * Animate counter from 0 to target
 */
function animateCounter(element, target) {
    const duration = 2000;
    const start = 0;
    const startTime = performance.now();
    
    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        // Easing function
        const easeOut = 1 - Math.pow(1 - progress, 3);
        const current = Math.floor(start + (target - start) * easeOut);
        
        element.textContent = current.toLocaleString();
        
        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }
    
    requestAnimationFrame(update);
}

/**
 * Copy to clipboard functionality
 */
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showNotification('Code copied to clipboard!', 'success');
    }).catch(err => {
        console.error('Failed to copy:', err);
        showNotification('Failed to copy code', 'error');
    });
}

/**
 * Show notification
 */
function showNotification(message, type = 'info') {
    const container = document.querySelector('.messages-container') || createMessageContainer();
    
    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    alert.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
        <span>${message}</span>
        <button class="alert-close">&times;</button>
    `;
    
    container.appendChild(alert);
    
    // Close button
    alert.querySelector('.alert-close').addEventListener('click', () => {
        alert.style.animation = 'slideOut 0.3s ease forwards';
        setTimeout(() => alert.remove(), 300);
    });
    
    // Auto dismiss
    setTimeout(() => {
        if (alert.parentElement) {
            alert.style.animation = 'slideOut 0.3s ease forwards';
            setTimeout(() => alert.remove(), 300);
        }
    }, 3000);
}

/**
 * Create message container if not exists
 */
function createMessageContainer() {
    const container = document.createElement('div');
    container.className = 'messages-container';
    document.body.appendChild(container);
    return container;
}

/**
 * Format code with syntax highlighting (basic)
 */
function formatCode(code, language) {
    // Basic syntax highlighting patterns
    const patterns = {
        python: [
            { pattern: /(#.*)/g, class: 'comment' },
            { pattern: /\b(def|class|if|elif|else|for|while|try|except|finally|with|import|from|as|return|yield|raise|pass|break|continue|and|or|not|in|is|lambda|global|nonlocal)\b/g, class: 'keyword' },
            { pattern: /\b(True|False|None)\b/g, class: 'boolean' },
            { pattern: /(".*?"|'.*?')/g, class: 'string' },
            { pattern: /\b(\d+)\b/g, class: 'number' },
        ],
        javascript: [
            { pattern: /(\/\/.*|\/\*[\s\S]*?\*\/)/g, class: 'comment' },
            { pattern: /\b(function|const|let|var|if|else|for|while|return|class|import|export|from|async|await|try|catch|throw|new|this)\b/g, class: 'keyword' },
            { pattern: /\b(true|false|null|undefined)\b/g, class: 'boolean' },
            { pattern: /(".*?"|'.*?'|`.*?`)/g, class: 'string' },
            { pattern: /\b(\d+)\b/g, class: 'number' },
        ]
    };
    
    let formatted = code;
    const langPatterns = patterns[language] || patterns.python;
    
    langPatterns.forEach(({ pattern, class: className }) => {
        formatted = formatted.replace(pattern, `<span class="${className}">$1</span>`);
    });
    
    return formatted;
}

/**
 * API call for code review
 */
async function submitCodeForReview(code, language) {
    try {
        const response = await fetch('/api/review/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            },
            body: JSON.stringify({ code, language })
        });
        
        if (!response.ok) {
            throw new Error('Review failed');
        }
        
        return await response.json();
    } catch (error) {
        console.error('Error submitting code:', error);
        throw error;
    }
}

/**
 * Get CSRF token
 */
function getCSRFToken() {
    const name = 'csrftoken';
    let cookieValue = null;
    
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    
    return cookieValue;
}

/**
 * Export functions for global use
 */
window.AICodeReviewer = {
    copyToClipboard,
    showNotification,
    formatCode,
    submitCodeForReview,
    getCSRFToken
};

// Add slideOut animation
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);