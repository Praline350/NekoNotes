export default class TodoWidget {
    constructor(widgetElement) {
        this.widget = widgetElement;
        this.widgetId = this.widget.dataset.widgetId;
        
        // Vérification que l'ID existe
        if (!this.widgetId) {
            throw new Error('Widget ID non trouvé');
        }
        
        // Vérification que les éléments nécessaires existent
        this.initializeElements();
        this.initializeEventListeners();
        this.updateProgressBar();
    }

    initializeElements() {
        this.taskContainer = this.widget.querySelector('.task-container');
        this.titleInput = this.widget.querySelector('.widget--title');
        this.addTaskInput = this.widget.querySelector('.addTask--title');
        this.progressBar = this.widget.querySelector('.progress');
        this.csrfToken = this.widget.querySelector('[name=csrfmiddlewaretoken]').value;

        // Vérifie que tous les éléments nécessaires sont présents
        if (!this.taskContainer || !this.titleInput || !this.addTaskInput || 
            !this.progressBar || !this.csrfToken) {
            throw new Error('Éléments manquants dans le widget');
        }
    }


    initializeEventListeners() {
        // Gestion du titre
        this.titleInput.addEventListener('keydown', (event) => this.handleTitleUpdate(event));
        this.titleInput.addEventListener('blur', (event) => this.handleTitleUpdate(event));
        
        // Gestion de l'ajout de tâche
        this.addTaskInput.addEventListener('focus', () => this.handleTaskInputFocus());
        this.addTaskInput.addEventListener('keydown', (event) => this.handleNewTask(event));
        
        // Gestion des checkboxes existantes
        this.initializeCheckboxes();

        // Gestion delete de tâche
        this.initializeDeleteBtns();
        this.initializeUpdateTask();

    }

    initializeCheckboxes() {
        const checkboxes = this.widget.querySelectorAll('.taskCheckbox');
        checkboxes.forEach(checkbox => {
            checkbox.addEventListener('click', (event) => this.handleTaskStatus(event));
        });
    }

    initializeDeleteBtns() {
        const deleteBtns = this.widget.querySelectorAll('.task--delete');
        deleteBtns.forEach(deleteBtn => {
            deleteBtn.addEventListener('click', (event) => this.deleteTask(event));
        });
    }
    
    initializeUpdateTask() {
        const taskTitles = this.widget.querySelectorAll('.task--input');
        taskTitles.forEach(taskTitle => {
            // Lors de l'appui sur "Enter"
            taskTitle.addEventListener('keydown', (event) => {
                if (event.key === 'Enter') {
                    this.handleTaskStatus(event);
                    event.target.blur();
                }
            });
        });
    }

    async handleTitleUpdate(event) {
        if (event.type === 'keydown' && event.key !== 'Enter') return;
        
        event.preventDefault();
        const newTitle = this.titleInput.value;

        if (newTitle === this.currentTitle) return;
        if (event.type === 'keydown' && event.key === 'Enter') {
            this.titleInput.blur();
        }

        try {
            const response = await fetch("http://127.0.0.1:8000/widgets/update-title/", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.csrfToken
                },
                body: JSON.stringify({
                    widget_id: this.widgetId,
                    new_title: newTitle
                })
            });

            const data = await response.json();
            if (!data.success) {

                console.error('Erreur lors de la mise à jour du titre');
            } else {
                this.currentTitle = newTitle;
            }
        } catch (error) {
            console.error('Erreur AJAX:', error);
        }
    }

    handleTaskInputFocus() {
        if (this.addTaskInput.value === "Add task") {
            this.addTaskInput.value = "";
        }
    }

    async handleNewTask(event) {
        if (event.key !== 'Enter') return;
        
        event.preventDefault();
        const newTitle = this.addTaskInput.value; 
        if (event.type === 'keydown' && event.key === 'Enter') {
            this.addTaskInput.blur();
        }

        try {
            const response = await fetch("http://127.0.0.1:8000/widgets/add-task/", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.csrfToken
                },
                body: JSON.stringify({
                    title: newTitle,
                    widget_id: this.widgetId
                })
            });

            const data = await response.json();
            if (data.task_html) {
                this.taskContainer.insertAdjacentHTML('beforeend', data.task_html);
                this.addTaskInput.value = '';
                // Réinitialiser les écouteurs d'événements pour la nouvelle tâche
                this.initializeCheckboxes();
                this.initializeDeleteBtns();
                this.updateProgressBar();
            }
        } catch (error) {
            console.error('AJAX error:', error);
        }
    }

    handleTaskStatus(event) {

        const taskDiv = event.target.closest('.task');
        this.progressBar.classList.remove('progress--start')
        const isCompleted = event.target.checked;
        const taskId = taskDiv.dataset.taskId
        const taskTitle = event.target.value;
        console.log(taskTitle)

        taskDiv.classList.toggle('completed', isCompleted);
        taskDiv.classList.toggle('pending', !isCompleted);


        try {
            fetch('http://127.0.0.1:8000/widgets/task/update/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.csrfToken
                },
                body :JSON.stringify({
                    task_id : taskId,
                    title: taskTitle,
                    status : isCompleted
                })
            })
            .then(response => response.json())
            .then(data => {
                if (!data.success) {
                    console.error('Erreur lors de la mise à jour de la tâche');
                }
            }).catch(error => console.error('Erreur AJAX:', error));
        } catch (error) {
            console.error('Erreur lors de l\'envoi de la requête:', error);
        }
        this.updateProgressBar();
    }
    deleteTask(event) {
        const taskDiv = event.target.closest('.task');
        if (!taskDiv) return;
        const taskId = taskDiv.dataset.taskId
        try {
            fetch('http://127.0.0.1:8000/widgets/task/delete/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.csrfToken
                },
                body : JSON?.stringify({
                    task_id : taskId
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    taskDiv.remove();
                } else {
                    console.error('Erreur lors de la suppression de la tâche');
                }
            }).catch(error => console.error('Erreur AJAX:', error));
        } catch (error) {
            console.error('Erreur lors de l\'envoi de la requête:', error);
        }

    }

    updateProgressBar() {
        const tasks = this.taskContainer.querySelectorAll('.task');
        const completedTasks = this.taskContainer.querySelectorAll('.task.completed');
        
        if (tasks.length === 0) {
            this.progressBar.style.width = '0%';
            return;
        }
        
        const percentage = (completedTasks.length / tasks.length) * 100;
        this.progressBar.style.width = `${percentage}%`;
    }
}


window.TodoWidget = TodoWidget;