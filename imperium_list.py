from csv import DictWriter, DictReader
from databases import CCMDatabase
from creds import get_ccm_db_creds

provider = 'crump'

org_id = '81'

patients = {}

with open(f'{provider}_imperium.csv') as f:
    reader = DictReader(f)
    print(reader.fieldnames)
    for row in reader:
        if not row:
            continue
        npi_name = row['NPI Name'].strip()
        hicn = row['HICN'].strip()
        first_name = row['First Name'].strip().capitalize()
        last_name = row['Last Name'].strip().capitalize()
        sex = row['Sex[1]'].strip()
        dob = row['Birth Date'].strip()
        # dob = datetime.strptime(dob, '%m/%d/%Y')
        outerkey = f'{first_name}_{last_name}_{dob}'
        patient = {
            'NPI Name': npi_name,
            'HICN': hicn,
            'First Name': first_name,
            'Last Name': last_name,
            'Sex': sex,
            'Birth Date': dob
        }
        patients[outerkey] = patient


ccm_db = CCMDatabase(get_ccm_db_creds(remote=False))

ccm_patients = ccm_db.get_ccm_patients_by_org(org_id=org_id, key_mapping='combo_dob')

patients_in_ccm = {}

for id, info in ccm_patients.items():
    if id in patients.keys():
        p = {
            'id': info['id'],
            'NPI Name': patients[id]['NPI Name'],
            'HICN': patients[id]['HICN'],
            'First Name': info['first_name'],
            'Last Name': info['last_name'],
            'Sex': patients[id]['Sex'],
            'Birth Date': info['date_of_birth'],
            'Status': info['status'],
            'Enrollment Date': info['billing_eligible_ts']
        }
        key = p['id']
        patients_in_ccm[key] = p

not_in_ccm = {}

for id, info in patients.items():
    if id not in ccm_patients.keys():
        id = id
        not_in_ccm[id] = info

# print(patients_in_ccm.items())

with open(f'imperium_{provider}_parsed.csv', 'w', newline='') as active_new_file:
    fieldnames = ['NPI Name', 'HICN', 'First Name', 'Last Name', 'Sex', 'Birth Date', 'Status', 'Enrollment Date']
    writer = DictWriter(active_new_file, fieldnames=fieldnames, extrasaction='ignore')
    writer.writeheader()
    for id, item in patients_in_ccm.items():
        writer.writerow(item)
    for id, item in not_in_ccm.items():
        writer.writerow(item)

# with open(f'imperium_{provider}_not_in_ccm.csv', 'w', newline='') as active_new_file:
#     fieldnames = ['NPI Name', 'HICN', 'First Name', 'Last Name', 'Sex', 'Birth Date']
#     writer = DictWriter(active_new_file, fieldnames=fieldnames, extrasaction='ignore')
#     writer.writeheader()
#     for id, item in patients_not_in_ccm.items():
#         writer.writerow(item)


