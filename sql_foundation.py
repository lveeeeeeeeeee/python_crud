from sql_config import *
import psycopg2


def randomword(length):
    import random, string
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def read_cfg():
    from configparser import ConfigParser

    cfg = ConfigParser()
    cfg.read(config_path)

    host = cfg.get('main', 'host')
    port = cfg.get('main', 'port')
    username = cfg.get('main', 'username')
    password = cfg.get('main', 'password')
    db_name = cfg.get('main', 'db_name')
    return host, port, username, password, db_name


host, port, username, password, db_name = read_cfg()


def _default_handler(e: Exception):
    print(e.args[0])


def safe_connection(func, handle = _default_handler):

    def _wrapper(*args, **kwargs):
        cursor = None
        connection = None

        try:
            host, port, username, password, db_name = read_cfg()
            connection = psycopg2.connect(
                database = db_name,
                user = username,
                password = password,
                host = host,
                port = port
            )
            cursor = connection.cursor()
            result = func(cursor, **kwargs)
            connection.commit()
            return result
                
        except Exception as error:
            handle(error)
            if connection:
                connection.rollback()
        
        finally:
            if cursor is not None:
                cursor.close()
            if connection is not None:
                connection.close()
        
    return _wrapper


def check_connection(host, port, username, pwd, db_name, handler=_default_handler):
    try:
        connect = psycopg2.connect(
            database = db_name,
            user = username,
            password = pwd,
            host = host,
            port = port
        )
        return True

    except Exception as e:
        handler(e)
        return False
    
    finally:
        if connect != None:
            connect.close()


def check_from_cfg(handler=_default_handler):
    try:
        host, port, username, password, db_name = read_cfg()
        connect = psycopg2.connect(
            database = db_name,
            user = username,
            password = password,
            host = host,
            port = port
        )
        return True

    except Exception as e:
        handler(e)
        return False
    
    finally:
        if connect != None:
            connect.close()


def ret_connection(handler):
    try:
        host, port, username, password, db_name = read_cfg()
        connection = psycopg2.connect(
            database = db_name,
            user = username,
            password = password,
            host = host,
            port = port
        )
        return connection

    except Exception as e:
        handler()


@safe_connection
def create_db(cursor):
    cursor.execute(
        f"""DROP DATABASE IF EXISTS demo_school;
            CREATE DATABASE demo_school"""
        )


def _gen_table_query(names: list, attr_properties: list):
    diff = abs(len(names) - len(attr_properties))
    result = ""
    
    for i in range(diff):
        if len(names) > len(attr_properties):
            attr_properties.append("BLOB")
        if len(names) < len(attr_properties):
            names.append(f"defaultname{i+diff+1}")
    
    for i in range(len(names)):
        result += f"{names[i]} {attr_properties[i]}"
        if i+1 < len(names):
            result += ", "

    return result


@safe_connection
def create_table(
    cursor, name="default", 
    attr_names = ['default1'], attr_props = ["BLOB"],
    ):

    query_add = _gen_table_query(attr_names, attr_props)

    cursor.execute(f"""CREATE TABLE IF NOT EXISTS {name} (
        {query_add}
        )"""
        )


@safe_connection
def foreign_keys(cursor, table_name=None, fk=None):
    if table_name != None and fk != None:
        for i in range(len(fk)):
            query = f"""ALTER TABLE {fk_tablenames[i]} 
                ADD COLUMN {fk[i][0]} BIGSERIAL
                REFERENCES {fk[i][1]};"""
            cursor.execute(query)
            print(f"{fk[i][1]} in {fk_tablenames[i]}")


def pack_insert_query_vals(to_pack=[], brackets=True):
    packed = ""
    for i in range(len(to_pack)):
        if i == 0 and brackets:
            packed += " ("
        
        packed += f"{to_pack[i]}"
        
        if i == len(to_pack) - 1 and brackets:
            packed += ") "
        elif i == len(to_pack) - 1:
            packed += " "
        else:
            packed += ", "
    return packed


@safe_connection
def insert_into_table(
    cursor, table_name=None, attrs=None, 
    values=None, attrs_brackers=True, values_brackets=True
    ):
    """
    """
    attrs = pack_insert_query_vals(attrs, attrs_brackers)
    values = pack_insert_query_vals(values, values_brackets)
    cursor.execute(f"""INSERT INTO {table_name}{attrs} VALUES{values}""")


@safe_connection
def alter_pk(cursor, tablename="", pk_name=""):
    try:
        cursor.execute(
            f"""ALTER TABLE {tablename} DROP COLUMN {pk_name} CASCADE"""
            )
        cursor.execute(
            f"""ALTER TABLE {tablename} 
            ADD COLUMN {pk_name} BIGSERIAL PRIMARY KEY"""
            )
    
    except Exception as e:
        print("too bad mate,", e.args[0])


@safe_connection
def select(cursor, to_select="*", tablename="", cond="", limit=1, offset=""):
    query = f"""SELECT {to_select} FROM {tablename} """
    if cond != "":
        query += f"WHERE {cond} "
    if limit > 0:
        query += f"LIMIT {limit} "
    if offset != "":
        query += offset
    cursor.execute(query)
    result = cursor.fetchall()
    return result


def _pack_conditions(cond=[]):
    query = ""
    for i in range(len(cond)):
        if i > 0:
            query += "AND "
        query += f"{cond[i]} "
    return query


@safe_connection
def delete_from_table(cursor, tablename="", cond=[]):
    cond = _pack_conditions(cond)
    query = f"""DELETE FROM {tablename} """
    if cond != "":
        query += f"WHERE {cond}"
    cursor.execute(query)


def _pack_update_vals(vals=[], columns=[]):
    query = ""
    for i in range(len(vals)):
        if i > 0:
            query += ", "
        query += f"{columns[i]} = {vals[i]} "
    return query


@safe_connection
def update_table(cursor, tablename="", columns=[], vals=[], cond=[]):
    cond = _pack_conditions(cond)
    vals = _pack_update_vals(columns=columns, vals=vals)
    query = f"UPDATE {tablename} "
    if vals != "":
        query += f"SET {vals}"
    if cond != "":
        query += f"WHERE {cond}"
    cursor.execute(query)


@safe_connection
def unique(cursor, tablename="", columns = ""):
    cursor.execute(f"ALTER TABLE {tablename} ADD UNIQUE {columns}")


def init():
    for i in range(len(tablenames)):
        create_table(
            None, 
            name=tablenames[i],
            attr_names=atts[i],
            attr_props=types[i]
            )

    # for i in range(len(pks)):
    #     alter_pk(None, tablename=tablenames[i], pk_name=pks[i])

    foreign_keys(None, table_name=fk_tablenames, fk=fk_dict)


def input_data():
    from random import randint
    sex = randint(0, 1) * 3
    
    for i in range(len(subjects)):
        insert_into_table(
            None, table_name="subjects", 
            attrs=[att_subjects[1]],
            values=[f"'{subjects[i]}'"]
            )
    
    for i in range(len(groups)):
        insert_into_table(
            None, table_name="stud_groups",
            attrs=[att_groups[1]],
            values=[f"'{groups[i]}'"]
        )

    for i in range(100):
        insert_into_table(
            None, table_name="students",
            attrs=[*att_students, "group_id"],
            values=[
                f"{i+1}",
                f"'{people[sex][randint(0, len(people[sex]))-1]}'",
                f"'{people[sex+1][randint(0, len(people[sex+1]))-1]}'",
                f"'{people[sex+2][randint(0, len(people[sex+2]))-1]}'",
                f"{randint(1, len(groups))}"
            ]
        )
        sex = randint(0, 1) * 3
    
    for i in range(10):
        insert_into_table(
            None, table_name="teachers",
            attrs=att_teachers,
            values=[
                f"{i+1}",
                f"'{people[sex][randint(0, len(people[sex]))-1]}'",
                f"'{people[sex+1][randint(0, len(people[sex+1]))-1]}'",
                f"'{people[sex+2][randint(0, len(people[sex+2]))-1]}'",
            ]
        )
        sex = randint(0, 1) * 3
    
    for tablename, attrs in uniques.items():
        unique(None, tablename=tablename, columns=attrs)

    for i in range(50):
        insert_into_table(
            None, table_name=name_st_sub,
            attrs=[
                "relation_id", 
                "student_id",
                "subject_id"],
            values=[
                f"{i+1}",
                f"{randint(1, 50)}",
                f"{randint(1, len(subjects))}",
            ]
        )

    for i in range(50):
        insert_into_table(
            None, table_name=name_st_teach,
            attrs=[
                "relation_id", 
                "student_id",
                "teacher_id"],
            values=[
                f"{i+1}",
                f"{randint(1, 50)}",
                f"{randint(1, 10)}"
            ]
        )

    for i in range(50):
        insert_into_table(
            None, table_name=name_sub_teach,
            attrs=[
                "relation_id", 
                "subject_id",
                "teacher_id"],
            values=[
                f"{i+1}",
                f"{randint(1, len(subjects))}",
                f"{randint(1, 10)}"
            ]
        )
    
    for i in range(50):
        insert_into_table(
            None, table_name=name_tests,
            attrs=[
                "test_id", 
                "test_name",
                "subject_id"],
            values=[
                f"{i+1}",
                f"'{randomword(4)}'",
                f"{randint(1, len(subjects))}"
            ]
        )
    
    for i in range(50):
        insert_into_table(
            None, table_name=name_grades,
            attrs=[
                "grade_id", 
                "grade",
                "test_id",
                "student_id"
                ],
            values=[
                f"{i+1}",
                f"{randint(1, 10)}",
                f"{randint(1, 50)}",
                f"{randint(1, 50)}"
            ]
        )


@safe_connection
def drop_schema(cursor):
    cursor.execute("""DROP SCHEMA public CASCADE; CREATE SCHEMA public""")


def main(_):
    """
    The main function.
    """
    drop_schema()
    init()
    input_data()


# queries
@safe_connection
def query_groups_amount(cursor):
    drop_query_results(cursor)
    cursor.execute("""
        SELECT foo.group_name, count(*) 
        INTO query_result
        FROM 
        (SELECT student_name, stud_groups.group_name FROM students
        JOIN stud_groups ON students.group_id = stud_groups.group_id) AS foo
        GROUP BY foo.group_name
    """)


@safe_connection
def query_subjects_amount(cursor):
    drop_query_results(cursor)
    cursor.execute(f"""
        select 
        subjects.subject_name, count(students_subjects.subject_id) as students_amount
        into query_result
        from subjects
        join students_subjects on subjects.subject_id = students_subjects.subject_id
        group by subjects.subject_id
        order by subjects.subject_id;
        """)


@safe_connection
def query_avg_grades(cursor):
    drop_query_results(cursor)
    cursor.execute("""
        select students.student_name as name, 
        students.student_surname as surname,
        students.student_patronymic as patronymic,
        stud_groups.group_name,
        avg(grade) 
        into query_result
        from grades
        join students on grades.student_id = students.student_id
        join stud_groups on stud_groups.group_id = students.group_id
        group by grades.student_id, students.student_name, 
        students.student_surname,
        students.student_patronymic,
        stud_groups.group_name
        """)


@safe_connection
def query_avg_grades_for_subjects(cursor):
    drop_query_results(cursor)
    cursor.execute("""
        select foo.subject, foo.grade, foo.subject_id
		into query_result
		from (
        select
        avg(grades.grade) as grade, subjects.subject_name as subject,
        subjects.subject_id
        from grades
        join tests on tests.test_id = grades.test_id
        join subjects on subjects.subject_id = tests.subject_id
        group by subject, subjects.subject_id) as foo
        group by foo.subject, foo.grade, foo.subject_id     
        """)


@safe_connection
def query_students_amount(cursor):
    drop_query_results(cursor)
    cursor.execute("""
        select 
        teachers.teacher_name, teachers.teacher_surname, 
        teachers.teacher_patronymic, count(students_teachers.teacher_id) as students_count
        into query_result
        from teachers
        join students_teachers on teachers.teacher_id = students_teachers.teacher_id
        group by teachers.teacher_id
        """)


@safe_connection
def drop_query_results(cursor):
    cursor.execute("drop table if exists query_result")


if __name__ == "__main__":
    main(None)