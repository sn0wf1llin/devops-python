if __name__ == '__main__':
    student_list = []

    for _ in range(int(input())):
        name = input()
        score = float(input())
        student_list.append([name, score])
	
    
    print(student_list)
    student_list = [x for x in student_list if x[1] * 10 % 10 != 0]
    sorted_mod_student_list = sorted([[i[0], i[1]*100] for i in student_list])
    grades_set = set([i[1] for i in sorted_mod_student_list])
    grades_sorted_list = sorted(list(grades_set))
    slv = grades_sorted_list[1]

    print("".join([i[0] + "\n" for i in sorted_mod_student_list if i[1] == slv])) 
    

