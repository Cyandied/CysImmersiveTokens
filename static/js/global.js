const flash = document.querySelector(".flash")

function hideFlash(){
    flash.classList.add("end-flash")
    setTimeout(()=>{
        flash.classList.add("hidden")
    },200)
}

if(flash){
    flash.addEventListener("click", e=>{
        hideFlash()
    })
    
    
    setTimeout(()=>{
        hideFlash()
    },2000)
}