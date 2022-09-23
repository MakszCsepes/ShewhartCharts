// Visualization Constants
const POINT_RADIUS          = 5
const FILL_COLOR            = 'rgba(173,253,34,0.29)'
const VALUES_COLOR          = "rgb(245,152,35)";
const UCL_COLOR             = 'rgb(5, 2, 200)';
const CL_COLOR              = 'rgb(250,236,79)';
const LCL_COLOR             = 'rgb(255, 0, 10)';
const UCL_2_COLOR           = 'rgb(0,196,255)';
const UCL_1_COLOR           = 'rgb(42,229,161)';
const LCL_2_COLOR           = 'rgb(255,0,136)';
const LCL_1_COLOR           = 'rgb(188,245,88)';
const COMPARE_VALUES_COLOR  = "rgb(217,35,245)";
const COMPARE_UCL_COLOR     = 'rgb(187,6,71)';
const COMPARE_CL_COLOR      = 'rgb(190,174,6)';
const COMPARE_LCL_COLOR     = 'rgb(18,141,4)';

// Color pf points on chart
const BAD_POINT_COLOR   = 'red'
const GOOD_POINT_COLOR  = 'lime'
const TREND_POINT_COLOR = 'black'


const X_CHART_NAME = 'Individual X chart'
const R_CHART_NAME = 'Moving R'


// configuration of chart
const OPTIONS = {
    scales: {
        y: {
//                min: 0.65,
//                max: 0.85,
//                beginAtZero: true
        }
    },
};

function DetectBadPoints(Dataset) {
    const X = Dataset[0].data;
    const UCL_value = Dataset[2].data[0];
    const LCL_value = Dataset[3].data[0];

    for (let i = 0; i < X.length; i++) {
        if (X[i] < LCL_value || X[i] > UCL_value) {
            Dataset[0].pointBackgroundColor[i] = BAD_POINT_COLOR;
        }
    }
}

// put all the points on the plot
function PrepareDatasets(ChartData, OverlayedData) {

    X = ChartData['X'];

    let Dataset = [{
        label: ChartData['ChartLabel'],
        data: X,
        // fill: true,
        backgroundColor: FILL_COLOR,
        borderColor: VALUES_COLOR,
        pointBackgroundColor: Array(X.length).fill(GOOD_POINT_COLOR),
        pointBorderColor: Array(X.length).fill(GOOD_POINT_COLOR),
        radius: POINT_RADIUS,
    }, {
        label: "CL",
        data: Array(X.length).fill(ChartData['CL']),
        fill: false,
        borderColor: CL_COLOR,
        tension: 0.1
    }, {
        label: "UCL",
        data: Array(X.length).fill(ChartData['UCL']),
        fill: false,
        borderColor: UCL_COLOR,
        tension: 0.1
    }, {
        label: "LCL",
        data: Array(X.length).fill(ChartData['LCL']),
        fill: false,
        borderColor: LCL_COLOR,
        tension: 0.1
    }];

    if (OverlayedData.length !== 0) {
        Overlayed_X   = OverlayedData['X']
        Overlayed_UCL = OverlayedData['UCL']
        Overlayed_CL  = OverlayedData['CL']
        Overlayed_LCL = OverlayedData['LCL']

        // Overlayed X
        console.log(OverlayedData)
        Dataset.push({
            label: OverlayedData['ChartLabel'],
            data: Overlayed_X,
            // fill: true,
            backgroundColor: FILL_COLOR,
            borderColor: COMPARE_VALUES_COLOR,
            pointBackgroundColor: Array(Overlayed_X.length).fill(GOOD_POINT_COLOR),
            pointBorderColor: Array(Overlayed_X.length).fill(GOOD_POINT_COLOR),
            radius: POINT_RADIUS,
        });

        // Overlayed UCL
        Dataset.push({
            label: "Overlayed UCL",
            data: Array(Overlayed_X.length).fill(Overlayed_UCL),
            fill: false,
            borderColor: COMPARE_UCL_COLOR,
            tension: 0.1
        });

        // Overlayed CL
        Dataset.push({
            label: "Overlayed CL",
            data: Array(Overlayed_X.length).fill(Overlayed_CL),
            fill: false,
            borderColor: COMPARE_CL_COLOR,
            tension: 0.1
        });

        // Overlayed LCL
        Dataset.push({
            label: "Overlayed LCL",
            data: Array(Overlayed_X.length).fill(Overlayed_LCL),
            fill: false,
            borderColor: COMPARE_LCL_COLOR,
            tension: 0.1
        });
    }

    DetectBadPoints(Dataset);
    return Dataset
}


function DisplayCriteria(desc_js, chart_desc) {

    const criteria_block = chart_desc[0].getElementsByClassName('CRITERIA_block')
    const criteria = JSON.parse(desc_js['CRITERIA'])

    var is_stable = true;
    for (let i in criteria) {
        if (criteria[i]) {
            is_stable = false;
            criteria_id = (i).toString()

            criteria_block[0].innerHTML += "<div class='criteria_row'>" +
                                                "<span class='detected_criteria'>criteria " + criteria_id + " detected: </span>" + CRITERIA_DESC[criteria_id] +
                                           "</div>"
        }
    }


}


// Extracts chart data from json and
// inserts it into corresponding tags
function AddDesc(ctx1, desc_js) {
    const chart_holder = ctx1.parentElement
    const chart_desc = chart_holder.getElementsByClassName('chart_desc');
    const spans = chart_desc[0].getElementsByTagName('span');

    spans[0].innerText += " " + desc_js['UCL'];
    spans[1].innerText += " " + desc_js['CL' ];
    spans[2].innerText += " " + desc_js['LCL'];

    DisplayCriteria(desc_js, chart_desc);

}

function open_chart_from_object(obj) {
    const XmR_obj = {
        'ChartData_X': null,
        'ChartData_R': null,
        'Labels': null
    }

    XmR_obj['Labels'] = obj['Labels'];

    XmR_obj['ChartData_X'] = {
        'X':          obj['X']['X'],
        'CL':         obj['X']['CL'],
        'UCL':        obj['X']['UCL'],
        'LCL'       : obj['X']['LCL'],
        'CRITERIA'  : obj['X']['CRITERIA'],
        'ChartLabel': X_CHART_NAME
    }

    XmR_obj['ChartData_R'] = {
        'X':        obj['R']['X'],
        'CL':       obj['R']['CL'],
        'UCL':      obj['R']['UCL'],
        'LCL':        obj['R']['LCL'],
        'CRITERIA'  : obj['R']['CRITERIA'],
        'ChartLabel': R_CHART_NAME
    }

    return XmR_obj;
}

var MyChart1 = "";
var MyChart2 = "";


function add_histogram() {
    var canvas = document.getElementById("MyHistogram1-1");
    console.log("canvas")
    console.log(canvas)
    var data = {
        labels: [
            "20%",
            "30%",
            "40%",
            "50%",
            "60%",
            "70%",
            "80%",
            "90%",
            "100%"
        ],
        datasets: [
            {
                label: "Gauss Normal dist.",
                data: [
                    4,
                    8,
                    15,
                    30,
                    40,
                    30,
                    15,
                    8,
                    4
                ],
                backgroundColor: [
                    "rgba(255, 0, 0, 0.6)",
                    "rgba(255, 48, 0, 0.6)",
                    "rgba(255, 102, 0, 0.6)",
                    "rgba(255, 154, 0, 0.6)",
                    "rgba(255, 205, 0, 0.6)",
                    "rgba(255, 255, 0, 0.6)",
                    "rgba(203, 255, 0, 0.6)",
                    "rgba(150, 255, 0, 0.6)",
                    "rgba(94, 255, 0, 0.6)",
                    "rgba(0, 255, 0, 0.6)"
                ]
            }
        ]
    };
    var option = {
        tooltips: {
            enabled: false
        },
        legend: {
            display: false
        },
        annotation: {
            annotations: [
                {
                    type: "bar",
                    mode: "vertical",
                    // scaleID: "x-axis-0",
                    value: "70%",
                    borderColor: "black",
                    label: {
                        content: "Your Score",
                        enabled: true,
                        position: "center"
                    }
                }
            ]
        }
    };

    const config = {
        type: 'bar',
        data: data,
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        },
    };

    var myBarChart = new Chart(canvas, config);
}


function run() {
    const chart_results_count = document.getElementById('charts').querySelectorAll(`[id^="results_container"]`).length;
    console.log(chart_results_count)
    console.log(document.getElementById('charts'))

    for (let i = 0; i < chart_results_count; i++) {
        const js_data = document.getElementById('js_data' + (i+1).toString())
        // obj = {'Labels': [], 'X': {json}, 'R': {json}, 'Overlay': {obj}}
        //
        //
        let obj = JSON.parse(js_data.innerText.toString());

        document.getElementById('chart_name_span' + (i+1).toString()).innerText = obj["Name"]

        // add two 1,2-sigma options
        const sigma_buttons_block = document.getElementById('add_sigma_buts' + (i+1).toString() + "-1")
        sigma_buttons_block.innerHTML += "<button id='display_2_sigma_button'>Show 2-sigma limits</button>" +
        "<button id='display_1_sigma_button'>Show 1-sigma limits</button>"
        // add two 1,2-sigma options

        Overlayed_Chart = {
            'ChartData_X': [],
            'ChartData_R': [],
            'Labels': []
        }
        if (obj['Overlay'] !== undefined) {
            Overlayed_Chart = open_chart_from_object(obj['Overlay'])
            Overlayed_Chart['ChartData_X']['ChartLabel'] = X_CHART_NAME + " (overlayed)"
            Overlayed_Chart['ChartData_R']['ChartLabel'] = R_CHART_NAME + " (overlayed)"
        }

        XmR = open_chart_from_object(obj)
        const Labels = XmR['Labels'];
        const ChartData_X = XmR['ChartData_X']
        const ChartData_R = XmR['ChartData_R']

        // X
        const data = {
            labels: Labels,
            datasets: PrepareDatasets(ChartData_X,
                                      Overlayed_Chart['ChartData_X']),
        }
        const config1 = {
            type: 'line',
            data: data,
            options: OPTIONS
        };
        const ctx1 = document.getElementById('MyChart'  + (i+1).toString() + '-1')
        AddDesc(ctx1, ChartData_X);
        MyChart1 = new Chart(ctx1, config1);

        // R
        const data2 = {
            labels: Labels,
            datasets: PrepareDatasets(ChartData_R,
                                      Overlayed_Chart['ChartData_R'])
        }
        const config2 = {
            type: 'line',
            data: data2
        };
        const ctx2 = document.getElementById('MyChart' + (i+1).toString() + '-2')
        AddDesc(ctx2, ChartData_R);
        MyChart2 = new Chart(ctx2, config2);
    }

    document.getElementById('side_panel').style.display = "hidden";

    add_histogram();

    return 0;
}


function apply_period() {
    const years_min = parseInt(document.getElementById('years_range_min').value);
    const years_max = parseInt(document.getElementById('years_range_max').value);

    const y_min = 1990;
    const y_max = 2019;


    console.log(MyChart1.data.labels)

    console.log(years_min - y_min)

    const start = 0;
    const end = 100;
    const step = 10;
    const arrayLength = Math.floor(((end - start) / step)) + 1;
    const range = [...Array(arrayLength).keys()].map(x => (x * step) + start);


    for (let i = 0; i < MyChart1.data.datasets.length; i++) {
        MyChart1.data.datasets[i].data
    }
}

const period_button = document.getElementById('period_range_button')
period_button.addEventListener('click', apply_period)


function add_2_sigma() {
    const CL_value  = MyChart1.data.datasets[1]['data'][0]
    const UCL_value = MyChart1.data.datasets[2]['data'][0]
    const LCL_value = MyChart1.data.datasets[3]['data'][0]

    const U_sigma_2 = CL_value + 2*(UCL_value - CL_value)/3
    const L_sigma_2 = CL_value - 2*(UCL_value - CL_value)/3

    const new_datasets = MyChart1.data.datasets;
    const Labels = MyChart1.data.labels;


    X_length = MyChart1.data.datasets[0]['data'].length

    MyChart1.data.datasets.push(
        {
        label: "UCL_2",
        data: Array(X_length).fill(U_sigma_2),
        fill: false,
        borderColor: UCL_2_COLOR,
        tension: 0.1
    }
    );
    MyChart1.data.datasets.push(
        {
        label: "LCL_2",
        data: Array(X_length).fill(L_sigma_2),
        fill: false,
        borderColor: LCL_2_COLOR,
        tension: 0.1
    }
    )

    MyChart1.update();

}


function add_1_sigma() {
    const CL_value  = MyChart1.data.datasets[1]['data'][0]
    const UCL_value = MyChart1.data.datasets[2]['data'][0]
    const LCL_value = MyChart1.data.datasets[3]['data'][0]

    const U_sigma_1 = CL_value + (UCL_value - CL_value)/3
    const L_sigma_1 = CL_value - (UCL_value - CL_value)/3

    const new_datasets = MyChart1.data.datasets;
    const Labels = MyChart1.data.labels;


    X_length = MyChart1.data.datasets[0]['data'].length

    MyChart1.data.datasets.push(
        {
        label: "UCL_2",
        data: Array(X_length).fill(U_sigma_1),
        fill: false,
        borderColor: UCL_1_COLOR,
        tension: 0.1
    }
    );
    MyChart1.data.datasets.push(
        {
        label: "LCL_2",
        data: Array(X_length).fill(L_sigma_1),
        fill: false,
        borderColor: LCL_1_COLOR,
        tension: 0.1
    }
    )

    MyChart1.update();
}


