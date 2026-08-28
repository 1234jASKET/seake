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

const seakeGuide = document.querySelector("[data-seake-guide]");
const seakeGuideClose = document.querySelector("[data-seake-guide-close]");

if (seakeGuide && seakeGuideClose) {
    seakeGuideClose.addEventListener("click", () => {
        seakeGuide.classList.add("is-hidden");
    });
}

const pressPlanner = document.querySelector("#pressPlanner");

if (pressPlanner) {
    const pagesInput = document.querySelector("#pressPages");
    const formatInput = document.querySelector("#pressFormat");
    const colorInput = document.querySelector("#pressColor");
    const quantityInput = document.querySelector("#pressQuantity");
    const adsInput = document.querySelector("#pressAds");
    const readyTitle = document.querySelector("#pressReadyTitle");
    const finalPages = document.querySelector("#pressFinalPages");
    const blankPages = document.querySelector("#pressBlankPages");
    const sheets = document.querySelector("#pressSheets");
    const mode = document.querySelector("#pressMode");
    const adSpaces = document.querySelector("#pressAdSpaces");
    const advice = document.querySelector("#pressAdvice");
    const montageSummary = document.querySelector("#pressMontageSummary");
    const pageGrid = document.querySelector("#pressPageGrid");
    const sheetGrid = document.querySelector("#pressSheetGrid");

    const updatePressPlanner = () => {
        const requestedPages = Math.max(2, Number(pagesInput.value || 2));
        const requestedAds = Math.max(0, Number(adsInput.value || 0));
        const contentPages = requestedPages + requestedAds;
        const roundedPages = Math.ceil(contentPages / 4) * 4;
        const missingPages = roundedPages - contentPages;
        const foldedSheets = roundedPages / 4;
        const quantity = Math.max(1, Number(quantityInput.value || 1));

        finalPages.textContent = `${roundedPages} pages`;
        blankPages.textContent = missingPages === 0 ? "Aucune" : `${missingPages}`;
        sheets.textContent = `${foldedSheets} feuilles par journal`;
        mode.textContent = colorInput.value;
        adSpaces.textContent = `${requestedAds} espace${requestedAds > 1 ? "s" : ""}`;

        const pageTiles = [];
        for (let page = 1; page <= roundedPages; page += 1) {
            let type = "Complement";
            let className = "fill-page";

            if (page <= requestedPages) {
                type = "Article / contenu";
                className = "article-page";
            } else if (page <= requestedPages + requestedAds) {
                type = "Publicite";
                className = "ad-page";
            }

            pageTiles.push(
                `<div class="press-page-tile ${className}"><strong>Page ${page}</strong><span>${type}</span></div>`,
            );
        }

        pageGrid.innerHTML = pageTiles.join("");

        const sheetCards = [];
        for (let sheet = 1; sheet <= foldedSheets; sheet += 1) {
            const leftOutside = roundedPages - ((sheet - 1) * 2);
            const rightOutside = 1 + ((sheet - 1) * 2);
            const leftInside = rightOutside + 1;
            const rightInside = leftOutside - 1;

            sheetCards.push(`
                <article class="press-sheet-card">
                    <strong>Feuille ${sheet}</strong>
                    <div class="press-sheet-spread">
                        <span>Exterieur: p.${leftOutside}</span>
                        <span>Exterieur: p.${rightOutside}</span>
                        <span>Interieur: p.${leftInside}</span>
                        <span>Interieur: p.${rightInside}</span>
                    </div>
                </article>
            `);
        }

        sheetGrid.innerHTML = sheetCards.join("");
        montageSummary.textContent = `${requestedPages} page${requestedPages > 1 ? "s" : ""} de contenu + ${requestedAds} espace${requestedAds > 1 ? "s" : ""} publicitaire${requestedAds > 1 ? "s" : ""} = ${contentPages} pages utilisees. Montage final: ${roundedPages} pages.`;

        if (missingPages === 0) {
            readyTitle.textContent = "Pret pour le montage presse";
            advice.textContent = `${contentPages} pages fonctionne bien pour un journal plie. Preparez un PDF final ${formatInput.value}, ${colorInput.value}, pour environ ${quantity.toLocaleString("fr-CA")} copies.`;
        } else {
            readyTitle.textContent = "Ajouter des pages avant presse";
            advice.textContent = `Pour ${requestedPages} pages et ${requestedAds} publicite${requestedAds > 1 ? "s" : ""}, vous utilisez ${contentPages} pages. Preparez ${roundedPages} pages: ajoutez ${missingPages} page${missingPages > 1 ? "s" : ""} blanche${missingPages > 1 ? "s" : ""}, publicite${missingPages > 1 ? "s" : ""} ou annonce${missingPages > 1 ? "s" : ""} avant d'envoyer le PDF a l'imprimeur.`;
        }
    };

    pressPlanner.addEventListener("input", updatePressPlanner);
    pressPlanner.addEventListener("change", updatePressPlanner);
    updatePressPlanner();
}
