import TodoWidget from './widgets/todoListClass.js';
import WidgetToolMenu from './components/widgetToolMenu.js';

console.log(WidgetToolMenu);
console.log(TodoWidget)

document.addEventListener('DOMContentLoaded', () => {
    // Initialisation conditionnelle basée sur les éléments présents
    
    const dashboardMenu = new WidgetToolMenu();
    


    document.querySelectorAll('.widget.todoList').forEach(widget => {
        new TodoWidget(widget);
        
    });
});