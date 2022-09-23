# n         - number value
# range     - dict: {'start', 'end'} or list [] of dict ranges
# including - boolean,
# in_all    - boolean, if True -> the value must be in all ranges
def is_value_in_ranges(n, ranges, including = False, in_all = False) -> {bool, list}:
    res = {'res': False, 'ranges_included': []}

    temp_res = False
    for i_range in range(0, ranges.__len__()):
        if including:
            temp_res = ranges[i_range]['start'] <= n <= ranges[i_range]['end']
        else:
            temp_res = ranges[i_range]['start'] < n < ranges[i_range]['end']

        if temp_res:
            res['ranges_included'].append(i_range)

    if in_all and res['ranges_included'].__len__() == ranges.__len__():
        res['res'] = True
    else:
        if res['ranges_included'].__len__() > 0:
            res['res'] = True

    return res

# in1,2 - means a value IS IN range
# out   - means a value IS OUT of range
def are_two_of_three_in_range(in1, in2, out, Range):
    if is_value_in_ranges(in1, Range) and \
       is_value_in_ranges(in2, Range) and not \
       is_value_in_ranges(out, Range):
            return True
    return False

# in_values  - list [] of numeric values TO BE in range
# out_values - list [] of numeric values excluded of range (NOT TO BE in range)
# Range      - dict: {'start', 'end'}
def are_values_in_range(in_values, out_values, Range):
    # if only one value (of in_values) is out of range -> false
    for i in in_values:
        if not is_value_in_ranges(i, [Range]):
            return False
    # if only one value (of out_values) is in range -> false
    for i in out_values:
        if is_value_in_ranges(i, [Range]):
            return False

    return True


# X          - list [] of values
# n          - how many values should be in range
# m          - how many values should not be in range
# Ranges     - list [] of dict: {'start', 'end'} range, where values supposed to be
# InAll      - (optional) values MUST BE in ALL ranges
# Exc_ranges - (optional) list [] of dict: {'start', 'end'} range, where values MUST NOT be
def are_sequential_values_in_ranges(X, n, m, Ranges, InAll = False, Excl_ranges = []):
    if len(Ranges) == 0: return False
    if len(X) < n or len(X) < m: return False

    num_values_in_ranges = num_values_out_of_ranges = 0
    all_ranges_included = set()

    excluded_ranges_size = len(Excl_ranges)
    for i in X:
        if excluded_ranges_size != 0 and is_value_in_ranges(i, Excl_ranges)['res']:
            num_values_in_ranges = num_values_out_of_ranges = 0
            continue

        value_in_ranges = is_value_in_ranges(i, Ranges, including=True)

        if InAll:
            i_included_ranges = value_in_ranges['ranges_included']
            for i in i_included_ranges:
                all_ranges_included.add(i)

        if value_in_ranges['res']:
            num_values_in_ranges += 1
            if num_values_out_of_ranges != m:
                num_values_out_of_ranges = 0
        else:
            num_values_out_of_ranges += 1
            if num_values_in_ranges != n:
                num_values_in_ranges = 0

        if num_values_in_ranges == n and \
           num_values_out_of_ranges == m:
                if InAll:
                    if len(all_ranges_included) == Ranges.__len__():
                        return True
                    else:
                        continue

                return True

    return False


# CUSTOM Longest Increasing Sequence
# X          - list of values
# increasing - True: increasing mode; False: decreasing mode
# RETURNS -> dict: {'start', 'end'}
def FindLIS(X, condition = (lambda X, i: X[i] > X[i-1])) -> {'start', 'end'}:
    res = {'start': 0,
           'end': 0}

    if len(X) == 1: return res

    start = startIndex = 0
    length = max_length = 1
    for i in range(1, len(X), 1):
        if condition(X, i):
            length += 1
        else:
            if length > max_length:
                max_length = length
                startIndex = start
            length = 1
            start = i

    if length > max_length:
        max_length = length
        startIndex = start

    res['start'] = startIndex
    res['end'] = startIndex + max_length
    return res


