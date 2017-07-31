#db connect
import argparse
import pymongo
conn = pymongo.MongoClient('mongodb://209.141.58.160:27017', 28017)#MongoClient()
db = conn.fund  #connect db fund, creat one if have none
chosen_fund_set = db['chosen_fund_set']

#choose mix by argsintegers
def _mix(argsintegers):
    rows = chosen_fund_set.find()#chosen_fund_set.find({'date':'2017-07-12'})
    if rows.count() <= 0:
        return ""

    index_last = 0
    if rows.count() > 0:
        index_last = rows.count() - 1

    #get fund by mix types 
    #2017-07-16    mix6:set() mix5:set() mix4:{'502050', '150268', '502022', '150300', '150228', '502042', '150282', '150141', '150136', '150292', '150256', '150330', '150250', '150242'} 
    chose_fund = rows[index_last]['date'] + "    "
    for i in argsintegers:
        mixtype = "mix" + str(i)
        chose_fund = chose_fund + mixtype + ":" + rows[index_last][mixtype] + " "
    
    return chose_fund

def _date(arg_date_strlist):
    chose_fund = ""
    return chose_fund

def _default():
    chose_fund = ""
    rows = chosen_fund_set.find()#chosen_fund_set.find({'date':'2017-07-12'})
    if rows.count() <= 0:
        return ""

    index_last = 0
    if rows.count() > 0:
        index_last = rows.count() - 1

    # try to get the data
    for i in range(6, 1, -1):
        mixtype = "mix" + str(i)
        chose_fund = rows[index_last][mixtype]
        if chose_fund == "set()":
            continue
        else:
            chose_fund = rows[index_last]['date'] + "    " + mixtype + ":" + rows[index_last][mixtype]
            break    
    
    return chose_fund


#outside function
def get_chosen_fund(argstring):
    try:
        if "jj" == argstring:
            return _default()

        parser = argparse.ArgumentParser()
        parser.add_argument("-d", "--date", type=str, nargs='*', help='')
        parser.add_argument("-m", "--mix", type=int, nargs='*', help='')
        args = parser.parse_args(argstring.split())   

        if args.mix != None:
            chose_fund = _mix(args.mix)
            return chose_fund
        if args.date != None:
            chose_fund = _date(args.date)
            return chose_fund
    except:
        return "wrong para:none was found"
    
