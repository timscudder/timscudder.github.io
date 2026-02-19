(function () {
    var navToggle = document.querySelector('.nav-toggle');
    var siteNav = document.getElementById('site-nav');
    if (!navToggle || !siteNav) return;

    navToggle.addEventListener('click', function (e) {
        e.stopPropagation();
        var isOpen = navToggle.getAttribute('aria-expanded') === 'true';
        navToggle.setAttribute('aria-expanded', String(!isOpen));
        siteNav.classList.toggle('nav-open', !isOpen);
    });

    // Close nav on any click outside the header
    document.addEventListener('click', function () {
        navToggle.setAttribute('aria-expanded', 'false');
        siteNav.classList.remove('nav-open');
    });
}());
