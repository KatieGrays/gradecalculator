import matplotlib.pyplot as plt
import os
import data
def main():

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

    def student_overall_grade(students, assignments, submissions):
        studentname = input("What is the student's name: ")
        student_id = ''
        for id, name in students.items():
            if name == studentname:
                student_id = id
            if student_id is None:
                print("Student not found")
                return
        average_grade = 0
        for id, aid, grade in submissions:
            if id == student_id:
                average_grade += (grade/100) * assignments[aid][1]
        print(f"{round(average_grade/1000 *100)}%")

    def assignment_statistics(assignment_dict, submissions):
        assignmentname = input("What is the assignment name: ")
        assignment_id = ''
        assignment_grades = []
        for id, (name, points) in assignments.items():
            if name == assignmentname:
                assignment_id = id
            if assignment_id is None:
                print("Assignment not found")
                return
            for studentid, id, grade in submissions:
                if id == assignment_id:
                    assignment_grades.append(grade)


        print(f"Min: {(int(min(assignment_grades)))}%")
        print(f"Avg: {int(sum(assignment_grades)/len(assignment_grades))}%")
        print(f"Max: {(int(max(assignment_grades)))}%")


    def assignment_graph(assignment_dict, submissions):
        assignment_name = input("What is the assignment name: ")
        assignment_id = None
        assignment_grades = []
        for id, (name, points) in assignments.items():
            if name == assignment_name:
                assignment_id = id
                break
        if assignment_id is None:
            print("Assignment not found")
            return

        for studentid, id, grade in submissions:
            if id == assignment_id:
                assignment_grades.append(grade)


        plt.hist(assignment_grades, bins=range(0, 100, 10))
        plt.show()

    students = student_info('students.txt')
    assignments = assignment_info('assignments.txt')
    submissions = submission_info('submissions')

    menu_option = input(f'''1. Student grade
2. Assignment statistics
3. Assignment graph
''')
    if menu_option == '1':
        student_overall_grade(students, assignments, submissions)
        main()

    if menu_option == '2':
        assignment_statistics(assignments, submissions)
        main()

    if menu_option == '3':
        return assignment_graph(assignments, submissions)



if __name__ == '__main__':
    main()