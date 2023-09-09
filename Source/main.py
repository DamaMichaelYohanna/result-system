from middleware import find_total_score_per_subject, find_total_score_all_subject, find_position


score: dict = {}
subject_list: list = ["English", "Mathematics", "Civic Education"]
print("********************************************")
print("++++++ WELCOME TO OUR SCORE BOOK APP +++++++")
print("____________________________________________")
print("for simplicity, we only have three subject for test")
print("--------- Subjects are listed below --------")
for index, subject in enumerate(subject_list):
    print(f"#{index}  {subject}")
print("--------------------------------------------")
student_number:str = input("Enter number of student for entry ")
student_names: list = []
print("--------- Enter students names below--------")
for n in range(int(student_number)):
    student_names.append(input("Enter student name: "))
    print("-----------------------------------------------")
print("--------------------------------------------")

for s in subject_list:
    print("++++++++++++++++++++++++++++++++++++++++++++++++")
    print(f"Now we proceed entry for  {s}")
    print("++++++++++++++++++++++++++++++++++++++++++++++++")
    for name in student_names:
        assignment = input(f"Enter assignment score for {name} ")
        test1 = input(f"Enter 1st CA score for {name} ")
        test2 = input(f"Enter 2nd CA score for {name} ")
        exams = input(f"Enter exams score for {name}")
        score[name] = {s: {"assignment": int(assignment), "test1": int(test1),
                                 "test2": int(test2), "exam": int(exams)}}
        print()
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++")


prepare_data: dict = {}

for name in score:
    _, edited_data = find_total_score_per_subject(score[name])
    prepare_data[name] = _

sum_total = find_total_score_all_subject(prepare_data)
print(sum_total)
print(find_position(sum_total))