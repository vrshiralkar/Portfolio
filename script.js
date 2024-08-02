window.onload = function () {
    const portfolioTitle = document.querySelector('.portfolio-title');
    const introDetails = document.querySelector('.intro-details');

    setTimeout(() => {
        portfolioTitle.style.opacity = '1';
    }, 100); // Initial fade-in of "PORTFOLIO"

    setTimeout(() => {
        portfolioTitle.style.opacity = '0'; // Gradual fade-out "PORTFOLIO"
    }, 3000); // After 2 seconds, start fading out "PORTFOLIO"

    setTimeout(() => {
        portfolioTitle.style.display = 'none'; // Hide "PORTFOLIO" after fade-out
        introDetails.style.display = 'block';  // Show the name/position/resume section
        introDetails.style.opacity = '1';      // Fade-in the name/position/resume section
    }, 3000); // 2 seconds after starting fade-out, show the intro details
};
