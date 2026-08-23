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

const pressPlanner = document.querySelector("#pressPlanner");

if (pressPlanner) {
    const pagesInput = document.querySelector("#pressPages");
    const formatInput = document.querySelector("#pressFormat");
    const colorInput = document.querySelector("#pressColor");
    const quantityInput = document.querySelector("#pressQuantity");
    const readyTitle = document.querySelector("#pressReadyTitle");
    const finalPages = document.querySelector("#pressFinalPages");
    const blankPages = document.querySelector("#pressBlankPages");
    const sheets = document.querySelector("#pressSheets");
    const mode = document.querySelector("#pressMode");
    const advice = document.querySelector("#pressAdvice");

    const updatePressPlanner = () => {
        const requestedPages = Math.max(2, Number(pagesInput.value || 2));
        const roundedPages = Math.ceil(requestedPages / 4) * 4;
        const missingPages = roundedPages - requestedPages;
        const foldedSheets = roundedPages / 4;
        const quantity = Math.max(1, Number(quantityInput.value || 1));

        finalPages.textContent = `${roundedPages} pages`;
        blankPages.textContent = missingPages === 0 ? "Aucune" : `${missingPages}`;
        sheets.textContent = `${foldedSheets} feuilles par journal`;
        mode.textContent = colorInput.value;

        if (missingPages === 0) {
            readyTitle.textContent = "Pret pour le montage presse";
            advice.textContent = `${requestedPages} pages fonctionne bien pour un journal plie. Preparez un PDF final ${formatInput.value}, ${colorInput.value}, pour environ ${quantity.toLocaleString("fr-CA")} copies.`;
        } else {
            readyTitle.textContent = "Ajouter des pages avant presse";
            advice.textContent = `Pour ${requestedPages} pages, preparez ${roundedPages} pages. Ajoutez ${missingPages} page${missingPages > 1 ? "s" : ""} blanche${missingPages > 1 ? "s" : ""}, publicite${missingPages > 1 ? "s" : ""} ou annonce${missingPages > 1 ? "s" : ""} avant d'envoyer le PDF a l'imprimeur.`;
        }
    };

    pressPlanner.addEventListener("input", updatePressPlanner);
    pressPlanner.addEventListener("change", updatePressPlanner);
    updatePressPlanner();
}
