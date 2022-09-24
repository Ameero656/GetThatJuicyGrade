def main():
    compare_mode = input("Comparison mode? ([y], n):")
    scaling = get_grade_rating()
    gradeinfo = add_assesment_information()
    currentgrade = calculate_grade(gradeinfo, scaling)
    if compare_mode != 'n':
        comparing = True
        while comparing:
            print("COMPARISON::")
            gradeinfo = add_assesment_information()
            experimentgrade = calculate_grade(gradeinfo, scaling)
            compare(
                round(currentgrade * 100) / 100,
                round(experimentgrade * 100) / 100)
        ask = input("Add comparison ([y], n)?")
        if ask == 'n':
            comparing = False


def compare(cg, eg):

    contribution = round((eg - cg) * 100) / 100

    print(f"""
Current Grade: {cg}%
Hypothetical Grade: {eg}%
Hypothetical Contribution: {contribution}%

""")


def add_assesment_information():
    databank = {}
    databank["formative"] = {}
    databank['summative'] = {}
    while True:
        assesment = input('Formative Assesment ID:')
        score = input("Score (x/x):")
        score = score.split('/')
        achieved_score = float(score[0])
        maximum_score = float(score[1])
        databank["formative"][assesment] = {
            'AchievedScore': (achieved_score)
        }, {
            "MaximumScore": (maximum_score)
        }
        finish = input('Done adding formative assesments (y/n)?')
        if finish == 'y':
            break
    while True:
        assesment = input('Sumative Assesment ID:')
        score = input("Score (x/x):")
        score = score.split('/')
        achieved_score = float(score[0])
        maximum_score = float(score[1])
        databank["summative"][assesment] = {
            'AchievedScore': (achieved_score)
        }, {
            "MaximumScore": (maximum_score)
        }
        finish = input('Done adding summative assesments(y/n)?')
        if finish == 'y':
            return databank


def calculate_grade_fraction(scaling, score):
    fractionscore = float((score[0] / score[1]) * 100)
    worth = fractionscore * scaling
    print(f"""
%:{fractionscore}%
%worth:{round(worth*100)/100}%""")
    return worth


def calculate_grade(gradeinfo, scaling):
    total_formative_points = 0
    total_formative_achieved_points = 0
    total_summative_points = 0
    total_summative_achieved_points = 0
    print("FORMATIVE::")
    for assesment in gradeinfo['formative']:
        total_formative_points += gradeinfo['formative'][assesment][1][
            'MaximumScore']
        total_formative_achieved_points += gradeinfo['formative'][assesment][
            0]['AchievedScore']
    print(f"""
Assesment:{assesment}:
	Grade: {gradeinfo['formative'][assesment][0]['AchievedScore']}/{gradeinfo['formative'][assesment][1]['MaximumScore']}
""")
    print(f"""
Total Avalible Formative Points: {total_formative_points}
Total Achieved Points: {total_formative_achieved_points}
Final Formative: {total_formative_achieved_points}/{total_formative_points} | {total_formative_achieved_points/ total_formative_points*10}%
""")
    formative_worth = calculate_grade_fraction(float(
        scaling[1]), [total_formative_achieved_points, total_formative_points])
    print("-----------------")
    print("SUMMATIVE::")
    for assesment in gradeinfo['summative']:
        total_summative_points += gradeinfo['summative'][assesment][1][
            'MaximumScore']
        total_summative_achieved_points += gradeinfo['summative'][assesment][
            0]['AchievedScore']
        print(f"""
Assesment:{assesment}:
	Grade: {gradeinfo['summative'][assesment][0]['AchievedScore']}/{gradeinfo['summative'][assesment][1]['MaximumScore']}
""")
    print(f"""
Total Avalible Summative Points: {total_summative_points}
Total Achieved Points: {total_summative_achieved_points}
Final Summative: {total_summative_achieved_points}/{total_summative_points} | {total_summative_achieved_points/total_summative_points*10}%
""")
    summative_worth = calculate_grade_fraction(float(
        scaling[0]), [total_summative_achieved_points, total_summative_points])
    print("-----------------")
    final_grade = formative_worth + summative_worth
    print(f"""
FINAL GRADE:
	::{round(final_grade*100)/100}%
----------------------

""")

    return final_grade


def calculate_alternate_grade(gradeinfo):
    pass


def get_grade_rating():
    a = float(input('Summative % worth:'))
    b = float(input('Formative % worth:'))
    return a / 100, b / 100


main()
