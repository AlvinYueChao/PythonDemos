import math
import random
import sys

if __name__ == '__main__':
    students = list(range(26))
    teachers = list(range(12))
    max_num_of_students = math.ceil(len(students) / len(teachers))
    min_num_of_students = math.floor(len(students) / len(teachers))
    invalid_choices = {}

    # 每个同学的老师选择列表
    student_prefs = {
        0: [0, 1, 2],
        1: [1, 0, 2],
        2: [2, 1, 0],
        3: [3, 4, 5],
        4: [4, 3, 5],
        5: [5, 4, 3],
        6: [6, 7, 8],
        7: [7, 6, 8],
        8: [8, 7, 6],
        9: [9, 10, 11],
        10: [10, 11, 9],
        11: [11, 9, 10],
        12: [0, 2, 1],
        13: [1, 0, 2],
        14: [2, 1, 0],
        15: [3, 5, 4],
        16: [4, 3, 5],
        17: [5, 4, 3],
        18: [6, 8, 7],
        19: [7, 6, 8],
        20: [8, 7, 6],
        21: [9, 11, 10],
        22: [10, 9, 11],
        23: [11, 10, 9],
        24: [0, 1, 2],
        25: [2, 0, 1],
    }

    # 每个同学不能选择自己现在的老师
    current_relationship = {i: random.randint(0, len(teachers) - 1) for i in students}

    # 每位老师已经有的学生列表
    teacher_assignments = {i: [] for i in teachers}

    # 每位同学当前正在考虑的老师列表
    student_choices = {i: student_prefs[i] for i in students}

    while students:
        student = students.pop(0)
        choices = student_choices[student]
        if current_relationship[student] in choices:
            invalid_choices[student] = choices

    if invalid_choices:
        print("current relationship:")
        for student, teacher in current_relationship.items():
            print(f"student {student} teacher {teacher}")
        print("=======================")
        print("invalid choices:")
        for student, invalid_choices in invalid_choices.items():
            print(f"{student}: {invalid_choices}")
        sys.exit()

    while students:
        student = students.pop(0)
        choices = student_choices[student]
        for teacher in choices:
            if len(teacher_assignments[teacher]) < max_num_of_students:
                teacher_assignments[teacher].append(student)
                break
            elif student in teacher_assignments[teacher]:
                break
            elif len(teacher_assignments[teacher]) == min_num_of_students \
                    and student_prefs[teacher_assignments[teacher][0]].index(teacher) > student_prefs[student].index(teacher):
                old_student = teacher_assignments[teacher][0]
                teacher_assignments[teacher][0] = student
                student_choices[old_student] = student_prefs[old_student][1:]
                students.append(old_student)
                break
        student_choices[student] = choices[1:]

    for teacher, students in teacher_assignments.items():
        print(f"Teacher {teacher}: {students}")
