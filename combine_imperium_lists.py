from csv import DictReader, DictWriter
from datetime import datetime
from os import listdir

gender_map = {
    '1': 'Male',
    '2': 'Female'
}

patients = {}

for file in listdir('.'):
    if not file.endswith('.csv'):
        continue
    with open(file, 'r') as f:
        reader = DictReader(f)
        for row in reader:
            if row['Status'] == '2':
                enroll_date = datetime.strptime(row['Enrollment Date'].split(' ')[0], '%Y-%m-%d')
                if enroll_date < datetime(2017, 10, 31):
                    enroll_date = enroll_date.strftime('%m-%d-%Y')
                    npi_name = row['NPI Name']
                    hicn = row['HICN']
                    first_name = row['First Name']
                    last_name = row['Last Name']
                    sex = gender_map[row['Sex']]
                    dob = row['Birth Date']
                    status = row['Status']
                    key = f'{first_name}_{last_name}_{dob}'
                    p = {
                        'NPI Name': npi_name,
                        'HICN': hicn,
                        'First Name': first_name,
                        'Last Name': last_name,
                        'Sex': sex,
                        'Birth Date': dob,
                        'Status': status,
                        'Enrollment Date': enroll_date
                    }

                    patients[key] = p

print(patients)

with open('imperium_parsed.csv', 'w', newline='') as file:
    fieldnames = ['NPI Name', 'HICN', 'First Name', 'Last Name', 'Sex', 'Birth Date', 'Enrollment Date']
    writer = DictWriter(file, fieldnames=fieldnames, extrasaction='ignore')
    writer.writeheader()
    for id, row in patients.items():
        writer.writerow(row)

