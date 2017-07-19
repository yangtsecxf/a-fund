#db connect
import argparse
import pymongo
conn = pymongo.MongoClient('mongodb://127.0.0.1:27017', 28017)#MongoClient()
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

def _default():
    rows = chosen_fund_set.find()#chosen_fund_set.find({'date':'2017-07-12'})
    if rows.count() <= 0:
        return ""

    index_last = 0
    if rows.count() > 0:
        index_last = rows.count() - 1

    #default mix6
    chose_fund = rows[index_last]['date'] + ":" + rows[index_last]['mix6']
    
    return chose_fund


#outside function
def get_chosen_fund(argstring):
    try: #mix fund
        #argparse
        parser = argparse.ArgumentParser(description='Process some integers.')
        parser.add_argument('integers', metavar='N', type=int, nargs='+',
                    help='an integer for the mix type')
        parser.add_argument('--mix', dest='mix_dest', action='store_const',
                    const=_mix, default=_default,
                    help='choose the mix type by integers (default: find the mix6)')
        args = parser.parse_args(argstring.split())
        chose_fund = args.mix_dest(args.integers)
        return chose_fund
    except:
        try: #jj
            if argstring == "jj":
                return _default()
            else:
                raise ValueError
        except:
            return "wrong para:none was found"
    
