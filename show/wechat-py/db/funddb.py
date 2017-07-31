#db connect
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


def _mixex(argsintegers):
    if len(argsintegers) == 0:
        rows = chosen_fund_set.find()
        return rows
        
    dic_filter = {"_id":0, "date":1}
    for i in argsintegers:
        mixtype = "mix" + str(i)
        dic_filter[mixtype] = 1
    
    rows = chosen_fund_set.find({}, dic_filter)#chosen_fund_set.find({'date':'2017-07-12'})

    return rows


def _dateex(arg_date_strlist, rows):
    rowsout = []

    if len(arg_date_strlist) == 0 and len(rows) == 0: # -d return all dates list
        rowsout = chosen_fund_set.find({}, {"_id":0, "date":1})
        return rowsout

    for row in rows:
        if row['date'] in arg_date_strlist:
            rowsout.append(row)

    return rowsout


import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-j", "--jijin", type=str, nargs='*', help='choose the default fund which is the last mix type')
parser.add_argument("-d", "--date", type=str, nargs='*', help='choose fund by date, such as : -d yyyy-mm-dd yyyy-mm-dd')
parser.add_argument("-m", "--mix", type=int, nargs='*', help='choose fund by mix type, such as : -m 6 5 4')


#outside function
def get_chosen_fund(argstring):
    try:
        if "jj" == argstring:
            return _default()

        args = parser.parse_args(argstring.split())
        print(args.jijin)
        print(args.mix)
        print(args.date)

        rows = []
        if args.jijin != None:
            return _default()
        if args.mix != None:
            rows = _mixex(args.mix)
        if args.date != None:
            rows = _dateex(args.date, rows)

        chose_fund = ""           
        for row in rows:
            print(row)
            chose_fund += str(row)
            chose_fund += "\n"    # newline     -
        
        return chose_fund

    except:        
        #Print a help message, including the program usage and information about the arguments registered with the ArgumentParser. If file is None, sys.stdout is assumed.
        #parser.print_help()
        #Return a string containing a help message, including the program usage and information about the arguments registered with the ArgumentParser.
        return parser.format_help()
    
