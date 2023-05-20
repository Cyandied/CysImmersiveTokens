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
                image.style.zIndex = zIndex
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
                image.style.zIndex = zIndex
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

colors.forEach(color => {
    color.addEventListener("change", async (e) => {
        const color = e.target.value
        const alpha = e.target.dataset.image
        const newimage = await poster("modifyAlpha",
            {
                "color": color,
                "alpha": alpha
            }
        )
        const images = wrapper.querySelectorAll(".inner-image")
        for (const image of images) {
            if (image.dataset.image == alpha) {
                image.innerHTML = ""
                const insertImage = document.createElement("img")
                insertImage.src = newimage["new-image"]
                insertImage.classList.add("image")
                image.appendChild(insertImage)
            }
        }
    })
})




