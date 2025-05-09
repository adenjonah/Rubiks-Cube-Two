// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Highlight the current page in the navigation
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        if (currentPath.includes(link.getAttribute('href'))) {
            link.style.textDecoration = 'underline';
            link.style.fontWeight = 'bold';
        }
    });
    
    // Add event listeners to quiz option radio buttons for better UX
    const radioButtons = document.querySelectorAll('input[type="radio"]');
    radioButtons.forEach(radio => {
        radio.addEventListener('change', function() {
            // Find all options and remove any highlighting
            const options = document.querySelectorAll('.option');
            options.forEach(option => {
                option.classList.remove('selected');
            });
            
            // Add highlighting to the selected option
            this.closest('.option').classList.add('selected');
        });
    });
}); 