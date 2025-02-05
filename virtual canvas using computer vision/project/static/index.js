document.getElementById('predictionBtn').addEventListener('click', function() {
    document.getElementById('prediction').scrollIntoView({ behavior: 'smooth' });
});


const mainTextElement = document.getElementById('mainText');
const mainText = "EXPLORING VIRTUAL CANVAS USING COMPUTER VISION";
let index = 0;

function typeEffect() {
    if (index < mainText.length) {
        mainTextElement.textContent += mainText.charAt(index);
        index++;
        setTimeout(typeEffect, 100); // Adjust typing speed (milliseconds)
    }
}

typeEffect();



// Show the abstract section by default
document.getElementById('abstract').style.display = 'block';

// Add event listeners to the buttons
document.getElementById('abstractBtn').addEventListener('click', function() {
    document.getElementById('abstract').style.display = 'block';
    document.getElementById('team').style.display = 'none';
    document.getElementById('abstractBtn').classList.add('active');
    document.getElementById('teamBtn').classList.remove('active');
});

document.getElementById('teamBtn').addEventListener('click', function() {
    document.getElementById('team').style.display = 'block';
    document.getElementById('abstract').style.display = 'none';
    document.getElementById('teamBtn').classList.add('active');
    document.getElementById('abstractBtn').classList.remove('active');
});


// document.getElementById('imageInput').addEventListener('change', function(e) {
//     const file = e.target.files[0];
//     if (file) {
//         // You can add logic here to process the uploaded image
//         alert('Image uploaded: ' + file.name);
//         // Clear the input field after processing
//         document.getElementById('imageInput').value = '';
//     }
// });


document.getElementById('imageInput').addEventListener('change', function(e) {
    const file = e.target.files[0];
    document.getElementById('positive-card').style.display="none";
    document.getElementById('negative-card').style.display="none"
    if (file) {
        const reader = new FileReader();
        reader.onload = function(event) {
            const imageUrl = event.target.result;

            // Remove previous uploaded image, if any
            const existingImage = document.querySelector('.uploaded-image');
            if (existingImage) {
                existingImage.remove();
            }

            // Create and add new image
            const imageElement = document.createElement('img');
            imageElement.src = imageUrl;
            imageElement.classList.add('uploaded-image');
            document.getElementById('uploded-img').appendChild(imageElement);
        };
        reader.readAsDataURL(file);
    }
});






// image show


