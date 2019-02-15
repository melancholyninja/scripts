import csv


def map_chartspan_providers():
    chartspan_provider_map = {}
    with open('chartspan_providers.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['NPI Number'] == '':
                continue
            provider_name = row['name']
            npi = row['NPI Number']
            client = row['Client Name']
            key = npi
            provider = {
                'name': provider_name,
                'npi': npi,
                'client': client,
            }
            chartspan_provider_map[key] = provider
    return chartspan_provider_map


def add_total_benes(map):

    new_map = {}

    for k, v in map.items():
        temp_total_benes = 0
        with open('big_file.csv', 'r') as f:
            big_file = csv.DictReader(f)
            for row in big_file:
                if k == row['National Provider Identifier']:
                    temp_total_benes = row['Number of Medicare Beneficiaries']

            new_dict = {}
            new_dict['npi'] = map[k]['npi']
            new_dict['name'] = map[k]['name']
            new_dict['client'] = map[k]['client']
            new_dict['total_beneficiaries'] = temp_total_benes
            new_map[k] = new_dict
    return new_map


def add_total_awvs(map):

    new_map = {}
    line = 0
    for k, v in map.items():
        print(k)
        print(line)
        line = line + 1
        temp_total_awvs = 0
        with open('puf_file.csv', 'r') as f:
            puf_file = csv.DictReader(f)
            for row in puf_file:
                if k == row['National Provider Identifier']:
                    temp_total_awvs = row['Number of Services']

            new_dict = {}
            new_dict['npi'] = map[k]['npi']
            new_dict['name'] = map[k]['name']
            new_dict['client'] = map[k]['client']
            new_dict['total_beneficiaries'] = map[k]['total_beneficiaries']
            new_dict['number of services'] = temp_total_awvs

            new_map[k] = new_dict
    return new_map


chartspan_providers = map_chartspan_providers()

map_with_total_benes = add_total_benes(chartspan_providers)

map_with_total_awvs = add_total_awvs(map_with_total_benes)


with open('chartspan_awvs.csv', 'w') as f:
    fieldnames = ['name', 'npi', 'client', 'total_beneficiaries', 'total_awvs']
    writer = csv.DictWriter(map_with_total_awvs, fieldnames=fieldnames)
    writer.writeheader()
    for k, v in map_with_total_awvs.items():
        writer.writerow(v)




# print(chartspan_providers)

# with open('puf.csv', 'r') as f:
#     chartspan_providers_in_puf = []
#     reader = csv.DictReader(f)
#     print(reader.fieldnames)
#     for row in reader:
#         if row['National Provider Identifier'] in chartspan_providers_npis:
#             chartspan_providers_in_puf.append(row)
#
#
# with open('chartspan_providers_in_puf_file.csv', 'w') as f:
#     fieldnames = ['National Provider Identifier', 'Last Name/Organization Name of the Provider',
#     'First Name of the Provider', 'Number of Services',
#     'Number of Medicare Beneficiaries', 'Average Medicare Payment Amount']
#
#     writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
#     writer.writeheader()
#     for row in chartspan_providers_in_puf:
#         writer.writerow(row)
