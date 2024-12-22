document.getElementById('upload-form').addEventListener('submit', function (event) {
    event.preventDefault();

    const form = event.target;
    const formData = new FormData(form);

    fetch('/upload-endpoint/', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        if (data.redirect_url) {
            window.location.href = data.redirect_url;
        } else {
            console.error('No redirect URL found:', data);
        }
    })
    .catch(error => {
        console.error('Error during upload:', error);
    });
});
