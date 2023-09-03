document.addEventListener("DOMContentLoaded", function () {

    var scan_modal_element = document.getElementById('scan-card-modal');
    var info_modal_element = document.getElementById('card-info-modal');
    var scan_button = document.getElementById("scan-button");


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
                var data_html = "<p>UID: " + data.UID + "<br> Card type: " + data.card_type + "</p>";
                document.getElementById("info-modal-body").innerHTML = data_html;
                new bootstrap.Modal(info_modal_element).show();     // Create new modal instance

            })

            .catch(error => {
                console.error('Error:', error);
                throw new Error("Server error");
            });

    });
});
