import pandas as pd
from db_fill import db_create, create_tables, fill_tables


def fed_okrug_table_form():
    """
    Создание датафрейма с данными о федеральных округах и их запись в "fed_okrug.csv"
    """

    df3 = pd.read_csv('Рыночные данные.csv', on_bad_lines='skip', sep=';', engine='python')

    okrug_list = df3['Брики2.Федеральный округ'].unique()
    fed_okrug_table = pd.DataFrame({
            'name': okrug_list})

    fed_okrug_table.index.rename('id', inplace=True)

    fed_okrug_table.to_csv('fed_okrug.csv')


def fed_subject_table_form():
    """
    Создание датафрейма с данными о федеральных субъектах (без проставления ФК)
    """

    df3 = pd.read_csv('Рыночные данные.csv', on_bad_lines='skip', sep=';', engine='python')

    unique_subject_okrug_list = pd.unique(list(zip(df3['Брики3.Субъект Федерации'],
                                                   df3['Брики2.Федеральный округ'])))
    subject_list = []
    okrug_list = []

    for i in unique_subject_okrug_list:
        subject_list.append(i[0])
        okrug_list.append(i[1])

    subject_table = pd.DataFrame(
        {
            'name': subject_list,
            'okrug_name': okrug_list}
    )

    subject_table.index.rename('id', inplace=True)

    return subject_table


def fed_subject_table_fk(subject_table):
    """
    Принимает заполненный датафрейм из fed_subject_table_form()
    Заполняет ФК для столбца "okrug_name" в таблице fed_subject и записывает его в 'fed_subject.csv'
    """

    df = pd.read_csv('fed_okrug.csv', on_bad_lines='skip', sep=',', engine='python')

    data = df.to_dict('records')
    new_dict = {}
    for d in data:
        new_dict[d['name']] = d['id']

    subject_table["okrug_name"] = subject_table["okrug_name"].map(new_dict)
    subject_table.to_csv('fed_subject.csv')


def group_table_form():
    """
    Создание датафрейма с данными о группах лекарственных средств
    и его запись в файл 'group_table.csv'
    """

    df3 = pd.read_csv('Рыночные данные.csv', on_bad_lines='skip', sep=';', engine='python')

    group_list = df3['Группа'].unique()
    group_table = pd.DataFrame({
            'name': group_list})

    group_table.index.rename('id', inplace=True)

    group_table.to_csv('group_table.csv')


def subgroup_table_form():
    """
    Создание датафрейма с данными о подгруппах лекарственных средств
    и его запись в файл 'subgroup_table.csv'
    """

    df3 = pd.read_csv('Рыночные данные.csv', on_bad_lines='skip', sep=';', engine='python')

    subgroup_list = df3['Сегмент'].unique()
    subgroup_table = pd.DataFrame({
            'name': subgroup_list})

    subgroup_table.index.rename('id', inplace=True)

    subgroup_table.to_csv('subgroup_table.csv')


def product_table_form():
    """
    Создание датафрейма с данными о продуктах
    """
    df3 = pd.read_csv('Рыночные данные.csv', on_bad_lines='skip', sep=';', engine='python')

    product_df = df3[['Торговое наименование', 'Группа', 'Сегмент']].copy()
    product_df = product_df.drop_duplicates()

    product_df.rename(columns={'Торговое наименование': 'name', 'Группа': 'group', 'Сегмент': 'subgroup'}, inplace=True)
    product_df.index.rename('id', inplace=True)

    return product_df


def product_table_fk(product_df, fk_table, column, filename):
    """
    Заполняет ФК для таблицы с продуктами.
    Принимает:
    - product_df: датафрейм, в котором нужно проставлять ФК
    - fk_table: датафрейм, на который ссылается ФК
    - column: колонка, в которой будет проставлен ФК
    - filename: имя файла, в который будет записан итоговый датафрейм
    """

    df = pd.read_csv(fk_table, on_bad_lines='skip', sep=',', engine='python')

    data = df.to_dict('records')
    new_dict = {}
    for d in data:
        new_dict[d['name']] = d['id']

    product_df[column] = product_df[column].map(new_dict)
    product_df.to_csv(filename)


def fact_table_form():
    """
    Создание датафрейма с фактами продаж
    """

    df3 = pd.read_csv('Рыночные данные.csv', on_bad_lines='skip', sep=';', engine='python')

    fact_table = df3.copy(deep=True)

    fact_table.drop(columns=['Source.Name',
                             'Бренд',
                             'Компания',
                             'Календарь.Неделя',
                             'Год2',
                             'Год-Неделя',
                             'Календарь.Квартал',
                             'Неделя',
                             'Фасовка',
                             'Дозировка',
                             'NFC.Описание 2',
                             'NFC.Описание 3',
                             'Брики2.Федеральный округ',
                             'ЛС.МНН',
                             'Сумма, руб. экстраполяция',
                             'Количество, уп. экстраполяция',
                             'Сегмент',
                             'Группа'],
                    axis=1,
                    inplace=True)

    fact_table.rename(columns={'Торговое наименование': 'name',
                               'ЛС.Корпорация': 'corporation',
                               'Sell Out Сумма, RUB': 'sum_sell',
                               'Sell  Out Количество, уп.': 'amount_sell',
                               'Sell  Out Цена, RUB': 'price_sell',
                               'Брики3.Субъект Федерации': 'fed_subject',
                               'Год': 'year',
                               'Календарь.Месяц': 'month'},
                      inplace=True)

    fact_table.index.rename('id', inplace=True)

    fact_table['sum_sell'] = fact_table['sum_sell'].str.replace(',', '.')
    fact_table['sum_sell'] = pd.to_numeric(fact_table['sum_sell'], errors='coerce')

    fact_table['price_sell'] = fact_table['price_sell'].str.replace(',', '.')
    fact_table['price_sell'] = pd.to_numeric(fact_table['price_sell'], errors='coerce')

    fact_table['year'] = pd.to_numeric(fact_table['year'], errors='coerce')

    return fact_table


def fact_table_fk(fact_table):
    """
    Заполняет фк для столбцов "fed_subject" и "name" в таблице fact_table
    и записывает его в 'fact_table.csv'
    """

    df = pd.read_csv('fed_subject.csv', on_bad_lines='skip', sep=',', engine='python')

    data = df.to_dict('records')
    new_dict = {}
    for d in data:
        new_dict[d['name']] = d['id']

    fact_table["fed_subject"] = fact_table["fed_subject"].map(new_dict)

    df = pd.read_csv('product_table.csv', on_bad_lines='skip', sep=',', engine='python')

    data = df.to_dict('records')
    new_dict = {}
    for d in data:
        new_dict[d['name']] = d['id']

    fact_table["name"] = fact_table["name"].map(new_dict)

    fact_table.to_csv('fact_table.csv')


if __name__ == "__main__":

    # создание csv с округами
    fed_okrug_table_form()

    # создание csv с субъектами и замена фк округов
    subject_table = fed_subject_table_form()
    fed_subject_table_fk(subject_table)

    # создание csv с группами и подгруппами
    group_table_form()
    subgroup_table_form()

    # создание дф с продуктами, замена группы и подгруппы на фк и создание таблицы с продуктами в csv
    product_table = product_table_form()
    product_table_fk(product_table, 'group_table.csv', 'group', 'product_table.csv')
    product_table_fk(product_table, 'subgroup_table.csv', 'subgroup', 'product_table.csv')

    # создание дф с фактами продаж,
    # замена фк субъектов и фк продуктов в таблице фактов и создание таблицы с фактами в csv
    fact_table = fact_table_form()
    fact_table_fk(fact_table)

    # создание БД
    db_create()

    # создание таблиц в БД
    create_tables()

    # заполнение таблиц данными
    fill_tables()



