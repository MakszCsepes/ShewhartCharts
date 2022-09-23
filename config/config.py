import json

# ======== CONFIGURATION ========
CONFIG_FILE         = "config/launchSettings.json"
DATABASE_CONNECTION = "config/db_connection.json"

# ===============================
LAUNCH_SETTINGS = {}

# app - flask app
def set_configuration(app):
    # CONFIGURE
    global LAUNCH_SETTINGS

    with open(CONFIG_FILE) as config_json_file:
        config_settings = json.load(config_json_file)
        app.config["UPLOAD_FOLDER"] = config_settings['upload_folder']
        LAUNCH_SETTINGS             = config_settings['host_and_port']
