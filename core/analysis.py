from .models import Member
import plotly.express as px
import pandas as pd
import datetime


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

        region = ''

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
        new_row = {'Birth_year': member.Birth_year}
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

    x_labels = ['0-15', '16-20', '21-25', '26-30', '31-35', '35+']

    fig = px.bar(x=x_labels, y=interval_dict.values(),
                 title='Age Group Count')

    chart = fig.to_html()

    return chart, x_labels, interval_dict.values()


def age_group_percent():

    _, x_labels, interval = age_group_count()

    total_members = sum(interval)

    age_group_percent = [(element/total_members)*100 for element in interval]

    fig = px.bar(x=x_labels, y=age_group_percent,
                 title='Age Group Percent')

    chart = fig.to_html()

    return chart


def new_members_time_interval(interval_days):
    today = datetime.date.today()
    interval = today - datetime.timedelta(days=interval_days)

    member_object = Member.objects.all()

    df = pd.DataFrame()

    for member in member_object:
        new_row = {'creation_date': member.creation_date}
        df = df.append(new_row, ignore_index=True)

    df_slice = df[df['creation_date'] >= interval]
    new_members = len(df_slice)

    return new_members


def regional_distribution():
    member_object = Member.objects.all()

    df = pd.DataFrame()

    for member in member_object:
        new_row = {'zip_code': member.zip_code}
        df = df.append(new_row, ignore_index=True)

    df['region'] = df['zip_code'].apply(lambda x: helper.zip_to_region(x))

    region = []
    antal = []

    for i in range(len(df['region'].value_counts())):
        region.append(df['region'].value_counts().keys()[i])
        antal.append(df['region'].value_counts()[i])

    d = dict(zip(region, antal))

    sorted_d = dict(sorted(d.items(), key=lambda item: item[1], reverse=True))

    region = [key for key in sorted_d.keys()]
    antal = [val for val in sorted_d.values()]

    fig = px.bar(x=region, y=antal,
                 title='Regional Distribution')

    chart = fig.to_html()

    return chart
