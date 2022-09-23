const FORM_NAMES = {
    'settings': 'saved_settings_json',
    'data'    : 'saved_data_json',
    'id'      : 'identifier'
}

const saving_setting = "save_enabled"
const overlay_setting = "with_overlay"


const CRITERIA_DESC = {
    1: "1 or more points lie above the UCL or below the lower LCL zone",
    2: "2 out of 3 consecutive points lie in one of the zones A",
    3: "4 out of 5 consecutive points lie in or outside zone B in zone A on one side of CL",
    4: "9 points in a row lie on the same side of CL (in zone C or outside it)",
    5: "6 or more ascending or descending dots in a row.",
    6: "14 or more alternately increasing and decreasing successive points, resembling a periodic process.",
    7: "15 consecutive points in zone C above and below CL",
    8: "8 consecutive points on both sides of CL and none in zone C."
}