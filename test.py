# eg. use:
# > python class-jsonifier.py --filename "Micro Package API Specs.xlsx - Business Classes.csv" 

import argparse
import pandas

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
        # print(row)
        # i += 1
        # if i> 10:
        #     break
        # counties_states.add(row['county'] + ", " + row['state'])
        # counties_states.append(row['state'])

    counties = list(counties)
    print("there are " + str(len(counties)) + " counties total")


    max_deaths = 0
    max_rows = []

    max_cases = 0
    max_cases_rows = []

    for row in zip(cf['county'], cf['state'], cf['deaths'], cf['cases'], cf['date']):
        
        if row[2] == max_deaths:
            max_rows.append(row)

        if row[2] > max_deaths:
            max_deaths = row[2]  
            max_rows = [row]

        if row[3] == max_cases:
            max_cases_rows.append(row)

        if row[3] > max_cases:
            max_cases = row[3]  
            max_cases_rows = [row]


    print("Max deaths")
    print(max_deaths)
    print([ row for row in max_rows])

    print("Max cases")
    print(max_cases)
    print([ row for row in max_cases_rows])


    # date,state,fips,cases,deaths
    sf = pandas.read_csv(states_file)


    # df["Fast Tract Description (edited)"] = df.apply(lambda x: str(x["ISO BOP Class Code"]) not in x["Fast Tract Description"], "[{0}] {1}".format(x["ISO BOP Class Code"], x["Fast Tract Description"]), x["Fast Tract Description"])
    # df["Fast Tract Description (edited)"] = [x[1] if str(x[0]) in x[1] else "[{0}] {1}".format(x[0], x[1]) for x in zip(df["ISO BOP Class Code"], df["Fast Tract Description"])]

    # with open(output_json_file, 'w') as outfile:
    #     outfile.write(df.to_json(orient='records'))

if __name__ == '__main__':
    main()
