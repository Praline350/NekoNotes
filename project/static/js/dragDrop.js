document.addEventListener('DOMContentLoaded', function() {
    let newX = 0, newY = 0, startX = 0, startY = 0;

    const widget = document.getElementById('widget')
    console.log('ok')

    if (widget) {
        widget.addEventListener('mousedown', mouseDown);
    } else {
        console.error('Le widget n\'a pas été trouvé');
    }

    function mouseDown(e){
        startX = e.clientX
        startY = e.clientY

        document.addEventListener('mousemove', mouseMove)
        document.addEventListener('mouseup', mouseUp)
    }

    function mouseMove(e) {
        newX = startX - e.clientX
        newY = startY - e.clientY

        startX = e.clientX;
        startY = e.clientY;

        widget.style.left = (widget.offsetLeft - newX) + 'px';  // Déplacer horizontalement
        widget.style.top = (widget.offsetTop - newY) + 'px';    // Déplacer verticalement

        console.log({newX, newY})

    }
    function mouseUp(e) {
        document.removeEventListener('mousemove', mouseMove)
    }
})