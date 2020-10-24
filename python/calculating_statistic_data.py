import random
import pandas as pd
from google.cloud import storage
def make_blob_public(bucket_name, blob_name):
    storage_client = storage.Client.from_service_account_json('/Users/Robik/2020/Pycharm/working/cred.json')
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.make_public()
    print(
        "Blob {} is publicly accessible at {}".format(
            blob.name, blob.public_url
        )
    )
def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""

    storage_client = storage.Client.from_service_account_json('/Users/Robik/2020/Pycharm/working/cred.json')
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )
def getdemo(data,today):
    for i in data:
        try:
            dovj = len(i['region_distribution'])
            if dovj == 25:
                a = data.index(i)
        except:
            print(data.index(i))
    regions = []
    for i in data[a]['region_distribution']:
        regions.append(i['region'])
    regions.append('Kyiv')
    regions.append('Autonomous Republic of Crimea')
    regions.append('Sevastopol')
    for i in data:
        lower_views = int(i['impressions']['lower_bound'])
        if lower_views == 1000000:
            upper_views = 2000000
        else:
            upper_views = int(i['impressions']['upper_bound'])
        i['views'] = random.randint(lower_views, upper_views)
    df1 = pd.DataFrame()
    posts = []
    views = []
    for i in data:
        posts.append(i['id'])
        views.append(i['views'])
    df1['posts'] = posts
    df1['views'] = views
    for region_name in regions:
        mylist = []
        for i in data:
            views = i['views']
            try:
                new_regions = i['region_distribution']
                reg_views = 0
                for a in new_regions:
                    reg = a['region']
                    if reg == region_name:
                        reg_views = round(float(a['percentage']) * views, 0)
                mylist.append(reg_views)
            except Exception as e:
                mylist.append(0)
        df1[region_name] = mylist
        print(region_name)
    #df1['Kyiv'] = df1['Kiev']+df1['Kyiv']
    #df1 = df1.drop('Kiev',axis=1)
    cols = ['Cherkasy Oblast', 'Mykolaiv Oblast',
            'Zhytomyr Oblast', 'Zaporizhia Oblast', 'Zakarpattia Oblast',
            'Volyn Oblast', 'Vinnytsia Oblast', 'Ternopil Oblast', 'Sumy Oblast',
            'Rivne Oblast', 'Poltava Oblast', 'Odessa Oblast', 'Lviv Oblast',
            'Chernihiv Oblast', 'Luhansk Oblast', 'Kiev Oblast',
            'Kirovohrad Oblast', 'Khmelnytskyi Oblast', 'Kherson Oblast',
            'Kharkiv Oblast', 'Ivano-Frankivsk Oblast', 'Donetsk Oblast',
            'Dnipropetrovsk Oblast', 'Chernivtsi Oblast', 'Kyiv',
            'Autonomous Republic of Crimea', 'Sevastopol']
    df1['uk'] = df1[cols].sum(axis=1).astype(int)
    df1['other'] = df1.views - df1.uk
    df1['other'] = df1['other'].astype(int)
    df1 = df1.drop(['uk'], axis=1)
    a = 0
    p = 0
    for i in data:
        try:
            dovj = len(i['demographic_distribution'])
            if dovj > p:
                p = dovj
                a = data.index(i)
        except:
            print(data.index(i))
    demo = []
    for i in data[a]['demographic_distribution']:
        demo.append(i['gender'] + '_' + i['age'])
    df2 = pd.DataFrame()
    posts = []
    views = []
    for i in data:
        posts.append(i['id'])
        views.append(i['views'])
    df2['posts'] = posts
    df2['views'] = views
    for region_name in demo:
        mylist = []
        for i in data:
            views = i['views']
            try:
                new_regions = i['demographic_distribution']
                reg_views = 0
                for a in new_regions:
                    reg = a['gender'] + '_' + a['age']
                    if reg == region_name:
                        reg_views = round(float(a['percentage']) * views, 0)
                mylist.append(reg_views)
            except Exception as e:
                mylist.append(0)
        df2[region_name] = mylist
        print(region_name)
    filename = 'views_'+str(today) + '.csv'
    df1.to_csv(filename)
    #upload_blob('facebook_ads_opora', filename, 'views.csv')
    filename = 'gender_' + str(today) + '.csv'
    df2.to_csv(filename)
    #upload_blob('facebook_ads_opora', filename, 'gender.csv')
    print('success')