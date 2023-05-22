const images = document.querySelectorAll(".inner-image")

function forceZindex(){
    images.forEach(image =>{
        const zIndex = image.dataset.layer
        image.style.zIndex = zIndex
    })
}

window.onload = forceZindex()

function uncollapse(){
    images.forEach(part => {
        part.classList.remove("collapsed")
    })
    setTimeout(()=>{
        images.forEach(part => {
            part.classList.remove("timer400ms")
            part.classList.add("timer50ms")
        })
    },300)
}

let clicked = false

const textWrappers = document.querySelectorAll(".text-wrapper")
const tutorialButton = document.querySelectorAll(".tutorial-button")

tutorialButton.forEach(button => {
    button.addEventListener("click",e=> {
        uncollapse()
        if(e.target.nodename != "IMG"){
            const part = e.target.parentElement.dataset.part
            textWrappers.forEach(textWrapper => {
                const textPart = textWrapper.dataset.part
                textWrapper.classList.add("hidden")
                if(textPart == part){
                    textWrapper.classList.remove("hidden")
                }
            })
        }
        if(clicked){
            const part = e.target.parentElement.dataset.part
            textWrappers.forEach(textWrapper => {
                const textPart = textWrapper.dataset.part
                textWrapper.classList.add("hidden")
                if(textPart == part){
                    textWrapper.classList.remove("hidden")
                }
            })
        }
        else{clicked = !clicked}
    })
})