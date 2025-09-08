import math
import time
from typing import Optional
import numpy as np
import pandas as pd
from itertools import permutations, combinations

#example solution: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
#at index of 'one_of_eleven' is the id of 'one_of_ten'

start_time = time.time()

####################################################################
############# data to be shaped by progression of show #############
####################################################################

full_size_table = False
print_absolute_table = False #only if possible solutions < 100000
size_of_smaller_group = 10 # normally 10
size_of_bigger_group = 11 # normally 11
count = 0
abs_table = np.array([[0 for _ in range(size_of_bigger_group)] for _ in range(size_of_smaller_group)])
pos_lights = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

sheet = pd.read_excel("C:\\Julian\\AYTO\\AYTO_Infos.xlsx", header=None)
ex_tenP = []
ex_elevenP = []
ex_matches = []
ex_no_matches = []
ex_nights = []
newest_night = []

#read excel data
for x in range(size_of_smaller_group): # 10 p in group 1
    ex_tenP.append(sheet[x+1][0])
for x in range(size_of_bigger_group): # 11 p in group 2
    ex_elevenP.append(sheet[x+1][1])
for x in range(10): # 10 possible matches
    if pd.isna(sheet[0][5+x]):
        break
    if pd.isna(sheet[2][5+x]):
        temp = [sheet[0][5 + x], sheet[1][5 + x]]
    else:
        temp = [sheet[0][5 + x], sheet[1][5 + x], sheet[2][6 + x]]
    ex_matches.append(temp)
for x in range(100): # many possible no matches
    if pd.isna(sheet[4][5+x]):
        break
    temp = [sheet[4][5 + x], sheet[5][5 + x]]
    ex_no_matches.append(temp)
for n in range(10): # 10 possible nights
    ex_night = []
    if pd.isna(sheet[7+n*3][5]):
        break
    for x in range(len(ex_tenP)): # possible matches => len of smaller group
        temp = [sheet[7+n*3][5+x], sheet[8+n*3][5+x]]
        ex_night.append(temp)
    if pd.isna(sheet[8+n*3][4]):
        newest_night = ex_night
        break
    ex_night.append(sheet[8+n*3][4])
    ex_nights.append(ex_night)

# DELETE THIS LATER ################################################

tenP = ex_tenP
elevenP = ex_elevenP
matches = ex_matches
no_matches = ex_no_matches
nights = ex_nights

####################################################################
############### dont change anything from this point ###############
####################################################################

# Create all possible combinations

def generate_unique_pos_solutions():
    global count, print_absolute_table
    small_len = len(tenP)  # z.B. 5
    L = small_len + 1  # length of one solution-tuple, i.E. 11
    vals = list(range(small_len))  # [0,1,..,n-1]
    total = small_len * math.comb(L, 2) * math.factorial(small_len - 1)

    # cashing permutations (faster)
    perms_cache = {
        dup: list(permutations([v for v in vals if v != dup]))
        for dup in vals
    }

    m=0
    found_one = False
    first_sol = []

    pos_sol = []
    for dup in vals:
        rem_perms = perms_cache[dup]  # (n-1)! Entries
        for i, j in combinations(range(L), 2): # Positions for the double values
            for p in rem_perms:
                res: list[Optional[int]] = [None] * L
                res[i] = res[j] = dup
                it = iter(p)
                for k in range(L):
                    if res[k] is None:
                        res[k] = next(it)
                if check_matches(res) and check_no_matches(res) and check_nights(res):
                    pos_sol.append(tuple(res))
                    count += 1
                    add_to_absolute_table(res)
                    if len(newest_night) != 0:
                        add_to_possible_lights(res)
                    if not found_one:
                        found_one = True
                        first_sol = res

                m += 1
                if m % 10 == 0 or m == total:
                    perc = m*100/total
                    print(f'\rGenerating constellations: [{"#" * int(perc / 2)}{" " * (50 - int(perc / 2))}] {perc:.2f}% done!', end="")

    print()
    return first_sol

# String helpers

def solution_str(solution):
    solution = np.array(solution)
    ret = ""
    for i in range(len(solution)-1):
        ret += f"{tenP[i]}: {", ".join([elevenP[i] for i in np.where(solution == i)[0]])}\n"
    return ret

def show_name(name):
    spaces = 9 - len(name)
    return int(spaces/2)*" " + name + round(spaces/2+0.3)*" "

# Table creation

def add_to_absolute_table(solution):
    global abs_table
    for i in range(len(solution)):
        abs_table[solution[i]][i] += 1

def print_table():
    global abs_table
    print("\n")
    if full_size_table:
        empty_line,end = " " * 9 + ("|" + " " * 9) * len(elevenP),"\n"
    else:
        empty_line,end = "",""
    print(empty_line,end=end)
    header = " " * 9
    for i in range(len(elevenP)):
        header += "|" + show_name(elevenP[i])
    print(header)
    print(empty_line,end=end)
    full_line = "-"*9 + ("+" + "-"*9)*len(elevenP)
    for i in range(len(tenP)):
        print(full_line)
        print(empty_line,end=end)
        data_line = show_name(tenP[i])
        for j in range(len(elevenP)):
            abs_val = abs_table[i][j]
            percentage = round(int(abs_val) / count * 100, 1)
            extra_zero = ""
            entry = f"{abs_val}" if print_absolute_table else f"{percentage}%"
            if percentage < 10:
                extra_zero = " "
                if abs_val == 0:
                    entry = f"\033[31m--- \033[0m"
            if abs_val > count/2:
                entry = f"\033[33m{entry}\033[0m"
            if abs_val == count:
                entry = f"\033[32m YES \033[0m"
            if print_absolute_table and not (abs_val == 0 or abs_val == count):
                extra_zero = " "*(5 - len(str(abs_val)))
            data_line += "|" + "  " + extra_zero + entry + "  "
        print(data_line)
        print(empty_line,end=end)

def show_new_insights():
    global abs_table
    new_matches = []
    new_no_matches = []
    matched_ten_p = []
    matched_eleven_p = []
    next_mbox = []
    for m in matches:
        matched_ten_p.append(m[0])
        matched_eleven_p.append(m[1])
    for i in range(len(abs_table)):
        for j in range(len(abs_table[i])):
            if abs_table[i][j] == count:
                match = [tenP[i], elevenP[j]]
                if not any(all(item in main_list for item in match) for main_list in matches):
                    new_matches.append(match)
            elif abs_table[i][j] == 0:
                no_match = [tenP[i], elevenP[j]]
                if no_match not in no_matches and not (elevenP[j] in matched_eleven_p or tenP[i] in matched_ten_p):
                    new_no_matches.append(no_match)
            if len(next_mbox) == 0 or abs(count/2-abs_table[i][j]) < next_mbox[0]:
                next_mbox = [abs(count/2-abs_table[i][j]), tenP[i], elevenP[j]]
    print("NEW_INSIGHTS:")
    print(f"New matches:\n{new_matches}")
    print(f"New no matches:\n{new_no_matches}")
    print(f"Statistically best next matchbox:\n{[next_mbox[1],next_mbox[2]]}")

def add_to_possible_lights(possibility):
    global pos_lights
    light_num = 0
    for i in range(len(tenP)):
        w = elevenP.index(newest_night[i][1])
        if tenP[possibility[w]] == newest_night[i][0]:
            light_num += 1
    pos_lights[light_num] += 1

def print_lights():
    print("\n num | possibility")
    print("-----+-------------")
    for i in range(len(elevenP)):
        print(f" {" "*(1-int(i/10))}{i}  |   {" "*(3-len(str(int(pos_lights[i] / count*100))))}{pos_lights[i] / count * 100:.2f}%")

# Solution checks
def check_matches(solution):
    for match in matches:
        one_of_ten = tenP.index(match[0])
        one_of_eleven = elevenP.index(match[1])

        if solution[one_of_eleven] != one_of_ten:
            return False
        if len(match) == 2:
            for w in range(len(elevenP)):
                if solution[w] == one_of_ten and w != one_of_eleven:
                    return False
        if len(match) == 3:
            second_w = elevenP.index(match[2])
            if solution[second_w] != one_of_ten:
                return False
    return True

def check_no_matches(solution):
    for match in no_matches:
        one_of_ten = tenP.index(match[0])
        one_of_eleven = elevenP.index(match[1])
        if solution[one_of_eleven] == one_of_ten:
            return False
    return True

def check_nights(solution):
    if len(nights) == 0:
        return True
    for night in nights:
        lights = night[len(tenP)]
        for i in range(len(tenP)):
            match = night[i]
            one_of_ten = tenP.index(match[0])
            one_of_eleven = elevenP.index(match[1])
            if solution[one_of_eleven] == one_of_ten:
                lights = lights - 1
                if lights < 0:
                    return False
        if lights != 0:
            return False
    return True

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    one_possibility = generate_unique_pos_solutions()

    if count == 0:
        print("There seems to be an error in this code, the starting parameters set by you in the excel sheet or at RTL.\n"
              "After careful consideration it's probably RTL's fault or a typo on your end.")
        exit(1)

    if count >= 100000:
        print_absolute_table = False
    print_table()

    print(f'\n{count} different solutions exist!')
    print(f'\nOne random possible solution might be:\n{solution_str(one_possibility)}')

    show_new_insights()

    if len(newest_night) != 0:
        print("Possible amount of lights turning on in the next matching night:\n")
        print_lights()

    end_time = time.time()
    print(f"\nThis AYTO-Calculator was presented to you by Julian Damm in {int(round(end_time-start_time) / 60)} minutes {round(end_time-start_time) % 60} seconds.")#"""