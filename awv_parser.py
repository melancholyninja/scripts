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


def map_puf_file():
    puf_map = {}
    with open('puf_file.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            npi = row['National Provider Identifier']
            last_name = row['Last Name/Organization Name of the Provider']
            first_name = row['First Name of the Provider']
            awvs = row['Number of Services']
            avg_payment = row['Average Medicare Payment Amount']
            provider = {
                'npi': npi,
                'last_name': last_name,
                'first_name': first_name,
                'awvs': awvs,
                'avg_payment': avg_payment
            }
            if npi in puf_map.keys():
                pass

            puf_map[npi] = provider
    return puf_map


def main():
    chartspan_providers = map_chartspan_providers()
    print(chartspan_providers['1194750570'])
    # with open('chartspan_awvs.csv', 'w') as f:
    #     fieldnames = ['name', 'npi', 'client', 'total_beneficiaries', 'total_awvs']
    #     writer = csv.DictWriter(map_with_total_awvs, fieldnames=fieldnames)
    #     writer.writeheader()
    #     for k, v in map_with_total_awvs.items():
    #         writer.writerow(v)

if __name__ == '__main__':
    main()








