const Humberger = document.querySelector('.header .navBar .navList .humberger');
const MobileMenu = document.querySelector('.header .navBar .navList ul');

Humberger.addEventListener('click',() => {
    Humberger.classList.toggle('active')
    MobileMenu.classList.toggle('active')
})

document.addEventListener('scroll',()=>{
    var scroll_pos = window.scrollY;
    if(scroll_pos>250){
        header.style.backgroundColor = "#29323c"
        header.style.boxShadow = "1px 2px 5px 0px #000"
    }
    else{
        header.style.backgroundColor = "#1612128f"
        header.style.boxShadow = "none"
    }
})
