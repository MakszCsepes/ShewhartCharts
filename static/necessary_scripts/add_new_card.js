



function ADD_NEW_AddEventListeners() {

    const AddNew_button = document.getElementById('add_new_chart_button')
    const AddNew_Cancel_button = document.getElementById("AddNew_Cancel")
    const Form = document.getElementById("AddNewChartForm")

    // Add New Chart event
    if (AddNew_button) {
        AddNew_button.addEventListener('click', function () {
            Form.style.display = "block";
            AddNew_Cancel_button.style.display = "block";
        })
    }

    // Cancel Adding New Chart event
    if (AddNew_Cancel_button) {
        AddNew_Cancel_button.addEventListener('click', function () {
            AddNew_Cancel_button.style.display = "none";
            Form.style.display = "none";
        })
    }

    // before submiting a form
    if (Form) {
        Form.onsubmit = function () {
            Form.elements["saved_data_json"].value = document.getElementById('charts_list').innerText
            alert("sumbit")
        };
    }

}

ADD_NEW_AddEventListeners()




// ========= COMPARE (OVERLAY) =========



function OVERLAY_AddEventListeners() {
    const chart_results_count = document.getElementById('charts').childElementCount;

    for (let i = 0; i < chart_results_count; i++) {
        const Overlay_button = document.getElementById('Overlay_button' + (i+1).toString())
        const CancelOverlay_button = document.getElementById('Overlay_Cancel' + (i+1).toString())
        const overlay_form = document.getElementById('OverlayChartForm' + (i+1).toString())

        if (Overlay_button) {
            Overlay_button.addEventListener('click', function () {
                overlay_form.style.display = "block";
                CancelOverlay_button.style.display = "block";
            });
        }

        if (CancelOverlay_button) {
            CancelOverlay_button.addEventListener('click', function () {
                overlay_form.style.display = "none";
                CancelOverlay_button.style.display = "none";
            })
        }

        // before submiting a form
        if (overlay_form) {
            overlay_form.onsubmit = function () {
                overlay_form.elements['saved_data_json'].value = document.getElementById('charts_list').innerText
                alert("sumbit")
            };
        }


        const saving_form = document.getElementById('save_to_db_form' + (i+1).toString())
         // before submiting a form
        if (saving_form) {
            saving_form.onsubmit = function () {
                saving_form.elements['saved_data_json'].value = document.getElementById('charts_list').innerText
                alert("sumbit")
            };
        }
    }
}

OVERLAY_AddEventListeners()

