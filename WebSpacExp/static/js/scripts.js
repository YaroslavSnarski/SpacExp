// Smooth Scroll Effect for Anchor Links
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("a[href^='#']").forEach(anchor => {
        anchor.addEventListener("click", function (e) {
            e.preventDefault();

            document.querySelector(this.getAttribute("href")).scrollIntoView({
                behavior: "smooth"
            });
        });
    });
});

// Example Interactive Feature
document.addEventListener("DOMContentLoaded", function () {
    const header = document.querySelector("h1");
    header.addEventListener("mouseover", function () {
        header.style.color = "#28a745"; // Change color to green
    });
    header.addEventListener("mouseout", function () {
        header.style.color = "#007bff"; // Revert to original color
    });
});
