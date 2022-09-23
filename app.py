import os
import json

from flask import Flask, render_template, request, flash, redirect, url_for
# from flask_mail import Mail
from werkzeug.utils import secure_filename

import Database_actions
import config.config as config
from Card import CalculateData, SaveCard
from ReadDataFromFile import GetCSVData, PrepareData_FromFile, is_file_allowed

from constants import SAVING_CHART_RETURN_CODES, DISPLAY_CHART_FORM_NAMES

# ========== SAVE FILE ==========
FILE_SAVED      = 1
NO_FILE         = 0
FILENAME_EMPTY  = -1
INCORRECT_FILE  = -2


def save_file(request):
    if 'file' not in request.files:
        flash('No file part')
        return NO_FILE

    file = request.files['file']
    if file.filename == '':
        print("app.py | save_file(): no selected files")
        return FILENAME_EMPTY
    if file and is_file_allowed(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return FILE_SAVED
    else:
        print("app.py | save_file(): " + file.filename + " is not allowed file")
        return INCORRECT_FILE


def remove_file(filename):
    uploads_dir_path = os.path.abspath(os.getcwd()) + "/" + app.config['UPLOAD_FOLDER']

    if filename in os.listdir(uploads_dir_path):
        os.remove(uploads_dir_path + "/" + filename)

        print("app.py | remove_file(): file removed")
    else:
        print("app.py | remove_file(): no file to remove")

# ===============================


app = Flask(__name__)


# display chart
def display(json_data_list, display_settings = {'multiple': False}):

    return render_template("chart_results.html",
                           chart_list = json_data_list,
                           settings   = json.dumps(display_settings))


def get_labels(subset_to_read) -> []:
    db_subset = json.loads(subset_to_read)
    integer_subset = {}
    for key in db_subset:
        integer_key = int(float(key))
        integer_subset[integer_key] = db_subset[key]
    db_subset = integer_subset

    labels = list(db_subset.keys())

    return labels


def initialise_card_from_db(query_res, subset_to_read) -> {}:
    db_subset = json.loads(subset_to_read)
    integer_subset = {}
    # change json keys from `str` to `int`
    for key in db_subset:
        integer_key = int(float(key))
        integer_subset[integer_key] = db_subset[key]
    db_subset = integer_subset

    X_obj              = {}
    X_obj['X']         = list(db_subset.values())
    X_obj['UCL']       = query_res[2]
    X_obj['CL']        = query_res[3]
    X_obj['LCL']       = query_res[4]
    X_obj['Name']      = query_res[5]
    X_obj['is_stable'] = query_res[6]
    X_obj['CRITERIA']  = query_res[7]
    X_obj['parent_id'] = query_res[8]

    return X_obj


def get_cards_from_db() -> []:
    TABLE_NAME = "Card"
    CONDITION = "where parent_id is not null LIMIT 6"
    CONDITION = "where card_id in (4, 6, 8, 10, 12, 28)"
    command = "select * from " + TABLE_NAME + " " + CONDITION
    res = Database_actions.execute_SQL(command)

    db_cards = []
    for i in res:
        X_obj = initialise_card_from_db(i, i[1])

        # query for parent card
        CONDITION = "where card_id=" + str(X_obj['parent_id'])
        command = "select * from " + TABLE_NAME + " " + CONDITION
        res = Database_actions.execute_SQL(command)[0]

        mR_obj = initialise_card_from_db(res, res[1])

        labels = get_labels(i[1])

        XmR_obj = {'X'     : X_obj,
                   'R'     : mR_obj,
                   'Labels': labels}

        db_cards.append(XmR_obj)

    return db_cards

def get_all_cards_from_db():
    TABLE_NAME = "Card"
    CONDITION = "where parent_id is not null"
    command = "select * from " + TABLE_NAME + " " + CONDITION
    res = Database_actions.execute_SQL(command)

    db_cards = []
    for i in res:
        X_obj = initialise_card_from_db(i, i[1])

        # query for parent card
        CONDITION = "where card_id=" + str(X_obj['parent_id'])
        command = "select * from " + TABLE_NAME + " " + CONDITION
        res = Database_actions.execute_SQL(command)[0]

        mR_obj = initialise_card_from_db(res, res[1])

        labels = get_labels(i[1])

        XmR_obj = {'X': X_obj,
                   'R': mR_obj,
                   'Labels': labels}

        db_cards.append(XmR_obj)

    return db_cards

@app.route("/")
def home():
    return render_template("start.html")

@app.route("/table")
def get_table():
    db_cards = get_all_cards_from_db()

    return render_template("table.html", chart_list=json.dumps(db_cards, indent=1))

@app.route("/register")
def register():
    return render_template("/registration.html")

@app.route("/login", methods=["POST"])
def authorization():
    return redirect("/begin")

@app.route("/display_user_charts")
def user_charts():
    return render_template("user_charts.html")


@app.route("/begin")
def index():
    db_cards = get_cards_from_db()

    return render_template("index.html", js_data=json.dumps(db_cards, indent=1))


@app.route("/chart_classifications")
def classification():
    return render_template("chart_classifications.html")


@app.route("/classification/individual")
def get_individual():
    return render_template("individual_X.html")

@app.route("/display_db_card", methods=["GET", "POST"])
def display_db_card():
    if request.method == 'POST':
        data     = request.form[DISPLAY_CHART_FORM_NAMES['data']]
        settings = request.form[DISPLAY_CHART_FORM_NAMES['settings']]

        settings = json.loads(settings)
        settings['multiple'] = False

        json_data         = json.loads(data)
        json_data['Name'] = json_data['X']['Name']
        return display(json_data_list   = [json.dumps(json_data)],
                       display_settings = settings)

    return redirect("/")


@app.route("/proceed", methods=["POST", "GET"])
def get_file():
    if request.method == 'POST':
        code = save_file(request)

        # file saving failed
        if code in [NO_FILE, FILENAME_EMPTY, INCORRECT_FILE]:
            print("file saving failed; code:" + str(code))
            return redirect(request.url)

        # file saving succeed
        print("app.py | get_file(): file saving succeed; code:" + str(code))
        filename  = secure_filename(request.files['file'].filename)
        card_name = request.form['name']

        return redirect(url_for('get_file', filename=filename, name=card_name))

    if request.method == 'GET':
        filename    = request.args.get('filename', "")
        card_name   = request.args.get('name', "")
        if card_name == "":
            card_name = filename

        # Read data from a file (i.e. .xlsx or .csv)
        RawData = PrepareData_FromFile(app.config["UPLOAD_FOLDER"] + '/' + filename)

        # Delete file from server
        remove_file(filename)

        # Prepare card data for js
        json_data           = CalculateData(RawData['X'], card_name)
        json_data['Labels'] = RawData['Labels']
        json_data['Name']   = card_name

        return display(json_data_list=[json.dumps(json_data)])


@app.route("/save", methods=["POST"])
def save_to_db():
    json_data = request.form['saved_data_json']
    id        = int(request.form[DISPLAY_CHART_FORM_NAMES['id']])

    json_to_save = json.loads(json_data)[id-1]

    res = SaveCard(json_to_save)
    # todo analyse res

    return redirect("/begin")

    json_data = json.loads(json_data)
    return display(json_data_list   = json_data,
                   display_settings = {'save_enabled': False})


@app.route("/overlay", methods=["POST"])
def overlay():
    if request.method == 'POST':
        # list [] of all chart wrappers
        data     = request.form[DISPLAY_CHART_FORM_NAMES['data']]
        data     = json.loads(data)
        settings = request.form[DISPLAY_CHART_FORM_NAMES['settings']]
        settings = json.loads(settings)
        # chart wrappers id
        id       = int(request.form[DISPLAY_CHART_FORM_NAMES['id']])

        # get chart for overlay from a file
        code = save_file(request)
        # file saving failed
        if code in [NO_FILE, FILENAME_EMPTY, INCORRECT_FILE]:
            print("file saving failed; code:" + str(code))
            return redirect(request.url)
        # file saving succeed
        print("app.py | get_file(): file saving succeed; code:" + str(code))
        filename = secure_filename(request.files['file'].filename)
        card_name = request.form['name']

        # Read data from a file (i.e. .xlsx or .csv)
        RawData = PrepareData_FromFile(app.config["UPLOAD_FOLDER"] + '/' + filename)

        # Delete file from server
        remove_file(filename)

        # Prepare card data for js
        json_data = CalculateData(RawData['X'], card_name)
        json_data['Labels'] = RawData['Labels']
        json_data['Name'] = card_name

        data_for_overlay = json.loads(data[id-1])
        data_for_overlay['Overlay'] = json_data
        data[id-1] = json.dumps(data_for_overlay)

        settings['with_overlay'] = True

        return display(json_data_list   = data,
                       display_settings = settings)


@app.route("/add_another_chart", methods=["POST"])
def add_another_chart():
    if request.method == 'POST':
        # list [] of all chart wrappers
        data = request.form[DISPLAY_CHART_FORM_NAMES['data']]
        data = json.loads(data)
        settings = request.form[DISPLAY_CHART_FORM_NAMES['settings']]
        settings = json.loads(settings)

        # get chart for overlay from a file
        code = save_file(request)
        # file saving failed
        if code in [NO_FILE, FILENAME_EMPTY, INCORRECT_FILE]:
            print("file saving failed; code:" + str(code))
            return redirect(request.url)
        # file saving succeed
        print("app.py | get_file(): file saving succeed; code:" + str(code))
        filename = secure_filename(request.files['file'].filename)
        card_name = request.form['name']

        # Read data from a file (i.e. .xlsx or .csv)
        RawData = PrepareData_FromFile(app.config["UPLOAD_FOLDER"] + '/' + filename)

        # Delete file from server
        remove_file(filename)

        # Prepare card data for js
        json_data = CalculateData(RawData['X'], card_name)
        json_data['Labels'] = RawData['Labels']
        json_data['Name'] = card_name

        data.append(json.dumps(json_data))

        return display(json_data_list   = data,
                       display_settings = settings)


if __name__ == '__main__':

    config.set_configuration(app)
    # DATABASE connection
    Database_actions.db_connection()

    app.run(host=config.LAUNCH_SETTINGS['host'],
            port=config.LAUNCH_SETTINGS['port'])

    # DATABASE connection close
    Database_actions.db_connection_close()

