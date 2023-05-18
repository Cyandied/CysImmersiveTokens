
async function poster(url, toSend){
    try {
        const result = await fetch(`http://127.0.0.1:5000/${url}`,{
            cache:"no-store",
            method:"POST",
            headers:{
                "content-type":"application/json"
            },
            body:JSON.stringify(toSend)
        })
        const data = await result.json()
        return data
    } catch (error) {
        console.log("oopsie", error)
    }
}

async function fetcher(url){
    try {
        const result = await fetch(`http://127.0.0.1:5000/${url}`)
        const data = await result.json()
        return data
    } catch (error) {
        console.log("oopsie", error)
    }
}

const colors = document.querySelectorAll(".color-picker")
const wrapper = document.querySelector(".image-wrap")

colors.forEach(color => {
    color.addEventListener("change", async (e)=>{
        const newimage = await poster("modifyAlpha",{"color":e.target.value})
        const images = wrapper.querySelectorAll("img")
        for(const image of images){
            console.log(image)
            if(image.dataset.position == "alpha"){
                image.remove()
            }
            if(image.dataset.position == "lines"){
                const img = document.createElement("img")
                img.src = newimage["new-image"]
                img.classList.add("image")
                img.dataset.position = "alpha"
                image.remove()
                wrapper.appendChild(img)
                wrapper.appendChild(image)
            }
        }
    })
})



