import sys
import time
import numpy as np
import pandas as pd
from itertools import permutations

#example solution: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
#at index of 'one_of_eleven' is the id of 'one_of_ten'

start_time = time.time()

####################################################################
############# data to be shaped by progression of show #############
####################################################################

full_size_table = False
absolute_table = False #only if possible solutions < 100000

sheet = pd.read_excel("C:\\Julian\\AYTO\\AYTO_Infos.xlsx", header=None)
ex_tenP = []
ex_elevenP = []
ex_matches = []
ex_no_matches = []
ex_nights = []
newest_night = []

#read excel data
for x in range(10):
    ex_tenP.append(sheet[x+1][0])
for x in range(11):
    ex_elevenP.append(sheet[x+1][1])
for x in range(10):
    if pd.isna(sheet[0][5+x]):
        break
    if pd.isna(sheet[2][5+x]):
        temp = [sheet[0][5 + x], sheet[1][5 + x]]
    else:
        temp = [sheet[0][5 + x], sheet[1][5 + x], sheet[2][6 + x]]
    ex_matches.append(temp)
for x in range(100):
    if pd.isna(sheet[4][5+x]):
        break
    temp = [sheet[4][5 + x], sheet[5][5 + x]]
    ex_no_matches.append(temp)
for n in range(10):
    ex_night = []
    if pd.isna(sheet[7+n*3][5]):
        break
    for x in range(10):
        temp = [sheet[7+n*3][5+x], sheet[8+n*3][5+x]]
        ex_night.append(temp)
    if pd.isna(sheet[8+n*3][4]):
        newest_night = ex_night
        break
    ex_night.append(sheet[8+n*3][4])
    ex_nights.append(ex_night)

tenP = ex_tenP
elevenP = ex_elevenP
matches = ex_matches
no_matches = ex_no_matches
nights = ex_nights

####################################################################
############### dont change anything from this point ###############
####################################################################

# Create all possible combinations

def init_possible_solutions():
    unique_numbers = list(range(10))  # Numbers 0-9
    pos_sol = set()
    i = 0
    j = 1

    for perm in permutations(unique_numbers + [10]):  # Generate all permutations of 0-9
        i += 1
        while i> (39916800 / 100 * j):
            j += 1
            sys.stdout.write(f'\rGenerating constellations: [{"#"*int(j/2)}{" "*(50-int(j/2))}] {j}% done!')
            sys.stdout.flush()
        for num in unique_numbers:  # Choose a number to duplicate
            replaced = tuple(num if f == 10 else f for f in perm)
            if check_no_matches(replaced) and check_matches(replaced) and check_nights(replaced):
                pos_sol.add(replaced)
    print()
    return list(pos_sol)

# String helpers

def solution_str(solution):
    solution = np.array(solution)
    ret = ""
    for i in range(10):
        ret += f"{tenP[i]}: {", ".join([elevenP[i] for i in np.where(solution == i)[0]])}\n"
    return ret

def show_name(name):
    spaces = 9 - len(name)
    return int(spaces/2)*" " + name + round(spaces/2+0.3)*" "

# Table creation

def get_percentage_table(possibilities):
    table = np.array([[float(0.0) for _ in range(11)] for _ in range(10)])
    k,j,length = 0,0,len(possibilities)*11
    for solution in possibilities:
        for i in range(11):
            k += 1
            while k > (length * j / 100):
                j += 1
                sys.stdout.write(
                    f'\rCalculating percentages:   [{"#" * int(j / 2)}{" " * (50 - int(j / 2))}] {j}% done!')
                sys.stdout.flush()
            table[solution[i]][i] += 1
    table *= 100 / len(possibilities)
    return table

def create_percentage_table(possibilities):
    percentage_table = get_percentage_table(possibilities)
    print("\n")
    if full_size_table:
        empty_line,end = " " * 9 + ("|" + " " * 9) * 11,"\n"
    else:
        empty_line,end = "",""
    print(empty_line,end=end)
    header = " " * 9
    for i in range(11):
        header += "|" + show_name(elevenP[i])
    print(header)
    print(empty_line,end=end)
    full_line = "-"*9 + ("+" + "-"*9)*11
    for i in range(10):
        print(full_line)
        print(empty_line,end=end)
        data_line = show_name(tenP[i])
        for j in range(11):
            percentage = round(float(percentage_table[i][j]),1)
            abs_val = round(float(percentage_table[i][j] * len(possibilities) / 100))
            extra_zero = ""
            entry = f"{abs_val}" if absolute_table else f"{percentage}%"
            if percentage < 10:
                extra_zero = " "
                if percentage == 0:
                    entry = f"\033[31m--- \033[0m"
            if percentage > 50:
                entry = f"\033[33m{entry}\033[0m"
            if percentage == 100:
                entry = f"\033[32m YES \033[0m"
            if absolute_table and not (percentage == 0 or percentage == 100):
                extra_zero = " "*(5 - len(str(abs_val)))
            data_line += "|" + "  " + extra_zero + entry + "  "
        print(data_line)
        print(empty_line,end=end)
    return percentage_table

def show_new_insights(table):
    new_matches = []
    new_no_matches = []
    matched_ten_p = []
    matched_eleven_p = []
    next_mbox = []
    for m in matches:
        matched_ten_p.append(m[0])
        matched_eleven_p.append(m[1])
    for i in range(len(table)):
        for j in range(11):
            if table[i][j] == 100:
                match = [tenP[i], elevenP[j]]
                if not any(all(item in main_list for item in match) for main_list in matches):
                    new_matches.append(match)
            elif table[i][j] == 0:
                no_match = [tenP[i], elevenP[j]]
                if no_match not in no_matches and not (elevenP[j] in matched_eleven_p or tenP[i] in matched_ten_p):
                    new_no_matches.append(no_match)
            if len(next_mbox) == 0 or abs(50-table[i][j]) < next_mbox[0]:
                next_mbox = [abs(50-table[i][j]), tenP[i], elevenP[j]]
    print("NEW_INSIGHTS:")
    print(f"New matches:\n{new_matches}")
    print(f"New no matches:\n{new_no_matches}")
    print(f"Statistically best next matchbox:\n{[next_mbox[1],next_mbox[2]]}")

def calculate_possible_lights(possibilities):
    lights = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for poss in possibilities:
        count = 0
        for i in range(10):
            w = elevenP.index(newest_night[i][1])
            if tenP[poss[w]] == newest_night[i][0]:
                count += 1
        lights[count] += 1

    print("\n num | possibility")
    print("-----+-------------")
    for i in range(11):
        print(f" {" "*(1-int(i/10))}{i}  |   {" "*(3-len(str(int(lights[i] / len(possibilities)*100))))}{lights[i] / len(possibilities) * 100:.2f}%")

# Solution checks
def check_matches(solution):
    for match in matches:
        one_of_ten = tenP.index(match[0])
        one_of_eleven = elevenP.index(match[1])

        if solution[one_of_eleven] != one_of_ten:
            return False
        if len(match) == 2:
            for w in range(11):
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
        lights = night[10]
        for i in range(10):
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

    all_possibilities = init_possible_solutions()

    if len(all_possibilities) == 0:
        print(
            "There seems to be an error in this code, the starting parameters set by you in the excel sheet or at RTL.\nAfter careful consideration it's probably RTL's fault or a typo on your end.")
        exit(1)

    if len(all_possibilities) >= 100000:
        absolute_table = False
    end_table = create_percentage_table(all_possibilities)

    print(f'\n{len(all_possibilities)} different solutions exist!')
    print(f'\nOne random possible solution might be:\n{solution_str(all_possibilities[np.random.randint(0, len(all_possibilities))])}')

    show_new_insights(end_table)

    if len(newest_night) != 0:
        calculate_possible_lights(all_possibilities)

    end_time = time.time()
    print(f"\nThis AYTO-Calculator was presented to you by Julian Damm in {round(end_time-start_time) / 60} minutes {round(end_time-start_time) % 60} seconds.")#"""