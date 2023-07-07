host = "localhost"
port = 5432
username = "postgres"
password = "^2gXq}:G3O_OwKV-uN]'N@]^U'"
db_name = "postgres"

# lists of attribute names and their types

import os
config_path = os.path.join(os.path.dirname(__file__), 'config.ini')

name_teachers = "teachers"
pk_teachers = "teacher_id"
att_teachers = [
    "teacher_id", 
    "teacher_name",
    "teacher_surname",
    "teacher_patronymic"
]
type_teachers = [
    "BIGSERIAL PRIMARY KEY",
    "TEXT NOT NULL",
    "TEXT NOT NULL",
    "TEXT"
]

name_students = "students"
pk_students = "student_id"
att_students = [
    "student_id", 
    "student_name",
    "student_surname",
    "student_patronymic"
]
type_students = [
    "BIGSERIAL PRIMARY KEY",
    "TEXT NOT NULL",
    "TEXT NOT NULL",
    "TEXT"
]

name_subjects = "subjects"
pk_subjects = "subject_id"
att_subjects = ["subject_id", "subject_name"]
type_subjects = ["BIGSERIAL PRIMARY KEY","TEXT NOT NULL UNIQUE"]

name_groups = "stud_groups"
pk_groups = "group_id"
att_groups = ["group_id","group_name"]
type_groups = ["BIGSERIAL PRIMARY KEY", "TEXT NOT NULL UNIQUE"]

name_grades = "grades"
pk_grades = "grade_id"
att_grades = ["grade_id", "grade"]
type_grades = ["BIGSERIAL PRIMARY KEY", "INTEGER NOT NULL"]

name_tests = "tests"
pk_tests = "test_id"
att_tests = ["test_id", "test_name"]
type_tests = ["BIGSERIAL PRIMARY KEY", "TEXT NOT NULL"]

name_st_sub = "students_subjects"
pk_st_sub = "relation_id"
att_st_sub = ["relation_id"]
type_st_sub = ["BIGSERIAL PRIMARY KEY"]

name_st_teach = "students_teachers"
pk_st_teach = "relation_id"
att_st_teach = ["relation_id"]
type_st_teach = ["BIGSERIAL PRIMARY KEY"]

name_sub_teach = "subjects_teachers"
pk_sub_teach = "relation_id"
att_sub_teach = ["relation_id"]
type_sub_teach = ["BIGSERIAL PRIMARY KEY"]

fk_dict = [
    ("teacher_id", "teachers (teacher_id)"),
    ("teacher_id", "teachers (teacher_id)"),
    ("student_id", "students (student_id)"),
    ("student_id", "students (student_id)"),
    ("student_id", "students (student_id)"),
    ("subject_id", "subjects (subject_id)"),
    ("subject_id", "subjects (subject_id)"),
    ("subject_id", "subjects (subject_id)"),
    ("group_id", "stud_groups (group_id)"),
    ("test_id", "tests (test_id)")
]
fk_tablenames = [name_st_teach, name_sub_teach, name_st_teach, name_st_sub, name_grades, name_st_sub, name_sub_teach, name_tests, name_students, name_grades]

uniques = {
    name_grades: "(grade, student_id, test_id)",
    name_st_sub: "(student_id, subject_id)",
    name_st_teach: "(teacher_id, student_id)",
    name_sub_teach: "(teacher_id, subject_id)",
    name_tests: "(test_name, subject_id)",
}

tablenames = [
    name_grades, name_groups, name_st_sub, name_st_teach,
    name_students, name_sub_teach, name_subjects, name_teachers,
    name_tests
]
pks = [
    pk_grades, pk_groups, pk_st_sub, pk_st_teach,
    pk_students, pk_sub_teach, pk_subjects, pk_teachers,
    pk_tests
]
atts = [
    att_grades, att_groups, att_st_sub, att_st_teach,
    att_students, att_sub_teach, att_subjects, att_teachers,
    att_tests
]
types = [
    type_grades, type_groups, type_st_sub, type_st_teach,
    type_students, type_sub_teach, type_subjects, type_teachers,
    type_tests
]


men_names=[
    "Борис", "Борислав", "Бронислав", "Будимир", "Вавила", 
    "Вадим", "Валентин", "Валериан", "Валерий", "Варлам", 
    "Варламий", "Варнава", "Варсоноф", "Варсонофий", "Варфоломей"
]
men_surnames=[
    "Иванов", "Смирнов", "Кузнецов", "Попов", "Васильев", 
    "Петров", "Соколов", "Михайлов", "Новиков", "Фёдоров", 
    "Морозов", "Волков", "Алексеев", "Лебедев", "Семенов"
]
men_patr=[
    "Донатович", "Доримедонтович", "Дормедонтович", "Дормидонтович", "Дорофеевич",
    "Евсеевич", "Елизарович", "Зосимич", "Иакимович", "Карпович",
]


women_names=[
    "Августа", "Августина", "Авдотья", "Аврелия", "Аврея", 
    "Аврора", "Агапа", "Агапия", "Агарь", "Агата", 
    "Агафа", "Агафоклия", "Агафоника", "Агафья", "Аглаида"
]
women_surnames=[
    "Иванова", "Петрова", "Смирнова", "Кузнецова", "Васильева",
    "Попова", "Новикова", "Волкова", "Романова", "Козлова",
    "Соколова", "Андреева", "Морозова", "Николаева", "Михайлова"
]
women_patr=[
    "Донатовна", "Доримедонтовна", "Дормедонтовна", "Дорофеевна", "Дормидонтовна",
    "Карповна", "Лавровна", "Маевна", "Наркисовна", "Осиповна"
]


people = [
    men_names, men_surnames, men_patr, 
    women_names, women_surnames, women_patr
]

groups = [
    "ji83", "ПР_28к30", "ЩКШ-02", "ООАОА_2022", "ГАБ-16", 
    "FJH22", "A205", "fhEW340", "АББ-12-1", "GEG2021"
]

subjects = [
    "русский язык", "литература", "математика", "иностранный язык", 
    "история", "физическая культура", "музыка", "технология"
]

from configparser import ConfigParser
config = ConfigParser()

config.read(config_path)
if config.has_section('main') == False:
    config.add_section('main')
config.set('main', 'host', host)
config.set('main', 'port', f"{port}")
config.set('main', 'username', username)
config.set('main', 'db_name', db_name)
config.set('main', 'password', password)

with open(config_path, 'w') as f:
    config.write(f)