def enter_grade():
    grade = input("grade: ")
    try:
        grade1, grade2 = grade.split()[:2]
    except Exception as e:
        grade1, grade2 = grade, ""

    return grade1, grade2


def read_new_student():
    name = input("name: ")
    grade1, grade2 = enter_grade()

    while 1:
        try:
            grade1 = int(grade1)
        except Exception as e:
            print("\tgrade is a number, you entered <{}>".format(grade1))
            grade1, grade2 = enter_grade()

        if grade2 == "":
            return {
                "name": name,
                "grade": [grade1]
            }

        else:
            try:
                grade2 = int(grade2)
            except Exception as e:
                print("\tgrade is a number, you entered <{}>".format(grade2))
                grade1, grade2 = enter_grade()
                continue
            return {
                "name": name,
                "grade": [grade1, grade2]
            }


def main():
    while 1:
        N = int(input("Count of students: "))

        if 2 <= N <= 5:
            break
        else:
            print("N if {}! It is not in [2..5]. Try again ".format(N))

    student_list = []
    for i in range(N):
        student_list.append(read_new_student())


if __name__ == "__main__":
    main()
== == == =
if __name__ == '__main__':
    student_list = []

    for _ in range(int(input())):
        name = input()
        score = float(input())
        student_list.append([name, score])

    print(student_list)
    student_list = [x for x in student_list if x[1] * 10 % 10 != 0]
    sorted_mod_student_list = sorted([[i[0], i[1] * 100] for i in student_list])
    grades_set = set([i[1] for i in sorted_mod_student_list])
    grades_sorted_list = sorted(list(grades_set))
    slv = grades_sorted_list[1]

    print("".join([i[0] + "\n" for i in sorted_mod_student_list if i[1] == slv]))
