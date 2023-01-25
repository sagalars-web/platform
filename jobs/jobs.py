from django.conf import settings
import json
import random
from urllib.request import Request, urlopen
import psycopg2
import time


def establish_db_connection():

    conn = psycopg2.connect(
        host="containers-us-west-187.railway.app",
        database="railway",
        user="postgres",
        password="o7ldiAqCKY1MPF6bRxEu",
        port="7900"
    )

    cursor = conn.cursor()

    print('connection established')

    return conn, cursor


def track_exists(cursor, _id):
    cursor.execute(
        "SELECT auto_id FROM core_member WHERE auto_id = %s", (_id,))
    return cursor.fetchone() is not None


def schedule_api():

    i = 0

    conn, cursor = establish_db_connection()

    headers = {
        'autopilotapikey': '31f9fda3f63c4e5891904da0619c6d22'
    }

    bookmark = ''

    flag = True

    while flag:

        request = Request(
            'https://api2.autopilothq.com/v1/contacts' + bookmark, headers=headers)

        response_body = urlopen(request).read()

        my_json = response_body.decode('utf8').replace("'", '"')

        data = json.loads(my_json)

        members = []

        for contact in data['contacts']:

            all_fields = {}

            try:
                for field in contact['custom_fields']:
                    all_fields[field['kind']] = field['value']
            except:
                print('empty custom fields')

            try:
                mærkesag = all_fields['Mærkesager']
            except:
                print('No key issue')
                mærkesag = 'ingen mærkesag'

            try:
                fødselsår = all_fields['Fødselsår']
            except:
                print('No birthyear')
                fødselsår = 0000

            try:
                postnummer = all_fields['Postnummer']
            except:
                print('no zip code')
                postnummer = 0000

            print('Member: ', i)
            i += 1
            creation_date = contact['created_at']
            name = 'nemo'
            phone = 88888888
            email = 'john@saga.com'
            engagement = 120
            _id = contact['contact_id']

            print(track_exists(cursor, _id))
            if track_exists(cursor, _id):
                print('skipped member')
                continue

            values = (name, phone, creation_date,
                      email, mærkesag, fødselsår,
                      postnummer, engagement, _id)

            members.append(values)

        try:
            bookmark = '/' + data['bookmark']
            print(bookmark)
        except:
            flag = False

        if len(members) > 0:
            cursor.executemany(
                "INSERT INTO core_member (name, phone, creation_date, email, key_issue, birth_year, zip_code, engagement_score, auto_id) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)", members)
            #cursor.execute("INSERT INTO core_member (name, phone, creation_date, email, key_issue, birth_year, zip_code, engagement_score) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)",(name, phone, creation_date, email, mærkesag, fødselsår, postnummer, engagement))
            conn.commit()

        # Tilføj over tid når vi er mere skarpe på sikkerheden
        #navn = contact['FirstName']
        #email = contact['Email']

    cursor.close()
    conn.close()

    i = 0
    i += 1

    print('This code is running...', i)
