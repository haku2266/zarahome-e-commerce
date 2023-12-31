let counter = 0;

function navbarBurgerDeploy() {
    let navBurger = document.getElementById('navBurger');
    let customOffCanvas = document.getElementById('customOffCanvas');
    let wrapper = document.getElementById('customOffCanvasWrapper');
    let x_body = document.getElementsByTagName('body')[0];
    let cart = document.getElementById('navCart')

    if (counter % 2) {
        customOffCanvas.style.width = 'min(450px, 100%)';
        wrapper.style.visibility = 'visible';
        wrapper.style.opacity = '1';
        x_body.style.overflow = 'hidden';
    } else {
        customOffCanvas.style.width = '0px';
        wrapper.style.visibility = 'hidden'
        wrapper.style.opacity = '0';
        x_body.style.overflow = 'auto';

    }
    counter += 1
}



