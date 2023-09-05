document.addEventListener("DOMContentLoaded", function () {

    var scan_modal_element = document.getElementById('scan-card-modal');
    var info_modal_element = document.getElementById('card-info-modal');
    var scan_button = document.getElementById("scan-button");
    var save_button_submit = document.getElementById("save-button-submit");
    var card_name_input = document.getElementById("card-name-input");

    var cached_card = "";


    scan_button.addEventListener("click", function () {

        fetch('/scan-card', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
        })
            .then(response => {
                if (response.ok) {
                    bootstrap.Modal.getInstance(scan_modal_element).hide();     // Modal already open so I can just grab instance
                    return response.json(); // parse json
                } else {
                    throw new Error("Server error");
                }
            })

            .then(data => {

                if (data.scan_result) {

                    cached_card = data.scan_result;
                    document.getElementById("info-modal-body").innerText = data.scan_result;
                    new bootstrap.Modal(info_modal_element).show();     // Create new modal instance
                }

                else if (data.message) {
                    console.log(data.message);
                }

            })

            .catch(error => {
                console.error('Error:', error);
                throw new Error("Server error");
            });

    });

    save_button_submit.addEventListener("click", function () {

        fetch('/save-card', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "card_name": card_name_input.value,
                "scan_info": cached_card
            }),
        })
            .then((response) => {
                if (response.ok) {
                    window.location.reload();
                    // Successfully redirected
                    // You can handle the redirected response if needed
                } else {
                    console.error("Failed to redirect:", response.status);
                    // Handle redirection failure if necessary
                }
            })
            .catch((error) => {
                console.error("Error:", error);
                // Handle any other errors that may occur during redirection
            });

    });
});
