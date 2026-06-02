const menuToggle = document.querySelector(".menu-toggle");
const navLinks = document.querySelector(".nav-links");

if (menuToggle && navLinks) {
    menuToggle.addEventListener("click", () => {
        navLinks.classList.toggle("is-open");
    });
}

document.querySelectorAll(".copy-link").forEach((button) => {
    button.addEventListener("click", async () => {
        const link = button.dataset.copyLink;
        if (!link) {
            return;
        }

        await navigator.clipboard.writeText(link);
        button.textContent = "Lien copie";
        setTimeout(() => {
            button.textContent = "Copier le lien";
        }, 1800);
    });
});
