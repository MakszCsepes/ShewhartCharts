
function place_a_card_from_db(obj, i) {
    const X_obj = 'X'
    const settings = {}
    settings[saving_setting] = false

    const reference = '/display_db_card'

    const html = "<td class='chart_icon'></td>" +
                 "<td class='Chart_Name'>" + obj[X_obj]['Name'] + "</td>" +
                 "<td class='UCL'>"        + obj[X_obj]['UCL']  + "</td>" +
                 "<td class='CL' >"        + obj[X_obj]['CL']   + "</td>" +
                 "<td class='LCL'>"        + obj[X_obj]['LCL']  + "</td>" +
                 "<td class='LCL'>"        +
                 "<form method='post' action=" + reference + ">" +
                    "<input name='" + FORM_NAMES['settings'] +"' type='hidden' value='" + JSON.stringify(settings) +"'>" +
                    "<input name='" + FORM_NAMES['data']     +"' type='hidden' value='" + JSON.stringify(obj)      +"'>" +
                    "<label for='submit_display" + i + "'></label>" +
                    "<input type='submit' id='submit_display" + i + "'>" +
                 "</form>" +
                 "</td>";
    return html;
}

function display_cards_from_db() {
    const js_data = document.getElementById('db_cards')
    const obj     = JSON.parse(js_data.innerText);

    const cards_container = document.getElementById('existing_cards')
    let html = "";
    html = "<table class='db_res_table'>" +
            "<thead>" +
                "<tr>" +
                    "<th>F</th>" +
                    "<th>Chart Name</th>" +
                    "<th>UCL</th>" +
                    "<th>CL</th>" +
                    "<th>LCL</th>" +
                    "<th>@</th>" +
                "</tr>" +
            "</thead>" +
            "<tbody id='db_res_table_body'>"

    for (let i = 0; i < obj.length; i++) {
        html += "<tr class='card_to_display'>";
        html += place_a_card_from_db(obj[i], i)
        html += "</tr>";
    }

    html += "</tbody>" +
            "</table>"

    cards_container.innerHTML += html;
}

display_cards_from_db();


function add_icons() {
    const res_tbl_body = document.getElementById('db_res_table_body')
    var arr = [].slice.call(res_tbl_body.children);

    var td_arr = [].slice.call(arr[0].getElementsByTagName('td'))
    td_arr[0].innerHTML += "<img src='/static/icons/flag_ukr.png'>"

    td_arr = [].slice.call(arr[1].getElementsByTagName('td'))
    td_arr[0].innerHTML += "<img src='/static/icons/flag_chn.png'>"

    td_arr = [].slice.call(arr[2].getElementsByTagName('td'))
    td_arr[0].innerHTML += "<img src='/static/icons/flag_kuw.png'>"

    td_arr = [].slice.call(arr[3].getElementsByTagName('td'))
    td_arr[0].innerHTML += "<img src='/static/icons/flag_rus.png'>"

    td_arr = [].slice.call(arr[4].getElementsByTagName('td'))
    td_arr[0].innerHTML += "<img src='/static/icons/flag_lat.png'>"

    td_arr = [].slice.call(arr[5].getElementsByTagName('td'))
    td_arr[0].innerHTML += "<img src='/static/icons/flag_usa.png'>"
}

add_icons()