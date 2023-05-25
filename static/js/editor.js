async function poster(url, toSend) {
    try {
        const result = await fetch(`http://127.0.0.1:5000/${url}`, {
            cache: "no-store",
            method: "POST",
            headers: {
                "content-type": "application/json"
            },
            body: JSON.stringify(toSend)
        })
        const data = await result.json()
        return data
    } catch (error) {
        console.log("oopsie", error)
    }
}

async function fetcher(url) {
    try {
        const result = await fetch(`http://127.0.0.1:5000/${url}`)
        const data = await result.json()
        return data
    } catch (error) {
        console.log("oopsie", error)
    }
}

const layverControl = document.querySelectorAll(".layer-control")
const images = document.querySelectorAll(".inner-image")
const colors = document.querySelectorAll(".color-picker")

function forceZindex() {
    layverControl.forEach(layerSelected => {
        const zIndex = layerSelected.dataset.layer * 10
        const assImage = layerSelected.dataset.image
        images.forEach(image => {
            if (image.dataset.image == assImage && layerSelected.checked) {
                image.style.zIndex = -zIndex
            }
        })
    })
}

window.onload = forceZindex()

layverControl.forEach(layerSelected => {
    layerSelected.addEventListener("change", e => {
        const zIndex = e.target.dataset.layer * 10
        const assImage = e.target.dataset.image
        images.forEach(image => {
            if (image.dataset.image == assImage && layerSelected.checked) {
                image.style.zIndex = -zIndex
            }
        })
    })
})

const alphaControl = document.querySelectorAll(".is-alpha")

alphaControl.forEach(alphaController => {
    alphaController.addEventListener("change", e => {
        const isAlpha = e.target.checked
        const assImage = e.target.dataset.image
        images.forEach(image => {
            if (image.dataset.image == assImage) {
                image.classList.remove("alpha")
                if (isAlpha) {
                    image.classList.add("alpha")
                }
            }
        })
        colors.forEach(color => {
            if (color.dataset.image == assImage) {
                color.disabled = true
                if (isAlpha) {
                    color.disabled = false
                }
            }
        })

    })
})


const wrapper = document.querySelector(".images-wrap")
const loading = document.querySelector(".loading")

colors.forEach(color => {
    color.addEventListener("change", async (e) => {
        loading.classList.remove("hidden")
        const color = e.target.value
        const alpha = e.target.dataset.image
        const newimage = await poster("modifyAlpha",
            {
                "color": color,
                "alpha": alpha
            }
        )
        for (const image of images) {
            if (image.dataset.image == alpha) {
                image.innerHTML = ""
                const insertImage = document.createElement("img")
                insertImage.src = newimage["new-image"]
                insertImage.classList.add("image")
                image.appendChild(insertImage)
            }
        }
        loading.classList.add("hidden")
    })    })

const download = document.querySelector("#download")

download.addEventListener("click",async (e)=> {
    const toSend = []
    images.forEach(image =>{
        const toAppend = {}
        const temp = image.querySelector("img").src.split("/")
        toAppend["name"] = temp[temp.length-1]
        toAppend["z-index"] = +image.style.zIndex
        toSend.push(toAppend)
    })
    const downloadLink = await poster("save",toSend)
    const link = document.createElement("a")
    link.href = downloadLink.link
    link.download = "you-done-it"
    link.click()
})

const packSelector = document.querySelector("#token-pack-selector")
const tokenSelector = document.querySelector("#tokens")
const options = tokenSelector.querySelectorAll("option")

packSelector.addEventListener("change", e=> {
    options.forEach(option => {
        assPack = option.dataset.pack
        targetPack = packSelector.value
        option.classList.add("hidden")
        if(targetPack == "all" || assPack == targetPack){
            option.classList.remove("hidden")
        }
        if(assPack == "select"){
            option.selected = true
            option.classList.remove("hidden")
        }
    })
})
