import os


def create_temp_folder():
    print('-- start to create folder')
    try:
        os.makedirs('data/temp')
        print('-- temp folder created successfully')
    except FileExistsError:
        print('-- folder already ready')


def save_data_to_little_file(data, counter):
    print(f'-- save data to temp file with number {counter}')
    with open(f'data/temp/{counter}.csv', 'w+', encoding='utf-8') as little_file_with_data:
        little_file_with_data.writelines(data)


def file_divider(file_name, batch_size):
    print(f'-- start to divide big file to little by {batch_size} count lines')
    create_temp_folder()
    batches_count = 0
    lines_counter = 0
    with open(f'{file_name}', encoding='utf-8') as whole_data_file:
        header = next(whole_data_file)
        data_for_save = [header]
        for row in whole_data_file:
            if lines_counter >= batch_size:
                lines_counter = 0
                batches_count += 1
                save_data_to_little_file(data_for_save, batches_count)
                data_for_save = [header]

            data_for_save.append(row)
            lines_counter += 1
        batches_count += 1
        if len(data_for_save) > 0:
            save_data_to_little_file(data_for_save, batches_count)

    return batches_count

file_divider("rnc_report_2_2020.csv", 15000)