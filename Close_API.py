"""
Take Home Project for "Customer Support Engineer" at Close
reads the CSV data, processes it, injects it using Close API

By Sebastian Moncada Duque
"""

import csv
import datetime

def import_csv_data(file_name):
    """reads any CSV file within the project folder, just by passing the name 
    and resturns the titles and rows in diferent lists"""
    with open(file_name , newline="", encoding="UTF-8") as csvfile:
        data = list(csv.reader(csvfile, delimiter=','))
    titles = data.pop(0) #separate the headers and the data
    return titles, data

def get_leads(leads_data):
    """get the list of the companies within the data"""
    companies_list = []
    for lead_row in leads_data:
        if lead_row[0].strip() not in companies_list:
            companies_list.append(lead_row[0].strip())
    return companies_list

def group_contacts_by_lead(leads_data, leads_names):
    """group all the contacts from the same lead"""
    contacts_grouped_by_leads = []
    for lead_name in leads_names:
        leads_group = [lead for lead in leads_data if lead[0] == lead_name]
        contacts_grouped_by_leads.append(leads_group)
    return contacts_grouped_by_leads

def clean_data(data):
    """cleans the data to better use"""
    for row in data:
        if row[2] == "":
            row[2] = "notprovided@verify.email" #put a default email when empty
        else:
            row[2] = row[2].replace(",", ";").replace('"', '') # replace "," for ";" and delete the char " 
        row[3].replace('"', '') #delete the char " 
        if row[4] == "":
            row[4] = "01.01.1900" #put a default date in case of empty to not leave it blank 
        if row[5] == "":
            row[5] = "0" #put a default number in case of empty to not leave it blank 
        else:
            row[5] = row[5].replace("$", "").replace(",", "") #remove "$" and "," characters from revenue
    return data

def export_data_csv(header, data):
    """creates a CSV file with the headers and data passed"""
    with open('MOCK_DATA_CLEANED.csv', mode='w', encoding="UTF-8", newline='') as output_file:
        file_writer = csv.writer(output_file)
        file_writer.writerow(header)
        file_writer.writerows(data)

def get_leads_founded_between_2_dates(data, start_date, finish_date):
    """get the name of the leads that were founded between a given range"""
    for row in data:
        day, month, year = row[4].split(".")
        row[4] = datetime.datetime(int(year), int(month), int(day)) #replace the date with a datetime object

    leads_within_the_range = []
    for row in data:
        if row[4] == "": #if there is no founded date ignore that row
            continue
        if row[4] >= start_date and row[4] <= finish_date and row[0] not in leads_within_the_range: #if the lead is within the range and is not yet on the list, add that lead
            leads_within_the_range.append(row[0])
    return leads_within_the_range #returns the list

def segment_leads_by_state(data):
    """Segment Leads by US States and write a CSV file with the report of the revenue"""
    leads_by_state = []
    states = []
    for row in data:
        if row[5] == "" or row[5] == "0": #if there is no revenue data ignore that lead
            continue
        helper = [row[0], float(row[5]), row[6]] #group just the data required
        if helper not in leads_by_state: #if not yet on the list, add that data
            leads_by_state.append(helper)
        if row[6] not in states and row[6] != "": #save all the states
            states.append(row[6])
    
    output = []
    for state in states: #starts looping through each state
        leads = 0
        lead_most_revenue = ""
        revenue = 0
        total_revenue = 0
        for row in leads_by_state:
            if row[2] == state:
                total_revenue += row[1] #accumulates all the revenues of that state
                leads+=1 # +1 lead in that state
                if row[1] > revenue:
                    revenue = row[1] #save the highest revenue in that state
                    lead_most_revenue = row[0]
        output.append([state, leads, lead_most_revenue, total_revenue, total_revenue/leads]) #add the states's info to the list
    print(output)

    #export the date to a CSV file
    with open('output.csv', mode='w', encoding="UTF-8", newline='') as output_file:
        titles = ["US State", "Total number of leads", "The lead with most revenue", "Total revenue", "Median revenue"]
        file_writer = csv.writer(output_file)
        file_writer.writerow(titles)
        file_writer.writerows(output)


if __name__ == "__main__":
    headers, data = import_csv_data('MOCK_DATA.csv')
    cleaned_data = clean_data(data)
    export_data_csv(headers, cleaned_data)
    # start date and final date to search the lead that were founded inside that range
    leads_between_range = get_leads_founded_between_2_dates(
        cleaned_data,
        datetime.datetime(1963,3,29),
        datetime.datetime(1970,3,29)
    )
    #print(leads_between_range)

    #
    segment_leads_by_state(cleaned_data)




