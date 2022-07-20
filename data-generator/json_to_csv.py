import csv
import json


def write_json_to_csv(csv_file_name, json_obj):
    # columns = [x for row in json_obj for x in row.keys()]
    # columns = sorted(list(set(columns)))
    columns = ['timestamp', 'total_seconds_elapsed', 'movement', 'status']
    print('json-', columns)

    with open(csv_file_name, "w", newline="") as f:  # python 2: open("output.csv","wb")
        cw = csv.DictWriter(f, columns, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        cw.writeheader()
        cw.writerows(json_obj)
