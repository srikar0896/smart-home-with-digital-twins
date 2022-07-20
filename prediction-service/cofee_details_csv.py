import json
import csv

with open('E:\\lokesh_india\\smart_home\\final\\coffee_details.json') as json_file:
    print('a')
    data = json.load(json_file)
    print('a')
    employee_data = data['cofee_details']

data_file = open('E:\\lokesh_india\\smart_home\\final\\cofee_details.csv', 'w')

csv_writer = csv.writer(data_file)

count = 0
 
for emp in employee_data:
    if count == 0:        
        header = emp.keys()
        csv_writer.writerow(header)
        count += 1
   
    csv_writer.writerow(emp.values())
 
data_file.close()