import xlrd
import csv

ALLOWED_EXTENSIONS = ['xlsx', 'csv', 'ods', 'txt']

# Read data from Excel file
# RETURNS -> dict: {'Labels': [], 'X': [] }
def PrepareData_FromFile(filename):
    res = {'Labels': [], 'X': []}
    extension = filename.rsplit('.', 1)[1].lower()
    if extension == 'csv':
        res = GetCSVData(filename)
    if extension == 'xlsx':
        wb    = xlrd.open_workbook(filename)
        sheet = wb.sheet_by_index(0)

        X_label = []
        X       = []
        for i in range(sheet.nrows - 1):
            X_label.append(sheet.cell_value(i + 1, 0))
            X.append(sheet.cell_value(i + 1, 1))
        res['Labels'] = X_label
        res['X']      = X
    return res

# Read data from .csv file
# RETURNS -> dict: {'Labels': [], 'X': [] }
def GetCSVData(filename) -> {}:
    res = {'Labels': [], 'X': []}
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)

        field_1 = reader.fieldnames[0]
        field_2 = reader.fieldnames[1]
        for row in reader:
            res['Labels'].append(row[field_1])
            res['X'].append(float(row[field_2]))

        return res


def is_file_allowed(file):
    return '.' in file and \
            file.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS