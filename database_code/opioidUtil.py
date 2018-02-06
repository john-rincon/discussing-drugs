def buildUserProfile(work_file,user_name,yesPosts=0):
    import sqlite3 as sqlite
    with sqlite.connect(work_file) as con:
        cur = con.cursor()
    if yesPosts==0:
        cur.execute('SELECT subreddit_name, created_utc FROM Comment JOIN Subreddit on Comment.subreddit_id = Subreddit.subreddit_id ' \
               'WHERE Comment.user_id="{user}"'.format(user=user_name))
    else:
        cur.execute('SELECT subreddit_name, created_utc,body FROM Comment JOIN Subreddit on '
                    'Comment.subreddit_id = Subreddit.subreddit_id ' \
            'WHERE Comment.user_id="{user}"'.format(user=user_name))
    profile=cur.fetchall()
    print profile
# cur.execute('SELECT A_ID FROM affiliation WHERE A_DESCRIP="{desc}"'. \
#             format(desc=afil[i])) a= cur.fetchall()

# buildUserProfile("reddit-opiates.db",'hydrokid20')
# import sqlite3 as sqlite
# with sqlite.connect('reddit-opiates.db') as con:
#     cur = con.cursor()
# cur.execute('SELECT subreddit_name FROM Subreddit JOIN Comment on Comment.subreddit_id = Subreddit.subreddit_id ' \
#        'WHERE Comment.user_id="hydrokid20"')
# profile=cur.fetchall()
# print profile

# buildUserProfile('reddit-opiates.db','hydrokid20')
def getCommentAndTime(work_file,subreddit,start_time,end_time,yes_top_only=0):
    import sqlite3 as sqlite
    with sqlite.connect(work_file) as con:
        cur = con.cursor()
        # cur.execute("select * from people where name_last=:who and age=:age", {"who": who, "age": age})
        if yes_top_only==0:
            cur.execute('Select body, created_utc From Comment WHERE created_utc > :start AND created_utc < :end',
                        {"end":end_time,"start":start_time})
        else:
            cur.execute('Select body, created_utc From Comment WHERE created_utc > :start AND created_utc < :end AND '
                        'parent_id = link_id', {"end": end_time, "start": start_time})
        print len(cur.fetchall())

work_file='reddit-opiates.db'
getCommentAndTime(work_file, 'opiates',1,99999999999,1)