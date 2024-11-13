document.addEventListener('DOMContentLoaded', function () {
    let ImageBox = document.querySelector('.ImageBox');
    let camera = document.querySelector('.Camera');
    let Search = document.getElementById('Search');
    let SearchBtn = document.querySelector('.SearchIcon');
    let image = document.getElementById('fileUpload');
    let submit = document.querySelector('.submitBtn')
    let display = document.querySelector('.right')
    let currentInput = '';

    if (ImageBox) {
        console.log("Image Box found");
        ImageBox.style.display = 'none';
    } else {
        console.log("Image box not found");
    }

    if (camera) {
        console.log('Camera button found');
        camera.addEventListener('click', function () {
            camera.classList.toggle('active');

            if (camera.classList.contains('active')) {
                ImageBox.style.display = 'flex';
            } else {
                ImageBox.style.display = 'none';
            }
        });
    }

    if (image && submit) {
        console.log("File upload option and submit button found");

        image.onchange = function () {
            currentInput = image.files[0];
            if (currentInput) {
                if (currentInput.type === "image/jpeg" || currentInput.type === "image/png") {
                    console.log("Valid image file:", currentInput);
                    submit.addEventListener('click', async function () {
                        let { message, FurName, FurPrice, FurType, FurMaterial, FurColor, FurFeatures, FurImage, FurCount } = await sendImage(currentInput)
                        console.log(message, FurName, FurPrice, FurType, FurMaterial, FurColor, FurFeatures, FurImage, FurCount)


                        if (message != 0) {
                            display.innerHTML = " "

                            for (let i = 0; i < FurCount; i++) {

                                let itemClass = `item${i + 1}`;
                                let detailsClass = `details${i + 1}`;


                                display.innerHTML += `
                                <div class="furniture">
                                    <div class="item ${itemClass}" style="background-image: url(/${FurImage[i]});"></div>
                                    <div class="details ${detailsClass}">
                                        <h4>${FurName[i]}</h4>
                                        <ul>
                                            <li>Price: ₹${FurPrice[i]}</li>
                                            <li>${FurType[i]}</li>
                                            <li>${FurMaterial[i]}</li>
                                            <li>${FurColor[i]}</li>
                                            <li>${FurFeatures[i]}</li>
                                        </ul>
                                    </div>
                                </div>
                            `;
                            }

                            ImageBox.style.display = "none"
                        }
                        else{
                            ImageBox.style.display = "none"
                            alert("No matches found")
                            
                        }


                    })
                } else {
                    alert("Please upload a valid JPEG or PNG image.");
                }
            } else {
                alert("Please upload an image.");
            }
        };
    }

    if (SearchBtn) {
        console.log('Search Button found');
        SearchBtn.addEventListener('click', async function () {
            let searchvalue = Search.value;
            console.log("Searching for:", searchvalue);
        });
    }
});


async function sendImage(imageFile) {
    const formData = new FormData();
    formData.append('file', imageFile);

    try {
        const response = await fetch('/api/ImageSearch', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const result = await response.json();
        return {
            message: result.BackendResponse,
            FurName: result.FurName,
            FurPrice: result.FurPrice,
            FurType: result.FurType,
            FurMaterial: result.FurMaterial,
            FurColor: result.FurColor,
            FurFeatures: result.FurFeatures,
            FurImage: result.FurImage,
            FurCount: result.FurCount
        }

    } catch (error) {
        console.error('Error during fetch:', error);
        throw error;
    }
}