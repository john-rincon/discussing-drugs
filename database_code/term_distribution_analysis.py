def getUniqueTerms(work_file,start_time=-1,end_time=0,sub_reddit=0):
    import sqlite3 as sqlite
    with sqlite.connect(work_file) as con:
        cur = con.cursor()

        # cur.execute("select * from people where name_last=:who and age=:age", {"who": who, "age": age})
        if start_time>-1:
            start_time=start_time
        else: start_time=0
        if end_time > 0:
            end_time=end_time
        else: end_time=9999999999999

        cur.execute('SELECT ')
        if yes_top_only == 0:
            cur.execute('Select body, created_utc From Comment JOIN Subreddit '
                        'WHERE Subreddit.subreddit_id = Comment.subreddit_id AND Comment.created_utc > :start AND '
                        'Comment.created_utc < :end AND Subreddit.subreddit_name=:sub_name',
                        {"end": end_time, "start": start_time, "sub_name": subreddit})
        else:
            cur.execute('Select body, created_utc From Comment JOIN Subreddit '
                        'WHERE Subreddit.subreddit_id = Comment.subreddit_id AND Comment.created_utc > :start AND '
                        'Comment.created_utc < :end AND Subreddit.subreddit_name=:sub_name AND '
                        'Comment.parent_id=Comment.link_id',
                        {"end": end_time, "start": start_time, "sub_name": subreddit})
            # cur.execute('Select body, created_utc From Comment WHERE created_utc > :start AND created_utc < :end AND '
            # 'parent_id = link_id', {"end": end_time, "start": start_time})
        output = cur.fetchall()
        return output

#########
#1. Distribution Overall
####Words (pull unique where there's multiple CUIs for same term)
####Semantic Types
########

########
#2. Distribution Over time
####Words
####Semantic Types
#########

############################
#3. Distribution across users (popular v. avg)
###Words
###Types
#############################

############################
#4. Distribution between subreddits (opiate v. opiate recovery)
###Words
###Types
############################

