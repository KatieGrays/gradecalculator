import matplotlib.pyplot as plt
import os
import sys

def student_info(filename):
    students_dict = {}
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            students_dict[line[:3]] = line[3:]
    return students_dict


def assignment_info(filename):
    assignment_dict = {}
    with open(filename, 'r') as file:
        content = file.read().strip().split('\n')
        for i in range(0, len(content), 3):
            name = content[i]
            assignment_id = content[i + 1]
            points = int(content[i + 2])
            assignment_dict[assignment_id] = (name, points)
    return assignment_dict


def submission_info(foldername):
    submissions = []
    for filename in os.listdir(foldername):
        with open(os.path.join(foldername, filename), 'r') as file:
            for line in file:
                parts = line.strip().split('|')
                if len(parts) == 3:
                    submissions.append((parts[0], parts[1], float(parts[2])))
                else:
                    print("Error")
    return submissions


def student_overall_grade(students, assignments, submissions, studentname):
    student_id = ''
    for id, name in students.items():
        if name == studentname:
            student_id = id
            break
    if not student_id:
        print("Student not found")
        return
    total_points = 0
    total_possible_points = 0
    for id, aid, grade in submissions:
        if id == student_id:
            total_points += (grade / 100) * assignments[aid][1]
            total_possible_points += assignments[aid][1]
    if total_possible_points == 0:
        print("No submissions found for this student.")
    else:
        average_grade = (total_points / total_possible_points) * 100
        print(f"{(int(round(average_grade)))}%")


def assignment_statistics(assignment_dict, submissions, assignmentname):
    assignment_id = ''
    assignment_grades = []
    for id, (name, points) in assignment_dict.items():
        if name == assignmentname:
            assignment_id = id
            break
    if not assignment_id:
        print("Assignment not found")
        return
    for studentid, id, grade in submissions:
        if id == assignment_id:
            assignment_grades.append(grade)
    if not assignment_grades:
        print("No submissions found for this assignment.")
    else:
        print(f"Min: {int(min(assignment_grades))}%")
        print(f"Avg: {int(sum(assignment_grades) / len(assignment_grades))}%")
        print(f"Max: {int(max(assignment_grades))}%")


def assignment_graph(assignment_dict, submissions, assignment_name):
    assignment_id = None
    assignment_grades = []
    for id, (name, points) in assignment_dict.items():
        if name == assignment_name:
            assignment_id = id
            break
    if assignment_id is None:
        print("Assignment not found")
        return

    for studentid, id, grade in submissions:
        if id == assignment_id:
            assignment_grades.append(grade)

    if not assignment_grades:
        print("No submissions found for this assignment.")
    else:
        plt.hist(assignment_grades, bins=range(50, 101, 5))
        plt.xlabel('Grade Percentage')
        plt.ylabel('Students')
        plt.title(f'{assignment_name}')
        plt.show()

def main():
    students = student_info('data/students.txt')
    assignments = assignment_info('data/assignments.txt')
    submissions = submission_info('data/submissions')

    input_lines = sys.stdin.read().strip().split('\n')
    input_index = 0

    while input_index < len(input_lines):
        print('''1. Student grade
2. Assignment statistics
3. Assignment graph

Enter your selection: ''')


        menu_option = input_lines[input_index].strip()
        input_index += 1

        if menu_option == '1':
            print("What is the student's name: ")
            studentname = input_lines[input_index].strip()
            input_index += 1
            student_overall_grade(students, assignments, submissions, studentname)
        elif menu_option == '2':
            print("What is the assignment name: ")
            assignmentname = input_lines[input_index].strip()
            input_index += 1
            assignment_statistics(assignments, submissions, assignmentname)
        elif menu_option == '3':
            print("What is the assignment name: ")
            assignment_name = input_lines[input_index].strip()
            input_index += 1
            assignment_graph(assignments, submissions, assignment_name)
        else:
            print("Invalid option. Please try again.")

if __name__ == '__main__':
    main()
