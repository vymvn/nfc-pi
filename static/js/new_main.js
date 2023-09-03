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
                    // const scan_modal = new bootstrap.Modal(scan_modal_element).hide();
                    return response.json(); // parse json
                    //     // If the server operation is successful, show the new modal
                    //     scan_modal_element.modal('hide');
                } else {
                    throw new Error("Server error");
                }
            })

            .then(data => {
                console.log(data);
                // alert(JSON.stringify(data, null, 2));
                document.getElementById("info-modal-body").textContent = JSON.stringify(data, null, 4);
                console.log(JSON.stringify(data, null, 2));
                new bootstrap.Modal(info_modal_element).show();     // Create new modal instance

            })

            .catch(error => {
                console.error('Error:', error);
                throw new Error("Server error");
            });

    });
});