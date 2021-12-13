import csv
import sys


def read_csv(file_name):
    row_list = []
    with open(file_name, mode='r') as csv_file:
        reader = csv.reader(csv_file)
        count = 0
        for row in reader:
            count += 1
            row_list.append(row)
            print(count)
            if count == int(sys.argv[2]) + 1:
                break
        return row_list


def write_csv(rows):
    with open('test' + str(sys.argv[2]) + 'articles.csv', mode='w') as file:
        file_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in rows:
            file_writer.writerow(row)


if __name__ == "__main__":

    raw_col_data = []

    if len(sys.argv) == 3:
        print(sys.argv[2])
        raw_col_data = read_csv(sys.argv[1])
        write_csv(raw_col_data)
