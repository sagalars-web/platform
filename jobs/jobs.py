from django.conf import settings
import json
import random
from urllib.request import Request, urlopen
import psycopg2

def schedule_api():
    '''
    headers = {
    'autopilotapikey': '31f9fda3f63c4e5891904da0619c6d22'
    }
    request = Request('https://api2.autopilothq.com/v1/contacts/bookmark', headers=headers)

    response_body = urlopen(request).read()

    my_json = response_body.decode('utf8').replace("'", '"')

    data = json.loads(my_json)

    for contact in data['contacts'][:1]:
        creation_date = contact['created_at']
        fødselsår = contact['custom_fields'][0]['value']
        mærkesag = contact['custom_fields'][1]['value']
        postnummer = contact['custom_fields'][2]['value']

        #Tilføj over tid når vi er mere skarpe på sikkerheden
        #navn = contact['FirstName']
        #email = contact['Email']
    
    conn = psycopg2.connect(
        host="containers-us-west-135.railway.app",
        database="railway",
        user="postgres",
        password="aKRCb76YB3buctMVcoJ6",
        port="5486"
    )

    cursor = conn.cursor()

    data_row = cursor.fetchone()
    print("Connection established: ", data_row)



    print(data)
    '''
    i = 0
    i += 1
    
    print('This code is running...', i)