import json
import numpy as np
import xlrd
import Database_actions
from abc import abstractmethod

from constants import SAVING_CHART_RETURN_CODES

# ======== CHARTS BUILDING CONFIGURATION ======== <
# ====== COEFFICIENTS (Solonin, Section 3.3.) === <
from kksh_utils import are_values_in_range, are_sequential_values_in_ranges, FindLIS

MAIN_TABLE_NAME  = "Coefficients.xlsx"
MAIN_TABLE_SHEET = "Coefficients"
# =============================================== >
# =============================================== >

# RETURNS -> dict: {'subset size': {'coefficient': value}}
def openTableOfCoefficients() -> {}:
    wb    = xlrd.open_workbook(MAIN_TABLE_NAME)
    sheet = wb.sheet_by_name(MAIN_TABLE_SHEET)

    nrows = sheet.nrows
    ncols = sheet.ncols

    obj = {}
    for i in range(1, nrows):
        obj[int(sheet.cell_value(i, 0))] = {}
        for j in range(1, ncols):
            obj[sheet.cell_value(i, 0)][sheet.cell_value(0, j)] = sheet.cell_value(i, j)

    obj[1] = obj[2]
    return obj


TABLE = openTableOfCoefficients()



# ======== CRITERIA (Solonin, Section 4) ==================================

# 1 или более точeк лежат выше UCL или ниже нижней зоны LCL

# X   - list []
# UCL - numeric
# LCL - numeric
# RETURNS -> [bool, int]: is the criterion present,
#                         number of dots lying above UCL or below LCL
def Criteria_1(X, UCL, LCL) -> [bool, {int}]:
    CRITERION_1 = 1
    num = 0
    res = [False]

    for i in X:
        if i > UCL or i < LCL:
            num += 1

    if num >= CRITERION_1:
        res = [True, {'total': num}]

    return res

# 2 из 3 последовательных точек лежат в одной из зон A

# X   - list []
# A_U - dict: range {'start', 'end'}
# A_L - dict: range {'start', 'end'}
# RETURNS -> list [] of # boolean value, which determines whether there is the criterion
                        # if True, index of trend sequence beginning
                        # if True, 1st value
                        # if True, 2nd value
                        # if True, 3rd value
def Criteria_2(X, A_U, A_L) -> [bool, int, int, int, int]:
    CRITERION_2 = 2
    res = [False]

    if len(X) < CRITERION_2 + 1: return res

    for i in range(1, len(X) - 1):
        a, b, c = X[i-1], X[i], X[i+1]

        # Check Upper A
        # a, c are in A_U zone, b is not
        # a, b are in A_U zone, c is not
        # b, c are in A_U zone, a is not
        if are_values_in_range([a, c], [b], A_U) or \
           are_values_in_range([a, b], [c], A_U) or \
           are_values_in_range([b, c], [a], A_U):
                res = [True, i-1, a, b, c]

        if res[0]: break

        # Check Lower A
        # a, c are in A_L zone, b is not
        # a, b are in A_L zone, c is not
        # b, c are in A_L zone, a is not
        if are_values_in_range([a, c], [b], A_L) or \
           are_values_in_range([a, b], [c], A_L) or \
           are_values_in_range([b, c], [a], A_L):
                res = [True, i-1, a, b, c]

    return res

# 4 из 5 последовательных точек лежат в зоне B
# или вне ее в зоне A по одну сторону от CL

# X   - list []
# CL  - numeric
# B_U - dict: range {'start', 'end'}
# B_L - dict: range {'start', 'end'}
# A_U - dict: range {'start', 'end'}
# A_L - dict: range {'start', 'end'}
def Criteria_3(X, B_U, B_L, A_U, A_L) -> [bool]:
    CRITERION_3 = 4
    res = [False]

    if len(X) < CRITERION_3 + 1: return res

    # Above CL
    if are_sequential_values_in_ranges(X, CRITERION_3, 1, [B_U]) or \
       are_sequential_values_in_ranges(X, CRITERION_3, 1, [A_U]):
            res = [True, {}]
    # Below CL
    if are_sequential_values_in_ranges(X, CRITERION_3, 1, [B_L]) or \
       are_sequential_values_in_ranges(X, CRITERION_3, 1, [A_L]):
            res = [True, {}]

    return res

# 9 точек подряд лежат по одну сторону от CL
# (в зоне С или вне ее)
def Criteria_4(X, CL) -> [bool, {int}]:
    CRITERION_4 = 9
    res = [False]
    if len(X) < CRITERION_4: return res

    num = 0
    position = 0
    sequence_start_index = -1
    for i in range(0, len(X)):
        # define points position (over CL (1), under CL (-1) )
        if position == 0:
            if X[i] > CL:
                sequence_start_index = i
                position = 1
            else:
                sequence_start_index = i
                position = -1

            num += 1
            continue

        # over CL
        if position == 1:
            if X[i] > CL:
                num += 1
            else:
                position = 0
                num = 0

        # under CL
        if position == -1:
            if X[i] < CL:
                num += 1
            else:
                position = 0
                num = 0

        if num == CRITERION_4:
            res = [True, {'start': sequence_start_index}]
            return res

    return res

# 6 или более возрастающих или
# убывающих подряд точек.
def Criteria_5(X) -> [bool, {}]:
    CRITERION_5 = 6
    res_incr = FindLIS(X)
    res_decr = FindLIS(X, lambda X, i: X[i] < X[i-1])

    # if sequence INCREASING
    if res_incr['end'] - res_incr['start'] >= CRITERION_5:
        return [True, res_incr]

    # if sequence DECREASING
    if res_decr['end'] - res_decr['start'] >= CRITERION_5:
        return [True, res_decr]

    return [False]

# 14 или более попеременно возрастающих и убывающих
# последовательных точек, напоминающих периодический процесс.
def Criteria_6(X) -> [bool]:
    CRITERION_6 = 14
    max_num = num = 0
    position = 0

    for i in range(1, len(X)):
        # define points position (over CL (1), under CL (-1) )
        if position == 0:
            # more than
            if X[i] > X[i-1]:
                sequence_start_index = i
                position = 1
            # less than
            elif X[i] < X[i-1]:
                sequence_start_index = i
                position = -1

            num = 2
            continue

        # current value should be less than previous
        if position == 1:
            if X[i] < X[i-1]:
                num += 1
                position = -1
            else:
                if num > max_num:
                    max_num = num
                num = 2
                position = -1
            continue
        # current value should be more than previous
        if position == -1:
            if X[i] > X[i-1]:
                num += 1
                position = 1
            else:
                if num > max_num:
                    max_num = num
                num = 2
                position = 1
            continue

    if num > max_num:
        max_num = num

    if max_num >= CRITERION_6:
        return [True]

    return [False]

# 15 последовательных точек
# в зоне C выше и ниже CL.
def Criteria_7(X, C_U, C_L) -> [bool]:
    CRITERION_7 = 15
    if are_sequential_values_in_ranges(X, CRITERION_7, 0, [C_U, C_L]):
        return [True, {}]
    return [False]

# 8 последовательных точек по обеим
# сторонам CL и ни одной в зоне C.


# X     - list [] of values
# B_A_U - dict: {'start', 'end'} - range from B to A zone (up to the UCL)
# B_A_L - dict: {'start', 'end'} - range from B to A zone (down to the LCL)
# C     - dict: {'start', 'end'} - range from C bottom to C top zone
def Criteria_8(X, B_A_U, B_A_L, C) -> []:
    CRITERION_8 = 8
    if are_sequential_values_in_ranges(X, CRITERION_8, 0, Ranges=[B_A_U, B_A_L], InAll = True, Excl_ranges=[C]):
        return [True, {}]
    return [False]

# =================================================================================


class Card:
    Name = "Card"
    N    = -1  # size of a sampling
    X    = []

    # X Control limits
    CL  = -1
    UCL = -1
    LCL = -1

    is_process_stable = True  # is the process statistically controlled (SPC)

    def __init__(self, X, name = "card"):
        self.X = X
        self.N = len(X)
        self.Name = name

    def Get_X(self):
        return self.X

    def Get_N(self):
        return self.N

    @abstractmethod
    def Calculate(self):
        pass

    @abstractmethod
    def Calculate_CL(self):
        pass

    @abstractmethod
    def Calculate_UCL(self):
        pass

    @abstractmethod
    def Calculate_LCL(self):
        pass

    @abstractmethod
    def CriteriaInvestigate(self) -> []:
        u_sigma = (self.UCL - self.CL) / 3.0
        l_sigma = (self.CL - self.LCL) / 3.0

        A_U = {'start': self.UCL - u_sigma,     'end': self.UCL}
        B_U = {'start': self.UCL - 2 * u_sigma, 'end': self.UCL - u_sigma}
        C_U = {'start': self.CL,                'end': self.UCL - 2 * u_sigma}

        C_L = {'start': self.CL - l_sigma,     'end': self.CL}
        B_L = {'start': self.CL - 2 * l_sigma, 'end': self.CL - l_sigma}
        A_L = {'start': self.LCL,              'end': self.CL - 2 * l_sigma}
        res = [
            Criteria_1(self.X, self.UCL, self.LCL),
            Criteria_2(self.X, A_U, A_L),
            Criteria_3(self.X, B_U, B_L, A_U, A_L),
            Criteria_4(self.X, self.CL),
            Criteria_5(self.X),
            Criteria_6(self.X),
            Criteria_7(self.X, C_U, C_L),
            Criteria_8(self.X, {'start': B_U['start'], 'end': A_U['end']},
                               {'start': A_L['start'], 'end': B_L['end']},
                               {'start': C_L['start'], 'end': C_U['end']})
        ]

        # Determine if the process is stable or not
        # if one of the criteria is false, then the process is not stable
        for criteria in res:
            if not criteria[0]:
                self.is_process_stable = False
                break


        new_res = {}
        for i in range(0, len(res)):
            if res[i][0] != False:
                new_res[str(i + 1)] = res[i][1]
            else:
                new_res[str(i + 1)] = False

        return json.dumps(new_res)

    def ToJSON(self):
        json_obj = {'X':        self.Get_X(),
                    'UCL':      self.UCL,
                    'CL':       self.CL,
                    'LCL':      self.LCL,
                    'CRITERIA': self.CriteriaInvestigate()}

        return json_obj


class Card_X(Card):
    __mR_CL = -1

    def __init__(self, X, mR_CL, name="card"):
        Card.__init__(self, X, name)
        self.__mR_CL = mR_CL

    def Calculate(self):
        self.Calculate_CL()

        # Calculate X Control Limits
        self.Calculate_UCL()
        self.Calculate_LCL()

        # Trends
        # todo find out where it's used
        self.DefineTrends()

    # Moving R Central Line
    def Calculate_CL(self):
        self.CL = np.average(self.Get_X())

    # X Upper Control Limit
    def Calculate_UCL(self):
        X_CL = self.CL
        R_CL = self.__mR_CL

        if X_CL == -1 or R_CL == -1: return

        # todo properly calculate 3 sigma
        # UpperValue = X_CL + (3 * R_CL) / J6
        # UpperValue = X_CL + TABLE[self.Get_N()]['A2'] * R_CL
        # self.UCL = UpperValue
        self.UCL = X_CL + R_CL*2.66

    # X Lower Control Limit
    def Calculate_LCL(self):
        X_CL = self.CL
        R_CL = self.__mR_CL

        if X_CL == -1 or R_CL == -1: return

        # BottomValue = X_CL - 3 * R_CL / J6
        # self.LCL = X_CL - TABLE[self.Get_N()]['A2'] * R_CL
        self.LCL = X_CL - R_CL*2.66

    def DefineTrends(self):
        # TREND
        TREND_LIMIT = 7
        LIS = FindLIS(self.Get_X())

        if LIS['end'] - LIS['start'] > TREND_LIMIT:
            self.Trend = LIS
        # TREND


class mR_Card(Card):

    def __init__(self, X, name="card"):
        Card.__init__(self, X, name)
        self.Calculate_Set(X)

    def Calculate(self):
        self.Calculate_CL()
        self.Calculate_UCL()
        self.Calculate_LCL()

    # Moving R Central Line
    def Calculate_CL(self):
        self.CL = np.average(self.X)

    # R Upper Control Line
    def Calculate_UCL(self):
        if self.CL == -1:
            return

        # self.UCL = TABLE[self.Get_N()]['D4'] * self.CL
        self.UCL = 3.267 * self.CL

    # R Bottom Control Line
    def Calculate_LCL(self):
        # self.LCL = TABLE[self.Get_N()]['D3'] * self.CL
        self.LCL = 0

    def Calculate_Set(self, X):
        X_SamplingSize = len(X)

        # Filling the list
        self.X = [0]
        for j in range(1, X_SamplingSize, 1):
            self.X.append(abs(X[j] - X[j - 1]))

        self.X[0] = self.X[1]


# RETURNS: json object with chart's characteristics
def CalculateData(X, CardName) -> {}:
    card_mR = mR_Card(X, name=CardName + "_mR")
    card_mR.Calculate()

    card_x = Card_X(X, mR_CL=card_mR.CL, name=CardName + "_X")
    card_x.Calculate()

    return {'X':  card_x.ToJSON(),
            'R': card_mR.ToJSON()}


# RETURNS: code of success from SAVING_CHART_RETURN_CODES
def SaveCard(json_data) -> int:
    json_obj = json.loads(json_data)
    X        = json_obj['X']['X']
    R        = json_obj['R']['X']
    Labels   = json_obj['Labels']
    subset   = {}


    # 1) ===== first save mR-card =====

    # Create a json object of card key-value pairs ('year': hdi_value)
    for i in range(0, len(R)):
        Labels[i] = str(Labels[i])
        subset[Labels[i]] = R[i]
    subset = json.dumps(subset)

    # 0) ===== check if such a card already exists =====
    TABLE_NAME = "Card"

    command = "select subset from " + TABLE_NAME + " where parent_id is null;"
    res = Database_actions.execute_SQL(command)

    is_chart_already_present = False
    for i in res:
        # get subset json
        chart_subset = i[0]

        if json.loads(subset).keys() == json.loads(chart_subset).keys():
            subset_to_save_obj  = json.loads(subset)
            subset_to_check_obj = json.loads(chart_subset)

            key_value_count = 0
            round_value = 5
            for j in subset_to_save_obj:
                if round(subset_to_save_obj[j], round_value) == round(subset_to_check_obj[j], round_value):
                    key_value_count += 1

            if key_value_count == len(subset_to_check_obj.keys()):
                is_chart_already_present = True
                break

    if is_chart_already_present:
        return SAVING_CHART_RETURN_CODES['ERROR_CARD_ALREADY_AVAILABLE']

    command = "INSERT into " + TABLE_NAME + "(card_name, subset, UCL, CL, LCL, is_stable, criteria, parent_id)" + \
              " VALUES(" + \
              "'" + str(json_obj['Name']) + "','" + \
              str(subset) + "', " +\
              str(json_obj['R']['UCL']) + ", " + \
              str(json_obj['R']['CL']) + ", " + \
              str(json_obj['R']['LCL']) + ", " + \
              "False" + ", '" + \
              str(json_obj['R']['CRITERIA']) + "', " + \
              "NULL"  + \
              ");"

    Database_actions.execute_SQL(command)

    # ===== 2) then get its `id` =====
    command = "select MAX(card_id) from " + TABLE_NAME
    res = Database_actions.execute_SQL(command)
    last_id = res[0][0]

    # ===== 3) and save X-card with the given `parent_id` =====
    subset = {}
    for i in range(0, len(X)):
        Labels[i] = str(Labels[i])
        subset[Labels[i]] = X[i]
    subset = json.dumps(subset)

    command = "INSERT into " + TABLE_NAME + "(card_name, subset, UCL, CL, LCL, is_stable, criteria, parent_id)" + \
              " VALUES(" + \
              "'" + str(json_obj['Name']) + "','" + \
              str(subset) + "', " + \
              str(json_obj['X']['UCL']) + ", " + \
              str(json_obj['X']['CL']) + ", " + \
              str(json_obj['X']['LCL']) + ", " + \
              "False" + ", '" + \
              str(json_obj['R']['CRITERIA']) + "', " + \
              str(last_id) + \
              ");"

    Database_actions.execute_SQL(command)

    Database_actions.db_commit()
    return SAVING_CHART_RETURN_CODES['SUCCESS']