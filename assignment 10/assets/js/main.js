// ==================================== Hamburger Menu  ====================================
const hamburger = document.getElementById('hamburger');
const mainMenu = document.getElementById('mainMenu');

hamburger.addEventListener('click', () => {
    hamburger.classList.toggle('active');
    mainMenu.classList.toggle('active');
});

// ==================================== Main Menu Active Link  =====================================
window.addEventListener('scroll', function() {
  const header = document.getElementById('header');
  if (window.scrollY > 50) {
    header.style.boxShadow = "0 4px 20px rgba(0,0,0,0.2)";
  } else {
    header.style.boxShadow = "var(--outerBoxShadow)";
  }
}); 

// ==================================== Typewriter Effect  ====================================
const typewriter = new Typed('#typewriter', {
    strings: ['Faruk. ', 'a Python Developer.', 'a Django Developer.', 'Designer.', 'a Problem Solver.'],
    typeSpeed: 75,
    backSpeed: 50,
    loop: true
});
