import requests
import pandas as pd

def fetch_data(api_url, payload=None, method='GET'):
    response = ""

    # Handle GET and POST methods
    if method == 'GET':
        response = requests.get(api_url, params=payload)
    elif method == 'POST':
        response = requests.post(api_url, json=payload)
    else:
        print(f"Error: {method} not an allowed method")
        return None

    # Check for Success
    if response.status_code == 200:
        try:
            data = response.json()

            # Check 'results' type
            results = data['results']
            if isinstance(results, list):
                return pd.DataFrame(data['results'])
            elif isinstance(results, dict):
                return pd.DataFrame([data['results']])
            else:
                print(f"Unexpected 'results' structure: {results}")
                return None
                
        except ValueError as e:
            print("Error parsing JSON:", e)
            print("Response text:", response.text)
            return None
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None


if __name__ ==  "__main__":

    # POST REQUEST
    # api_url = "https://api.usaspending.gov/api/v2/search/spending_by_award/"
    # payload = {
    #     "filters": {
    #         "award_type_codes": ["10"],
    #         "agencies": [
    #             {
    #                 "type": "awarding",
    #                 "tier": "toptier",
    #                 "name": "Social Security Administration"
    #             }
    #         ],
    #         "recipient_scope": "domestic",
    #         "award_amounts": [
    #             {
    #                 "lower_bound": 1500000.00,
    #                 "upper_bound": 1600000.00
    #             }
    #         ]
    #     },
    #     "fields": ["Award ID", "Recipient Name", "Award Amount", "Awarding Agency"],
    #     "sort": "Recipient Name",
    #     "order": "desc"
    # }

    # data = fetch_data(api_url, payload, 'POST')


    # GET REQUEST
    api_url = "https://api.usaspending.gov/api/v2/references/agency/456/"

    data = fetch_data(api_url)

    if data is not None:
        print("Data fetched successfully. Saving to file...")
        data.to_csv('data/raw_data_test.csv', index=False)