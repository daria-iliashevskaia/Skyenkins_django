import psycopg2


def db_create():
    """
    Создание базы данных 'solopharm'
    """
    conn = psycopg2.connect(dbname="postgres", user="postgres", password="19IDD93a", host="127.0.0.1")
    cursor = conn.cursor()

    conn.autocommit = True

    create_request = """CREATE DATABASE solopharm"""

    cursor.execute(create_request)
    print("База данных успешно создана")

    cursor.close()
    conn.close()


def create_tables():
    conn = psycopg2.connect(dbname="solopharm", user="postgres", password="19IDD93a", host="127.0.0.1")
    cursor = conn.cursor()

    conn.autocommit = True

    create_group_table_request = """CREATE TABLE group_table
                                    (id SERIAL PRIMARY KEY,
                                    name VARCHAR(50))"""

    cursor.execute(create_group_table_request)
    print("Таблица group_table успешно создана")

    create_subgroup_table_request = """CREATE TABLE subgroup_table
                                    (id SERIAL PRIMARY KEY,
                                    name VARCHAR(50))"""

    cursor.execute(create_subgroup_table_request)
    print("Таблица subgroup_table успешно создана")

    create_fed_okrug_table_request = """CREATE TABLE fed_okrug
                                    (id SERIAL PRIMARY KEY,
                                    name VARCHAR(50))"""

    cursor.execute(create_fed_okrug_table_request)
    print("Таблица fed_okrug успешно создана")

    create_fed_subject_table_request = """CREATE TABLE fed_subject
                                    (id SERIAL PRIMARY KEY,
                                    name VARCHAR(50),
                                    okrug_name_id INTEGER REFERENCES fed_okrug(id))"""

    cursor.execute(create_fed_subject_table_request)
    print("Таблица fed_subject успешно создана")

    create_product_table_request = """CREATE TABLE product_table
                                    (id SERIAL PRIMARY KEY,
                                    name VARCHAR(240),
                                    group_id INTEGER REFERENCES group_table(id),
                                    subgroup_id INTEGER REFERENCES subgroup_table(id))"""

    cursor.execute(create_product_table_request)
    print("Таблица product_table успешно создана")

    create_fact_table_request = """CREATE TABLE fact_table
                                    (id SERIAL PRIMARY KEY,
                                    product_id INTEGER REFERENCES product_table(id),
                                    corporation VARCHAR(240),
                                    sum_sell FLOAT,
                                    amount_sell FLOAT,
                                    price_sell FLOAT,
                                    fed_subject INTEGER REFERENCES fed_subject(id),
                                    year INTEGER,
                                    month VARCHAR(50))"""

    cursor.execute(create_fact_table_request)
    print("Таблица fact_table успешно создана")

    cursor.close()
    conn.close()


def fill_tables():

    conn = psycopg2.connect(dbname="solopharm", user="postgres", password="19IDD93a", host="127.0.0.1")
    cursor = conn.cursor()

    conn.autocommit = True

    with open('fed_okrug.csv', 'r', encoding="utf-8") as f:
        next(f)
        cursor.copy_from(f, 'fed_okrug', sep=',')

    with open('fed_subject.csv', 'r', encoding="utf-8") as f:
        next(f)
        cursor.copy_from(f, 'fed_subject', sep=',')

    with open('group_table.csv', 'r', encoding="utf-8") as f:
        next(f)
        cursor.copy_from(f, 'group_table', sep=',')

    with open('subgroup_table.csv', 'r', encoding="utf-8") as f:
        next(f)
        cursor.copy_from(f, 'subgroup_table', sep=',')

    with open('product_table.csv', 'r', encoding="utf-8") as f:
        next(f)
        cursor.copy_from(f, 'product_table', sep=',')

    with open('fact_table.csv', 'r', encoding="utf-8") as f:
        next(f)
        cursor.copy_from(f, 'fact_table', sep=',')

    cursor.close()
    conn.close()
