export default class WidgetToolMenu {
    constructor() {
        this.menu = document.querySelector('.menu');
        this.dashboard = document.getElementById('dashboard');
        this.csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        this.activeSubmenu = null;
        
        this.initializeEventListeners();
        const baseUrl = "http://127.0.0.1:8000/"
    }

    initializeEventListeners() {
        // Gestion des clics sur les liens du menu
        this.menu.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', (event) => this.handleMenuClick(event));
        });

        // Gestion des sous-menus au survol
        this.menu.querySelectorAll('li').forEach(item => {
            if (item.querySelector('ul')) {
                item.addEventListener('mouseenter', () => this.showSubmenu(item));
                item.addEventListener('mouseleave', () => this.hideSubmenu(item));
            }
        });

        // Fermer les sous-menus lors d'un clic en dehors
        document.addEventListener('click', (event) => {
            if (!this.menu.contains(event.target)) {
                this.closeAllSubmenus();
            }
        });
    }

    showSubmenu(item) {
        const submenu = item.querySelector('ul');
        if (submenu) {
            this.activeSubmenu = submenu;
            submenu.style.display = 'block';
            // Animation 
            submenu.style.opacity = '0';
            setTimeout(() => {
                submenu.style.opacity = '1';
            }, 10);
        }
    }

    hideSubmenu(item) {
        const submenu = item.querySelector('ul');
        if (submenu) {
            submenu.style.opacity = '0';
            setTimeout(() => {
                submenu.style.display = 'none';
            }, 200); // Durée transition CSS
            this.activeSubmenu = null;
        }
    }

    closeAllSubmenus() {
        this.menu.querySelectorAll('ul ul').forEach(submenu => {
            submenu.style.display = 'none';
            submenu.style.opacity = '0';
        });
        this.activeSubmenu = null;
    }

    async handleMenuClick(event) {
        event.preventDefault();
        const link = event.target;
        const widgetName = link.textContent.trim();

        // Vérifie si c'est un lien de widget (sous-menu)
        if (link.closest('ul').parentElement.parentElement === this.menu) {
            await this.addWidget(widgetName);
        }
    }

    async addWidget(widgetName) {
        try {
            const response = await fetch("http://127.0.0.1:8000/widgets/add-widget/", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.csrfToken
                },
                body: JSON.stringify({ widget_name: widgetName })
            });

            const data = await response.json();

            if (data.widget_html) {
                // Ajoute le widget et initialise ses fonctionnalités
                this.dashboard.insertAdjacentHTML('beforeend', data.widget_html);
                this.initializeNewWidget(data.widget_html);
            } else if (data.error) {
                this.showError(data.error);
            }
        } catch (error) {
            this.showError('Erreur lors de l\'ajout du widget');
            console.error('Erreur AJAX:', error);
        }
    }

    initializeNewWidget(widgetHtml) {
        // Initialise le nouveau widget avec la classe TodoWidget
        const newWidget = this.dashboard.lastElementChild;
        console.log(newWidget)
        if (newWidget) {
            new TodoWidget(newWidget);
        }
    }

    showError(message) {
        // Création d'une notification d'erreur
        const notification = document.createElement('div');
        notification.className = 'error-notification';
        notification.textContent = message;

        document.body.appendChild(notification);

        // Supprime la notification après 3 secondes
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }
}


window.DashboardMenu = WidgetToolMenu;