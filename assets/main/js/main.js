let mycounter = 0;

function navbarBurgerDeploy() {
    mycounter += 1
    let navBurger = document.getElementById('navBurger');
    let customOffCanvas = document.getElementById('customOffCanvas');
    let x_body = document.getElementsByTagName('body')[0];

    if (mycounter % 2) {
        customOffCanvas.style.width = 'min(450px, 100%)';
        customOffCanvas.style.display = 'block';
        // customOffCanvas.style.opacity = '1';
        x_body.style.overflow = 'hidden';
    } else {
        customOffCanvas.style.width = '0px';
        customOffCanvas.style.display = 'none'
        // customOffCanvas.style.opacity = '0';
        x_body.style.overflow = 'auto';

    }
}

const accordion = document.getElementsByClassName('accordion-content-box');
for (let i = 0; i < accordion.length; i++) {
    accordion[i].addEventListener('click', function () {
        this.classList.toggle('active');
        const accordionContent = this.querySelector('.accordion-content');

        if (accordionContent.style.height) {
            accordionContent.style.height = null;
        } else {
            accordionContent.style.height = accordionContent.scrollHeight + 'px';
        }

    })
}



