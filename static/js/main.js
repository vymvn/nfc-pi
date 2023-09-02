
const scan_button = document.getElementById("scan-button");
// const save_button = document.getElementById("save-button");
const card_name_input = document.getElementById('card-name-input')
var scan_modal_element = document.getElementById('scan-card-modal');
var save_modal_element = document.getElementById('save-card-modal');
var modals = [];

// scan_modal_element.addEventListener('shown.bs.hidden', event => {
//     scan_modal_element.dispose();
//     var save_modal = bootstrap.Modal.getInstance(save_modal_element);
//     console.log('i did reach here');
//     save_modal.show();
// })

// save_modal_element.addEventListener('shown.bs.hidden', event => {
//     save_modal_element.dispose()
// })


scan_button.addEventListener("click", () => {
    
    var scan_modal = bootstrap.Modal.getInstance(scan_modal_element);
    modals.push(scan_modal);

    $.ajax({
        url: "/scan-card",
        type: 'post',

        statusCode: {
            500: function() {
                var error_modal = new bootstrap.Modal(document.getElementById('error-modal'));
                // scan_modal.hide()
                modals.forEach(modal => {
                   modal.hide() 
                });
                error_modal.toggle()
            }
        },
        
        success: function(response) {
            scan_modal.hide();
            if (response == "ok"){
                save_modal = new bootstrap.Modal(document.getElementById('save-card-modal'));
                modals.push(save_modal);
                save_modal.toggle();
            } else if (response == "timeout") {
                timeout_modal = new bootstrap.Modal(document.getElementById('timeout-modal'));
                modals.push(timeout_modal);

                fetch("/cancel-scan", {
                    method: "POST",
                });

                timeout_modal.toggle();
            }
    
        }

      });
})


// save_button.addEventListener("click", () => {
    
//     var save_modal = bootstrap.Modal.getInstance(save_modal_element);
    // 
    // $.ajax({
    //     url: "/save-card",
    //     type: 'post',
    //
    //     data: {
    //         // name: document.getElementById("card-name-input").innerText,
    //         name: "test"
    //     },
    //
    //     statusCode: {
    //         500: function() {
    //             var error_modal = new bootstrap.Modal(document.getElementById('error-modal'));
    //             save_modal.hide()
    //             error_modal.toggle()
    //         }
    //     },
    //     
    //     success: function(response) {
    //         save_modal.hide();
    //     }
    //
    //   });
// })
