import pymongo, time
import pandas as pd
conn = pymongo.MongoClient('mongodb://127.0.0.1:27017', 28017)#MongoClient()
db = conn.fund  #连接fund数据库，没有则自动创建
date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
print(date)
#chosen_fund_set = db.chosen_fund_set    #使用fund_set集合，没有则自动创建
fund_set = db[date] #使用'YYYY-MM-DD'集合，没有则自动创建
#print(list(fund_set.find()))
#load data to pandas
df = pd.DataFrame(list(fund_set.find()))
df=df.drop(['_id'],axis=1)

print("head-------------------------------------------------------------------------")
print(len(df))
print(df.head())

print("fund_id to index-------------------------------------------------------------")
df=df.set_index(df['fund_id'])
print(df.head())

#remove NA row
print("remove NA row----------------------------------------------------------------")
df_no_NA=df.dropna()
print('dropna column',len(df_no_NA))

df_no_name=df_no_NA.drop(['fund_name','fund_id'],axis=1)
print(df_no_name.head())

#del the '%',then we can sort
print("del the '%',then we can sort-------------------------------------------------")
def clean_num_in_column(column):
    return column.apply(drop_percent_sign)

def drop_percent_sign(state):
	if state.endswith('%'):
		return float(state.replace('%',''))#一定要变成浮点数字

df_drop_percent=df_no_name.apply(clean_num_in_column)
print(df_drop_percent.head())

# get max item in each column ,check the max item info
print("get max item in each column ,check the max item info-------------------------")
def get_large_in_column(column):
	return column.sort_values(ascending=False).iloc[0]
print(df_drop_percent.apply(get_large_in_column))

range=100
print("sort the top 100 funds by 'from_start'---------------------------------------")
print(df_drop_percent.sort_values(by=['from_start'],ascending=False).head(range))
fs_index=df_drop_percent.sort_values(by=['from_start'], ascending=False).head(range).index
#print(fs_index)

#sort the funds by 'three_year'
print("sort the top 100 funds by 'three_year'---------------------------------------")
print(df_drop_percent.sort_values(by=['three_year'],ascending=False).head(range))
y3_index=df_drop_percent.sort_values(by=['three_year'],ascending=False).head(range).index

#获得 按照基金成立一年以来涨幅 大小排序
#sort the funds by 'one_year'
print("sort the top 100 funds by 'one_year'-----------------------------------------")
y1_index=df_drop_percent.sort_values(by=['one_year'],ascending=False).head(range).index

#sort the funds by 'six_month'
print("sort the top 100 funds by 'six_month'----------------------------------------")
m6_index=df_drop_percent.sort_values(by=['six_month'],ascending=False).head(range).index

#sort the funds by the 'three_month'
print("sort the top 100 funds by the 'three_month'-----------------------------------")
m3_index=df_drop_percent.sort_values(by=['three_month'],ascending=False).head(range).index

#sort the funds by 'one_month'
print("sort the top 100 funds by 'one_month'-----------------------------------------")
m1_index=df_drop_percent.sort_values(by=['one_month'],ascending=False).head(range).index


fs_index_set=set(fs_index)
y3_index_set=set(y3_index)
y1_index_set=set(y1_index)
m6_index_set=set(m6_index)
m3_index_set=set(m3_index)
m1_index_set=set(m1_index)

#check the mix one during 6 columns
print("check the mix one during 6 columns-------------------------------------------")
mix_6c=fs_index_set&y3_index_set&y1_index_set&m6_index_set&m3_index_set&m1_index_set
print('mix 6c:',mix_6c)

#check the mix one during 5 columns
print("check the mix one during 5 columns-------------------------------------------")
mix_5c=y3_index_set&y1_index_set&m6_index_set&m3_index_set&m1_index_set
print('mix 5c:',mix_5c)

#check the mix one during 4 columns
print("check the mix one during 4 columns-------------------------------------------")
mix_4c=y1_index_set&m6_index_set&m3_index_set&m1_index_set
print('mix 4c:',mix_4c)

#check the mix one during 3 columns
print("check the mix one during 3 columns-------------------------------------------")
mix_3c=m6_index_set&m3_index_set&m1_index_set
print('mix 3c:',mix_3c)

#check the mix one during 2 columns
print("check the mix one during 2 columns-------------------------------------------")
mix_2c=m3_index_set&m1_index_set
print('mix 2c:',mix_2c)

#check the mix one during 1 columns
print("check the mix one during 1 columns-------------------------------------------")
mix_1c=m1_index_set
print('mix 1c:',mix_1c)

#check the detailed info aboout the mix_4c
print("check the detailed info aboout the mix_4c------------------------------------")
df_drop_percent=df_drop_percent.drop(['from_start','three_year'],axis=1)
for each in mix_4c:
    fund_id=df_drop_percent[df_drop_percent.index==each].sum(axis=1).index[0]
    fund_total_rate=df_drop_percent[df_drop_percent.index==each].sum(axis=1).values[0]
    print(fund_id,fund_total_rate)

# 5 c with fund_name
#df_no_NA = df_no_NA.sort_values(by=['fund_id'], ascending=True).head()
#a = pd.DataFrame(df_no_NA, index=mix_5c)  
#print(a)
#print(Index)
#a = df_no_NA[(df_no_NA.BoolCol==3)&(df_no_NA.attr==22)].mix_5c.tolist()  
#print(a) 
#print(df_no_NA.head())
#print()
#print(df_no_NA.head(['fund_id'], mix_5c))
#for x in mix_5c:
#    print(x)
#    print(df_no_NA.at[x, "fund_id"])
print("output the complete info of mix_5c------------------------------------------")
#print(list(mix_5c))
#print(df_no_NA['fund_id'].isin(list(mix_5c)))
#print(df_no_NA.at(list(mix_5c)[0], 'fund_id'))

print("save mix to mongodb------------------------------------------")
import time
from pymongo import MongoClient
conn = MongoClient('mongodb://127.0.0.1:27017', 28017)#MongoClient()
db = conn.fund  #连接fund数据库，没有则自动创建
date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
print(date)
chosen_fund_set = db.chosen_fund_set    #使用fund_set集合，没有则自动创建
#fund_set = db[date] #使用'YYYY-MM-DD HH:MM'集合，没有则自动创建

row = {"date":date, 
        "mix6":str(mix_6c),
        "mix5":str(mix_5c),
        "mix4":str(mix_4c),
        "mix3":str(mix_3c),
        "mix2":str(mix_2c),
        "mix1":str(mix_1c)}
chosen_fund_set.insert_one(row) 
