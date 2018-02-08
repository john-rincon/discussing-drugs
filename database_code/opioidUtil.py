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
    return profile
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
            cur.execute('Select body, created_utc From Comment JOIN Subreddit '
                        'WHERE Subreddit.subreddit_id = Comment.subreddit_id AND Comment.created_utc > :start AND '
                        'Comment.created_utc < :end AND Subreddit.subreddit_name=:sub_name',
                        {"end":end_time,"start":start_time, "sub_name":subreddit})
        else:
            cur.execute('Select body, created_utc From Comment JOIN Subreddit '
                        'WHERE Subreddit.subreddit_id = Comment.subreddit_id AND Comment.created_utc > :start AND '
                        'Comment.created_utc < :end AND Subreddit.subreddit_name=:sub_name AND '
                        'Comment.parent_id=Comment.link_id',{"end": end_time, "start": start_time, "sub_name": subreddit})
            # cur.execute('Select body, created_utc From Comment WHERE created_utc > :start AND created_utc < :end AND '
                        # 'parent_id = link_id', {"end": end_time, "start": start_time})
        output= cur.fetchall()
        return output

# getCommentAndTime(work_file, 'opiates',1,99999999999,1)

def getFrequentPosters(work_file,subreddit,threshold,start_time=0,end_time=0):
    import sqlite3 as sqlite
    with sqlite.connect(work_file) as con:
        cur = con.cursor()
        # cur.execute("select * from people where name_last=:who and age=:age", {"who": who, "age": age})
        cur.execute("SELECT subreddit_id FROM Subreddit WHERE subreddit_name=:sub_name", {"sub_name": subreddit})
        sub_id = cur.fetchall()
        sub_id = sub_id[0][0]
        cur.execute("SELECT COUNT(*) FROM Comment WHERE subreddit_id=:sub_id and user_id != '[deleted]'", {"sub_id": sub_id})
        total=cur.fetchall()
        total=total[0][0]
        # print total
        if end_time==0:
            sub_id='t5_2r0y3'
            cur.execute("SELECT user_id, COUNT(*) FROM Comment WHERE subreddit_id=:sub_id and user_id != '[deleted]' GROUP BY user_id "
                        "ORDER BY COUNT(*) DESC", {"sub_id":sub_id})
        else:
            cur.execute(
                "SELECT user_id, COUNT(*) FROM Comment WHERE subreddit_id=:sub_id AND created_utc < :end"
                " AND created_utc > :start AND user_id != '[deleted]' GROUP BY user_id "
                "ORDER BY COUNT(*) DESC", {"sub_id": subreddit,"end":end_time,"start":start_time})
        descendingList= cur.fetchall()
        currentSum=0
        frequentList=[]
        for user in descendingList:
            if currentSum >= total*threshold:
                break
            else:
                frequentList.append(user)
                currentSum+=user[1]
        return frequentList

def findPopularPosts(work_file,subreddit,threshold=0,start_time=0,end_time=0):
    import sqlite3 as sqlite
    with sqlite.connect(work_file) as con:
        cur = con.cursor()
        cur.execute("SELECT subreddit_id FROM Subreddit WHERE subreddit_name=:sub_name", {"sub_name": subreddit})
        sub_id = cur.fetchall()
        sub_id=sub_id[0][0]
        cur.execute("SELECT SUM(score) FROM Comment WHERE subreddit_id=:sub_id and score > 0",{"sub_id":sub_id})
        totalScore=cur.fetchall()
        totalScore=totalScore[0][0]
        cur.execute(
            "SELECT score,body FROM Comment WHERE subreddit_id=:sub_id AND score > 0 "
            "ORDER BY score DESC", {"sub_id":sub_id})
        allPosts=cur.fetchall()
        popularPosts = []
        currentSum=0
        for post in allPosts:
            if currentSum >= totalScore * threshold:
                break
            else:
                popularPosts.append(post)
                currentSum += post[0]
        return popularPosts

# print x

def makeDistributionGraph(input,numberIndex,xLabel,yLabel,title,color):
    import matplotlib.pyplot as plt
    total=0
    for post in input:
        total+=int(post[numberIndex])
    total=total+0.00
    xPoints=[0]
    yPoints=[0]
    i=1
    percentTotal=0.0
    for post in input:
        xPoints.append(i)
        i+=1
        if percentTotal==0.0:
            maxPercent= post[numberIndex]/total
        thisPercent=int(post[numberIndex])/total
        percentTotal+=thisPercent
        yPoints.append(thisPercent)
    # print yPoints[:100]
    # print xPoints[:100]
    line=plt.plot(xPoints,yPoints)

    plt.axis([-25,len(input),0,maxPercent+maxPercent*.1])
    plt.setp(line,'color',color,'linewidth',3.0,'ls','-')
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.title(title)
    plt.show()


# work_file='reddit-opiates.db'
#
# x= findPopularPosts(work_file,'opiates',1)
#
# # makeDistributionGraph(x,0,"Distribution of Comment Scores as Percent of Total")
#
# y=getFrequentPosters(work_file,'opiates',1)
# print y
# print len(y)
# makeDistributionGraph(x,0,'Comment Count','Percent of Total',"Distribution of Comment Scores as Percent of Total",'r')