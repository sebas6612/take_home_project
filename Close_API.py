"""
Take Home Project for "Customer Support Engineer" at Close
reads the CSV data, processes it, injects it using Close API

By Sebastian Moncada Duque
"""

import csv
import json
from closeio_api import Client

def import_csv_data(file_name):
    """reads any CSV file within the project folder, just by passing the name 
    and resturns the titles and rows in diferent lists"""
    with open(file_name , newline="", encoding="UTF-8") as csvfile:
        data = list(csv.reader(csvfile, delimiter=','))
    titles = data.pop(0) #separate the headers and the data
    return titles, data

def get_leads_names_and_states(leads_data):
    """get the list of the companies within the data and the US States"""
    companies_list = []
    states = []
    for lead_row in leads_data:
        if lead_row[0].strip() not in companies_list:
            companies_list.append(lead_row[0].strip())
        if lead_row[6] not in states and lead_row[6] != "":
            states.append(lead_row[6])
    return companies_list, states

def group_contacts_by_lead(leads_data, leads_names, headers):
    """group all the contacts from the same lead"""
    contacts_grouped_by_leads = []
    for lead_name in leads_names:
        lead_contacts = [lead for lead in leads_data if lead[0] == lead_name] #gets all the contacs where lead matches the current lead's name
        founded = lead_contacts[0][4]
        revenue = lead_contacts[0][5]
        state = lead_contacts[0][6]
        contacts_details = []
        for contact in lead_contacts: #creates a list with all the contacts of an specific lead
            if ";" in contact[2]: #if there is a ";" means there are 2 emails
                emails = [{"type": "office", "email": contact[2].split(";")[0]}, {"type": "office", "email": contact[2].split(";")[1]}]
            else:
                emails = [{"type": "office", "email": contact[2]}]
            if ";" in contact[3]: #if there is a ";" means there are 2 phone numbers
                phones = [{"type": "office", "phone": contact[3].split(";")[0]}, {"type": "office", "phone": contact[3].split(";")[1]}]
            else:
                phones = [{"type": "office", "email": contact[3]}]
            contacts_details.append({"name": contact[1], "emails": emails, "phones": phones})
        contacts_grouped_by_leads.append({
                            "name": lead_name,
                            "contacts": contacts_details, 
                            headers[4]: founded,
                            headers[5]: revenue,
                            "addresses": [{"state": state,"country":"US"}]
                        })
    print(json.dumps(contacts_grouped_by_leads[0], indent=4))
    return contacts_grouped_by_leads

def post_leads(leads_grouped):
    """Post the given list of leads to the Close's API """
    api = Client('api_5Dsq0sNtw1TwyiRPuMjylP.2BJZs6G9AQBEh5XnppxDUt')
    for lead in leads_grouped:
        resp = api.post('lead', data=lead)
        print(resp["name"], resp["id"])

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

def get_leads_founded_between_2_dates(start_date, finish_date):
    """get the name of the leads that were founded between a given range"""
    api = Client('api_5Dsq0sNtw1TwyiRPuMjylP.2BJZs6G9AQBEh5XnppxDUt')

    params = {
        "limit": None,
        "query": {
            "negate": False,
            "queries": [
                {
                    "negate": False,
                    "object_type": "lead",
                    "type": "object_type"
                },
                {
                    "negate": False,
                    "queries": [
                        {
                            "negate": False,
                            "queries": [
                                {
                                    "condition": {
                                        "before": {
                                            "type": "fixed_local_date",
                                            "value": finish_date,
                                            "which": "end"
                                        },
                                        "on_or_after": {
                                            "type": "fixed_local_date",
                                            "value": start_date,
                                            "which": "start"
                                        },
                                        "type": "moment_range"
                                    },
                                    "field": {
                                        "custom_field_id": "cf_mndnBH5FHQUxYghNx6UJrCuHkGFfRzpwNWVaLZiBb5y",
                                        "type": "custom_field"
                                    },
                                    "negate": False,
                                    "type": "field_condition"
                                }
                            ],
                            "type": "and"
                        }
                    ],
                    "type": "and"
                }
            ],
            "type": "and"
        },
        "results_limit": None,
        "sort": [],
        "_fields": {
            "lead": ["name"]
        }
    }

    resp = api.post("/data/search", params)

    #print(json.dumps(resp, indent=4))
    return [name["name"] for name in resp["data"]] #returns just the names of Leads

def segment_leads_by_state(data, _states):
    """Segment Leads by US States and write a CSV file with the report of the revenue"""
    output = []
    for state in _states:
        api = Client('api_5Dsq0sNtw1TwyiRPuMjylP.2BJZs6G9AQBEh5XnppxDUt')
        #filters to get the leads from a specific state and where the revenue is greater than 0
        params = {
            "limit": None,
            "query": {
                "negate": False,
                "queries": [
                    {
                        "negate": False,
                        "object_type": "lead",
                        "type": "object_type"
                    },
                    {
                        "negate": False,
                        "queries": [
                            {
                                "negate": False,
                                "related_object_type": "address",
                                "related_query": {
                                    "negate": False,
                                    "queries": [
                                        {
                                            "condition": {
                                                "mode": "full_words",
                                                "type": "text",
                                                "value": state
                                            },
                                            "field": {
                                                "field_name": "state",
                                                "object_type": "address",
                                                "type": "regular_field"
                                            },
                                            "negate": False,
                                            "type": "field_condition"
                                        }
                                    ],
                                    "type": "and"
                                },
                                "this_object_type": "lead",
                                "type": "has_related"
                            },
                            {
                                "negate": False,
                                "queries": [
                                    {
                                        "condition": {
                                            "gt": 0,
                                            "type": "number_range"
                                        },
                                        "field": {
                                            "custom_field_id": "cf_5KjFJKfF6DMsTl8P6e45nkQsfnwxoe4LpKABIz198uG",
                                            "type": "custom_field"
                                        },
                                        "negate": False,
                                        "type": "field_condition"
                                    }
                                ],
                                "type": "and"
                            }
                        ],
                        "type": "and"
                    }
                ],
                "type": "and"
            },
            "results_limit": None,
            "sort": [],
            "_fields": {
                "lead": ["name", "custom"]
            },
            "_limit": 100
        }
        resp = api.post("/data/search", params)
        lead_most_revenue = ""
        revenue = 0
        total_revenue = 0
        for i, row in enumerate(resp["data"]):
            if row["custom.cf_5KjFJKfF6DMsTl8P6e45nkQsfnwxoe4LpKABIz198uG"] > revenue: #if current lead is the highest revenue
                revenue = row["custom.cf_5KjFJKfF6DMsTl8P6e45nkQsfnwxoe4LpKABIz198uG"]
                lead_most_revenue = row["name"]
            total_revenue += row["custom.cf_5KjFJKfF6DMsTl8P6e45nkQsfnwxoe4LpKABIz198uG"]
        output.append([state, i+1, lead_most_revenue, total_revenue, total_revenue/(i+1)]) #add the states's info to the list
    
    #export the data to a CSV file
    with open('output.csv', mode='w', encoding="UTF-8", newline='') as output_file:
        titles = ["US State", "Total number of leads", "The lead with most revenue", "Total revenue", "Median revenue"]
        file_writer = csv.writer(output_file)
        file_writer.writerow(titles)
        file_writer.writerows(output)
    
if __name__ == "__main__":
    headers, data = import_csv_data('MOCK_DATA.csv')
    cleaned_data = clean_data(data)
    leads_list, states = get_leads_names_and_states(cleaned_data)
    leads = group_contacts_by_lead(cleaned_data, leads_list, headers)
    post_leads(leads)
    print(get_leads_founded_between_2_dates("1990-01-01", "2000-01-01"))
    segment_leads_by_state(cleaned_data, states)
