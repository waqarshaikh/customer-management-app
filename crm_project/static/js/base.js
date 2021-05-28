// ------------expander menu------------
const showMenu = (toggleId, navbarId, bodyId) => {
    const toggle = document.getElementById(toggleId),
        navbar = document.getElementById(navbarId)
    bodypadding = document.getElementById(bodyId)

    if (toggle && navbar) {
        toggle.addEventListener('click', () => {
            navbar.classList.toggle('expander')

            bodypadding.classList.toggle('body-pd')
        })
    }
}
showMenu('nav-toggle', 'navbar', 'body-pd')

// -----------Active-Link------------
const linkcolor = document.querySelectorAll('.nav_link')

function colorLink() {
    linkcolor.forEach(l => l.classList.remove('active'))
    this.classList.add('active')
}
linkcolor.forEach(l => l.addEventListener('click', colorLink))
    // ----------Collapse Menu-----------
const linkCollapse = document.getElementsByClassName('collapse_link')
var i

for (i = 0; i < linkCollapse.length; i++) {
    linkCollapse[i].addEventListener('click', function() {
        const collapseMenu = this.nextElementSibling
        collapseMenu.classList.toggle('showCollapse')

        const rotate = collapseMenu.previousElementSibling
        rotate.classList.toggle('rotate')
    })
}