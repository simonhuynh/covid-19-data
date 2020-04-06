# eg. use:
# > python class-jsonifier.py --filename "Micro Package API Specs.xlsx - Business Classes.csv" 

import argparse
import pandas
import json

output_json_file = 'fips_map.json'

def main():
    counties_file = "us-counties.csv"
    states_file = "us-states.csv"

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", help="CSV file with class data", type=str)
    # parser.add_argument("-u", "--underscorify", help="Replace spaces with underscores in CSV column names. Not implemented.", type=bool, nargs='?')
    args = parser.parse_args()

    # date,county,state,fips,cases,deaths
    cf = pandas.read_csv(counties_file)

    counties = set()
    i = 1
    for county_state in zip(cf['county'], cf['state']):
        counties.add(county_state)

    counties = list(counties)
    print("there are " + str(len(counties)) + " counties total")


    max_deaths = 0
    max_rows = []

    max_cases = 0
    max_cases_rows = []

    fips_map = {}

    county_map = {}

    missing_fips = set()

    for county, state, deaths, cases, date, fips_code in zip(cf['county'], cf['state'], cf['deaths'], cf['cases'], cf['date'], cf['fips']):
        deaths = int(deaths)
        cases = int(cases)

        county_state_name = str(county + ", " + state)
        try:
            fips_id = str(int(fips_code))
        except ValueError as e:
            # print("failed to get fips_id", row[5], row)
            missing_fips.add(county_state_name)
            fips_id = county_state_name

        # if county_state_name not in county_map:
        #     county_map[county_state_name] = {
        #         fips_codes: set([cf['fips']])
        #     }
        # else:
        #     county_map[county_state_name][fips_code].add([cf['fips'])

        if deaths == max_deaths:
            max_rows.append((county_state_name, deaths))

        if deaths > max_deaths:
            max_deaths = deaths  
            max_rows = [(county_state_name, deaths)]

        if cases == max_cases:
            max_cases_rows.append((county_state_name, cases))

        if cases > max_cases:
            max_cases = cases  
            max_cases_rows = [(county_state_name, cases)]

        if fips_id not in fips_map:
            fips_map[fips_id] = {
                'id': fips_id,
                'name': county_state_name,
                'records': []
            }
        fips_map[fips_id]['records'].append({
            'date': date,
            'cases': cases,
            'deaths': deaths
        })


    with open(output_json_file, 'w') as outfile:
        outfile.write(json.dumps(fips_map))

    print("\nDone!")
    print("These areas have no FIPS code ", list(missing_fips))

    print("Max deaths")
    print(max_deaths)
    print([ row for row in max_rows])

    print("Max cases")
    print(max_cases)
    print([ row for row in max_cases_rows])




    # date,state,fips,cases,deaths
    sf = pandas.read_csv(states_file)

    print("Here's the data for Snohomish\n")
    print(fips_map["53061"])

    # df["Fast Tract Description (edited)"] = df.apply(lambda x: str(x["ISO BOP Class Code"]) not in x["Fast Tract Description"], "[{0}] {1}".format(x["ISO BOP Class Code"], x["Fast Tract Description"]), x["Fast Tract Description"])
    # df["Fast Tract Description (edited)"] = [x[1] if str(x[0]) in x[1] else "[{0}] {1}".format(x[0], x[1]) for x in zip(df["ISO BOP Class Code"], df["Fast Tract Description"])]

    # with open(output_json_file, 'w') as outfile:
    #     outfile.write(df.to_json(orient='records'))

if __name__ == '__main__':
    main()
