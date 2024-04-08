

import pandas as pd
import numpy as np
import json
import requests
from PIL import Image
from numpy.linalg import norm
from sklearn import preprocessing

def budget(num):
  if num>=2000 and num<4000:
    return 1
  elif num>=4000 and num<8000:
    return 2
  elif num>=8000 and num<10000:
    return 3
  else:
    return 4

def bud_list(spending):
    if spending == '€ 2000- € 4000':
        return 1
    elif spending == '€ 4000 - € 8000':
        return 2
    elif spending == '€ 8000 - € 10000':
        return 3
    else:
        return 4

def data_read():
    data = pd.read_excel("Recommender_Dataset.xlsx")
    
    cities = list(data["City"].value_counts().keys())
    job_interest = list(data["Job domain"].value_counts().keys())
    hobby_interest = list(data["Interest"].value_counts().keys())
    
    return data, cities, job_interest, hobby_interest    

def recommend_college(spending_limit,cao_points,city_name,hobbies, field_interest):    
    data, cities, job_interest, hobby_interest = data_read()

    bud_value = data['Budget'].values
    bucket_bud = []
    for num in bud_value:
      bucket_bud.append(budget(num))
    
    data['Budget_Bucket'] = bucket_bud
    
    num_cols = ["CAO opening rank","CAO closing rank"]
    data1 = data.copy()
    
    le_c = preprocessing.LabelEncoder()
    le_i = preprocessing.LabelEncoder()
    le_jd = preprocessing.LabelEncoder()
    
    data1['Budget_Bucket'] = data1['Budget_Bucket'].astype('str')
    data1["City"] = le_c.fit_transform(data1["City"])
    for elem in data1['City'].unique():
        data1['City'+str(elem)] = data1['City'] == elem
    
    data1["Interest"] = le_i.fit_transform(data1["Interest"])
    for elem in data1['Interest'].unique():
        data1['Interest'+str(elem)] = data1['Interest'] == elem
    
    data1["Job domain"] = le_jd.fit_transform(data1["Job domain"])
    for elem in data1['Job domain'].unique():
        data1['Job domain'+str(elem)] = data1['Job domain'] == elem
    
    #data1["Budget_Bucket"] = data1["Budget_Bucket"])
    for elem in data1['Budget_Bucket'].unique():
        data1['budget'+str(elem)] = data1['Budget_Bucket'] == elem
    
    for num in num_cols:
      data1[num] = data1[num].astype('int')
    
    rank_nor = []
    maxi = 625.0
    mini = 0.0
    for num in data1['CAO opening rank'].values:
      rank_nor.append(float((num - mini)/(maxi - mini)))
    
    data1['CAO opening rank'] = rank_nor
    
    data_input = pd.DataFrame()


    data_sim = data1.copy()
    
    data_input['CAO opening rank'] = [float((int(cao_points)-mini)/(maxi-mini))]
    data_input['Budget_Bucket'] = [bud_list(spending_limit)]
    data_input['City'] = [city_name]
    data_input['Interest'] = [hobbies]
    data_input['Job domain'] = [field_interest]
    
    data_input['City'] = le_c.transform(data_input['City'])
    for elem in data1['City'].unique():
        data_input['City'+str(elem)] = data_input['City'] == elem
    data_input['Interest'] = le_i.transform(data_input['Interest'])
    for elem in data1['Interest'].unique():
        data_input['Interest'+str(elem)] = data_input['Interest'] == elem
    data_input['Job domain'] = le_jd.transform(data_input['Job domain'])
    for elem in data1['Job domain'].unique():
        data_input['Job domain'+str(elem)] = data_input['Job domain'] == elem
    
    data_input['Budget_Bucket'] = data_input['Budget_Bucket'].astype('str')
    for elem in data1['Budget_Bucket'].unique():
        data_input['budget'+str(elem)] = data_input['Budget_Bucket'] == elem
    
    for num in ['University',  'Course Name', 'CAO closing rank', 'Budget', 'City', 'Interest', 'Job domain', 'Budget_Bucket']:
      data_sim.pop(num)
      try:
        data_input.pop(num)
      except:
        continue
    
    
    pairwise_similarities=np.dot(data_sim.values,data_input.T)/(norm(data_sim.values)*norm(data_input.values))

    data["similarities"] = list(pairwise_similarities)

    data_final = data[['University', 'Course Name', 'Budget', 'similarities']]
    final_df = data_final.sort_values(by=['similarities'], ascending=False)

    final_df.pop("similarities")
    
    return final_df.head().to_dict(orient="records")