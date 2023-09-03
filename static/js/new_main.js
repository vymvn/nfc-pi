document.addEventListener("DOMContentLoaded", function () {

    var scan_modal_element = document.getElementById('scan-card-modal');
    var scan_button = document.getElementById("scan-button");

    scan_button.addEventListener("click", function () {
        // Send an HTTP POST request to the Flask server
        fetch('/scan-card', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            // body: JSON.stringify({ clicked: true }) // Send data to the server
        })
            .then(response => {
                console.log(response);
                // if (response.ok) {
                //     // If the server operation is successful, show the new modal
                //     scan_modal_element.modal('hide');
                // } else {
                //     alert("Server operation failed.");
                // }
            })

            .then(data => {
                console.log(data);
            })

            .catch(error => {
                console.error('Error:', error);
                alert("An error occurred.");
            });

    });
});
