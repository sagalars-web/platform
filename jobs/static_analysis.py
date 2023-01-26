from django.conf import settings
import json
import random
from urllib.request import Request, urlopen
import psycopg2
import time
from core.models import Member
import plotly.express as px
import pandas as pd
import datetime
from dotenv.main import load_dotenv
import os

load_dotenv()

class helper():
    def columns_from_database(list_of_columns):
        member_object = Member.objects.all()

        df = pd.DataFrame()

        for member in member_object:
            new_row = {}

            for column in list_of_columns:
                new_row[str(column)] = member.column

            df = df.append(new_row, ignore_index=True)

        return df

    def zip_to_region(zip_code):

        region = 'ukendt'

        if zip_code >= 0 and zip_code < 3000:
            region = 'Hovedstaden'
        elif zip_code >= 3000 and zip_code < 3700:
            region = 'Nordsjælland'
        elif zip_code >= 3700 and zip_code < 3800:
            region = 'Bornholm'
        elif zip_code >= 3800 and zip_code < 3900:
            region = 'Færøerne'
        elif zip_code >= 3900 and zip_code < 4000:
            region = 'Grønland'
        elif zip_code >= 4000 and zip_code < 5000:
            region = 'Sjælland, LF, Møn'
        elif zip_code >= 5000 and zip_code < 6000:
            region = 'Fyn'
        elif zip_code >= 6000 and zip_code < 7000:
            region = 'Sønderjylland'
        elif zip_code >= 7000 and zip_code < 9000:
            region = 'Midtjylland'
        elif zip_code >= 9000 and zip_code < 10000:
            region = 'Nordjylland'

        return region

    def establish_db_connection():

        conn = psycopg2.connect(
            host=os.environ['DB_HOST'],
            database=os.environ['DB_NAME'],
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASS'],
            port=os.environ['DB_PORT']
        )

        cursor = conn.cursor()

        print('connection established')

        return conn, cursor

def member_engagement_score():

    member_object = Member.objects.all()

    df = pd.DataFrame()

    for member in member_object:
        new_row = {'name': member.name,
                   'engagement_score': member.engagement_score}
        df = df.append(new_row, ignore_index=True)

    fig = px.bar(df, x='name', y='engagement_score',
                 title='Member Engagement Chart')

    chart = fig.to_html()

    return chart

def age_group_count():

    member_object = Member.objects.all()

    df = pd.DataFrame()

    for member in member_object:
        new_row = {'birth_year': member.birth_year}
        df = df.append(new_row, ignore_index=True)

    year = int(datetime.date.today().year)

    df['age'] = df['birth_year'].apply(lambda x: year - x)

    intervals = [[0, 15], [16, 20], [21, 25], [26, 30],
                 [31, 35], [36, 100]]

    interval_dict = {str(interval): 0 for interval in intervals}

    for interval in intervals:
        for _, row in df.iterrows():
            if row['age'] >= interval[0] and row['age'] <= interval[1]:
                interval_dict[str(interval)] += 1

    values = list(interval_dict.values())

    values.insert(0,datetime.date.today())

    values = tuple(values)

    conn, cursor = helper.establish_db_connection()

    cursor.execute(
                "INSERT INTO age_group_count (date, zero_to_fifteen, sixteen_to_twenty, twentyone_to_twentyfive, twentysix_to_thirty,thirty_to_thirtyfive, thirtyfive_plus) VALUES(%s, %s, %s, %s, %s, %s, %s)", values)
    conn.commit()

    cursor.close()
    conn.close()

def regional_distribution():
    member_object = Member.objects.all()

    df = pd.DataFrame()

    for member in member_object:
        new_row = {'zip_code': member.zip_code}
        df = df.append(new_row, ignore_index=True)

    df['region'] = df['zip_code'].apply(lambda x: helper.zip_to_region(x))

    regions = ['Hovedstaden',
                'Midtjylland',
                'Fyn',
                'Sjælland, LF, Møn',
                'Nordsjælland',
                'Nordjylland',
                'Sønderjylland',
                'ukendt',
                'Grønland',
                'Færøerne']
    antal = []

    for region in regions:
        antal.append(len(df[df['region'] == region]))

    antal.insert(0,str(datetime.date.today()))

    final = tuple(antal)

    conn, cursor = helper.establish_db_connection()

    cursor.execute(
                "INSERT INTO regional_distribution (date, hovedstaden, midtjylland, fyn, sjælland_lf_møn, nordsjælland, nordjylland, sønderjylland, ukendt, grønland, færøerne) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", final)
    conn.commit()

    cursor.close()
    conn.close()


    