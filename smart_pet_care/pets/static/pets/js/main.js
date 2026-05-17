// Create animated particles
document.addEventListener('DOMContentLoaded', function () {
    const particlesDiv = document.getElementById('particles');

    if (particlesDiv) {
        for (let i = 0; i < 30; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';
            particle.style.left = Math.random() * 100 + '%';
            particle.style.animationDelay = Math.random() * 15 + 's';
            particle.style.animationDuration = (Math.random() * 10 + 10) + 's';
            particlesDiv.appendChild(particle);
        }
    }

    // Smooth scroll (only if anchors exist)
    const anchors = document.querySelectorAll('a[href^="#"]');
    anchors.forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
});

// Auto-hide Django messages safely
setTimeout(() => {
    const alerts = document.querySelectorAll('.alert');
    if (!alerts.length) return;

    alerts.forEach(alert => {
        alert.style.transition = 'opacity 0.5s';
        alert.style.opacity = '0';
        setTimeout(() => alert.remove(), 500);
    });
}, 5000);

// Simple form validation helper
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return;

    form.addEventListener('submit', function (e) {
        const inputs = form.querySelectorAll('input[required]');
        let isValid = true;

        inputs.forEach(input => {
            if (!input.value.trim()) {
                isValid = false;
                input.style.borderColor = '#f44336';
            } else {
                input.style.borderColor = 'rgba(255, 255, 255, 0.15)';
            }
        });

        if (!isValid) {
            e.preventDefault();
            alert('Please fill in all required fields');
        }
    });
}

// Initialize forms (safe even if form not present)
validateForm('login-form');
validateForm('register-form');
validateForm('reminder-form');
