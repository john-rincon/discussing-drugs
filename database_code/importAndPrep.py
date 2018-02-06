import csv,json, datetime
from bz2 import BZ2File

# filepath=('/home/john/Downloads/reddit-data.csv')
filepath=('/home/john/Desktop/2013-01.bz2')
dictList=[]

for line in BZ2File(filepath,'r'):
    dictList.append(json.loads(line))

# for key in dictList[0]:
#     print key + " - " + str(type(dictList[0][key]))

def makeRedditTables(work_file):
    import sqlite3 as sqlite
    with sqlite.connect(work_file) as con:
        cur = con.cursor()

        cur.execute("DROP TABLE IF EXISTS User")
        cur.execute("DROP TABLE IF EXISTS Comment")
        cur.execute("DROP TABLE IF EXISTS Subreddit")
        cur.execute("DROP TABLE IF EXISTS Community")
        cur.execute("DROP TABLE IF EXISTS Immediate_Interaction")




        #subreddit_name = subreddit in JSON files
        cur.execute("CREATE TABLE Subreddit(subreddit_id TEXT NOT NULL PRIMARY KEY, subreddit_name TEXT)")

        #name = author in JSON files
        cur.execute("CREATE TABLE User(user_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, name TEXT)")

        #cur.execute("INSERT INTO professor (P_ID,P_NAME,P_TITLE), (?,?)")
        #con.commit()

        cur.execute("CREATE TABLE Community(subreddit_id INTEGER,user_id INTEGER, PRIMARY KEY (subreddit_id, user_id))")
        #comment_id = name in json (t# indicates 'thing' type, and following sequence is ID)
        #subreddit_id = foreign key
        #user_id = author in json

        cur.execute('''CREATE TABLE Comment(comment_id TEXT NOT NULL PRIMARY KEY,
         subreddit_id TEXT, user_id TEXT,body TEXT,
         gilded INTEGER, author_flair_text TEXT,
         downs INTEGER, ups INTEGER, controversiality INTEGER, score INTEGER,
         created_utc INTEGER, parent_id TEXT, link_id TEXT )''')

        cur.execute("CREATE TABLE Immediate_Interaction(immediate_interaction_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, first_poster_id INTEGER,second_poster_id INTEGER)")

def populateRedditTables(work_file,input_file):
    import sqlite3 as sqlite
    with sqlite.connect(work_file) as con:
        cur = con.cursor()

    for row in input_file:
        userString = "INSERT OR IGNORE INTO User VALUES(NULL,?)"
        subredditString= "INSERT OR IGNORE INTO Subreddit (subreddit_id, subreddit_name) VALUES (?,?)"
        subredditValues=[row['subreddit_id'],row['subreddit']]
        communityString = "INSERT OR IGNORE INTO Community (subreddit_id, user_id) VALUES (?,?)"
        communityValues=[row['subreddit_id'],row['author']]
        commentString = '''INSERT INTO Comment (comment_id, subreddit_id, body, user_id, gilded, author_flair_text,
         downs, ups, controversiality, score, created_utc, parent_id, link_id) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)'''
        commentValues=[row['name'] ,row['subreddit_id'], row['body'], row['author'], row['gilded'] ,  row['author_flair_text'],row['downs'],
                       row['ups'], row['controversiality'], row['score'], row['created_utc'],row['parent_id'], row['link_id']]
        commentString=commentString.strip('\n')
        # subredditValues=[str(row['subreddit_id']),str(row['subreddit'])]
        # communityString = "INSERT OR IGNORE INTO Community (subreddit_id, user_id) VALUES (?,?)"
        # communityValues=[str(row['subreddit_id']),str(row['author'])]
        # commentString = '''INSERT INTO Comment (comment_id, subreddit_id, user_id, gilded, author_flair_text,
        #  downs, ups, controversiality, score, created_utc, parent_id, link_id) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)'''
        # commentValues=[str(row['name']) ,str(row['subreddit_id']), str(row['author']), str(row['gilded']) ,  str(row['author_flair_text']),str(row['downs']),
        #                str(row['ups']), str(row['controversiality']), str(row['score']), str(row['created_utc']),str(row['parent_id']), str(row['link_id'])]
        # commentString=commentString.strip('\n')
        # print userString
        # print subredditString
        # print communityString
        # print commentString
        author= str(row['author'])
        # print author
        subList = ['opiates', 'OpiatesRecovery']
        if row['subreddit'] in subList:
            cur.execute(userString,[author])
            cur.execute(subredditString,subredditValues)
            cur.execute(communityString, communityValues)
            cur.execute(commentString,commentValues)
            con.commit()
def filterRedditTables(input_file):
    #####filter out non-opioid related comments
    x=0

####List of all keys ####
# [u'body', u'edited', u'subreddit_id', u'author_flair_css_class',
#  u'stickied', u'gilded', u'author_flair_text', u'author', u'created_utc',
#  u'link_id', u'parent_id', u'distinguished', u'score', u'retrieved_on',
#  u'controversiality', u'subreddit', u'id', u'author_cakeday']

#comments with same 'parent_id' seem to refer to same post
#cakeday = how long a user has been active
#link_id = indicative of same post
#parent_id = indicative of nesting structure. ID can be another comment
##when we set the above 2 equal, we find top level comments (63396 in file)
#coud use flair to identify medical professionals

#### SUBREDDIT LIST#####
#[u'Drugs', u'ChronicPain', u'glassine', u'medicine', u'opiates',
#  u'askdrugs', u'OpiatesRecovery', u'fentanyl']
from collections import Counter

x=0

###################################################
################CREATE LIST OF TIMES ##############
###################################################

opioidCount=[]
#
def countPostDays (dictList):
    for line in dictList:
        utcTime=float(line['created_utc'])
        # print utcTime
        normTime=datetime.datetime.utcfromtimestamp(utcTime)
        # print normTime
        normTime=str(normTime)
        normTime= normTime[:10]
        opioidCount.append(normTime)
###COUNT TIMES
    counts = dict()
    for i in opioidCount:
      counts[i] = counts.get(i, 0) + 1
    print counts
###################

# for line in dictList:
#     x= line['author_flair_text']
#     if x:
#         print line['subreddit']+ ' --- '+ x

subList=[]

# makeRedditTables('reddit-opiates.db')
# populateRedditTables('reddit-opiates.db',dictList)


