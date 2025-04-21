// Track viewport dimensions
function logViewport() {
    console.log('Viewport width:', window.innerWidth);
}

// Run on resize and initial load
window.addEventListener('resize', logViewport);
document.addEventListener('DOMContentLoaded', logViewport);