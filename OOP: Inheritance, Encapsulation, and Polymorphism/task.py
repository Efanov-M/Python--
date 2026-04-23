# Исходя из квиза к предыдущему занятию, у нас уже есть класс преподавателей и класс студентов (вы можете взять этот код за основу или написать свой). Студентов пока оставим без изменения, а вот преподаватели бывают разные, поэтому теперь класс Mentor должен стать родительским классом, а от него нужно реализовать наследование классов Lecturer (лекторы) и Reviewer (эксперты, проверяющие домашние задания). Очевидно, имя, фамилия и список закрепленных курсов логично реализовать на уровне родительского класса. А чем же будут специфичны дочерние классы? Об этом в следующих заданиях. А пока можете проверить, что успешно реализовали дочерние классы

# В квизе к предыдущей лекции мы реализовали возможность выставлять студентам оценки за домашние задания. Теперь это могут делать только Reviewer (реализуйте такой метод)! А что могут делать лекторы? Получать оценки за лекции от студентов :) Реализуйте метод выставления оценок лекторам у класса Student (оценки по 10-балльной шкале, хранятся в атрибуте-словаре у Lecturer, в котором ключи – названия курсов, а значения – списки оценок). Лектор при этом должен быть закреплен за тем курсом, на который записан студент.

# Перегрузите магический метод __str__ у всех классов.
# У проверяющих он должен выводить информацию в следующем виде:
# print(some_reviewer)
# Имя: Some
# Фамилия: Buddy
# У лекторов:
# print(some_lecturer)
# Имя: Some
# Фамилия: Buddy
# Средняя оценка за лекции: 9.9
# А у студентов так:
# print(some_student)
# Имя: Ruoy
# Фамилия: Eman
# Средняя оценка за домашние задания: 9.9
# Курсы в процессе изучения: Python, Git
# Завершенные курсы: Введение в программирование

# Реализуйте возможность сравнивать (через операторы сравнения) между собой лекторов по средней оценке за лекции и студентов по средней оценке за домашние задания.

# Создайте по 2 экземпляра каждого класса, вызовите все созданные методы, а также реализуйте две функции:

# для подсчета средней оценки за домашние задания по всем студентам в рамках конкретного курса (в качестве аргументов принимаем список студентов и название курса);
# для подсчета средней оценки за лекции всех лекторов в рамках курса (в качестве аргумента принимаем список лекторов и название курса).

class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def rate_lecturer(self, lecturer, course, grade):
        if (isinstance(lecturer, Lecturer) and course in self.courses_in_progress and course in lecturer.courses_attached):
            if course in lecturer.course_grades:
                lecturer.course_grades[course].append(grade)
            else:
                lecturer.course_grades[course] = [grade]
        else:
            return 'Ошибка'

    def get_middl_grade_all_course(self):
        """
        Возращаем среднее значение по всем оценка

        """
        grades = []
        for grade in self.grades.values():
            grades.extend(grade)
        if not grades:
            return 0
        return sum(grades) / len(grades)

    def get_all_grade_course(self, course):
        """
        Возвращаем все оценки по одному курсу
        """
        if course in self.grades:
            return self.grades[course]
        else:
            return []

    def __eq__(self, other):
        """
        Сравниваем среднюю оценку одного студента с другим
        """
        if not isinstance(other, Student):
            return NotImplemented
        return self.get_middl_grade_all_course() == other.get_middl_grade_all_course()

    def __lt__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self.get_middl_grade_all_course() < other.get_middl_grade_all_course()

    def __str__(self) -> str:
        """
        Формируем строку для вывода в печать:
        Имя: Ruoy
        Фамилия: Eman
        Средняя оценка за домашние задания: 9.9
        Курсы в процессе изучения: Python, Git
        Завершенные курсы: Введение в программирование

        """
        print_ = []
        print_.append(f'Имя: {self.name}')
        print_.append(f'Фамилия: {self.surname}')
        middel_grades = self.get_middl_grade_all_course()
        print_.append(f'Средняя оценка за домашние задания : {middel_grades}')
        print_.append(f'Курсы в процессе обучения: {','.join(self.courses_in_progress)}')
        print_.append(f'Завершенные курсы: {','.join(self.finished_courses)}')
        return '\n'.join(print_)

class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer (Mentor):

    def __init__(self, name, surname,):
        super().__init__(name, surname)
        self.course_grades = {}

    def get_middl_grade(self):
        """
       Возвращаем среднюю оценку
        """

        grades = []
        for grade in self.course_grades.values():
            grades.extend(grade)
        if not grades:
            return 0
        return sum(grades) / len(grades)

    def __eq__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self.get_middl_grade() == other.get_middl_grade()
    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self.get_middl_grade() < other.get_middl_grade()

    def __str__(self) -> str:
        """
        Формируем строку для вывода в печать:
        Имя: Some
        Фамилия: Buddy
        Средняя оценка за лекции: 9.9

        """
        print_ = []
        print_.append(f'Имя: {self.name}')
        print_.append(f'Фамилия: {self.surname}')
        middl_grade = self.get_middl_grade()
        print_.append(f'Средняя оценка за лекции : {middl_grade}')
        return '\n'.join(print_)



class Reviewer (Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)

    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self) -> str:
        """
        Формируем строку для вывода в печать:
        Имя: Some
        Фамилия: Buddy
        """
        print_ = []
        print_.append(f'Имя: {self.name}')
        print_.append(f'Фамилия: {self.surname}')
        return '\n'.join(print_)

def average_hw_grade_by_course(students: list, course:str):
        """
        Получаем среднуюю оценку по списку студентов для определенного кураса
        """
        middl_grade = []
        if students:
            for student in students:
                grades = student.get_all_grade_course(course)
                middl_grade.extend(grades)
            if not middl_grade:
                return 0
            return sum(middl_grade) / len(middl_grade)
        else:
            raise ValueError('Список студентов пуст')

def average_lecture_grade_by_course(lecturers: list, course: str):
    """
    Получаем среднюю оценку по списку лекторов и определенному курсу
    """
    all_grades = []

    for lecturer in lecturers:
        if course in lecturer.course_grades:
            all_grades.extend(lecturer.course_grades[course])

    if not all_grades:
        return 0

    return sum(all_grades) / len(all_grades)


lecturer_1 = Lecturer('Иван', 'Грозный')
lecturer_2 = Lecturer('Петр', 'Романов')
lecturer_1.courses_attached += ['Python', 'C++', 'Go']
lecturer_2.courses_attached += ['Python', 'JS', 'Java']

reviewer_1 = Reviewer('Григорий', 'Потемкин')
reviewer_2 = Reviewer('Алексей', 'Толстой')
reviewer_1.courses_attached += ['Go', 'C++']
reviewer_2.courses_attached += ['Python', 'JS', 'Java']

student_1 = Student('Николай','Миклухомаклай', 'М')
student_2 = Student('Мария','Медичи', 'ЖЕН')
student_1.courses_in_progress += ['Python', 'Java', 'JS']
student_2.courses_in_progress += ['Go']

student_1.rate_lecturer(lecturer_1, 'Python', 8)
student_1.rate_lecturer(lecturer_1, 'Python', 9)
student_2.rate_lecturer(lecturer_2, 'Go', 7)

print(lecturer_1.course_grades) #{'Python': [8, 9]}
print(lecturer_2.course_grades) # {}

reviewer_1.rate_hw(student_1, 'Python', 10)
reviewer_1.rate_hw(student_1, 'Python', 9)

print(student_1.grades) #{'Python': [10, 9]}

print(student_1.get_middl_grade_all_course())
print(lecturer_1.get_middl_grade())


