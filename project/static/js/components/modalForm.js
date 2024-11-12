document.addEventListener("DOMContentLoaded", function () {
    // Récupère tous les boutons d'ouverture de modale
    console.log('ok')
    const openModalButtons = document.querySelectorAll("[data-modal-target]");
    const closeModalButtons = document.querySelectorAll(".close-button");

    // Fonction pour ouvrir une modale spécifique
    function openModal(modal) {
        if (modal) {
            modal.style.display = "flex";
        }
    }

    // Fonction pour fermer une modale spécifique
    function closeModal(modal) {
        if (modal) {
            modal.style.display = "none";
        }
    }

    // Écouter le clic pour ouvrir la modale
    openModalButtons.forEach(button => {
        button.addEventListener("click", function (event) {
            event.preventDefault();
            const modal = document.querySelector(this.dataset.modalTarget);
            openModal(modal);
        });
    });

    // Écouter le clic pour fermer la modale
    closeModalButtons.forEach(button => {
        button.addEventListener("click", function () {
            const modal = this.closest(".modal");
            closeModal(modal);
        });
    });

    // Fermer la modale en cliquant en dehors du contenu de la modale
    window.addEventListener("click", function (event) {
        const modals = document.querySelectorAll(".modal");
        modals.forEach(modal => {
            if (event.target === modal) {
                closeModal(modal);
            }
        });
    });
});
