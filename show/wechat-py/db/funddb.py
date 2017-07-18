import pymongo
conn = pymongo.MongoClient('mongodb://127.0.0.1:27017', 28017)#MongoClient()
db = conn.fund  #connect db fund, creat one if have none
chosen_fund_set = db['chosen_fund_set']

def get_chosen_fund():
    rows = chosen_fund_set.find()#chosen_fund_set.find({'date':'2017-07-12'})
    if rows.count() <= 0:
        return ""

    index_last = 0
    if rows.count() > 0:
        index_last = rows.count() - 1

    chose_fund = rows[index_last]['date'] + ":" + rows[index_last]['mix4']
    
    return chose_fund


