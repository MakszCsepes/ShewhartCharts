const settings_block = document.getElementById("json_settings")

function apply_settings() {
    const settings = JSON.parse(settings_block.innerText)

    const chart_results_count = document.getElementById('charts').childElementCount;
    for (let i = 0; i < chart_results_count; i++) {
        saving_form = document.getElementById('save_to_db_form' + (i+1).toString())
        if (settings[saving_setting] === false) {
            saving_form.style.display = "none";
        } else {
            saving_form.elements['saved_data_json'].value = document.getElementById('charts_list').innerText
        }
    }
}

apply_settings();