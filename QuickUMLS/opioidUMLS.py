from nltk.corpus import stopwords
commonWords=open('commonWords.txt').read().decode('utf-8').splitlines()
nltkWords = stopwords.words('english')
allStopWords=set(commonWords+nltkWords)

def removeCommonWords(text):
    text=text.lower()
    text = ' '.join([word for word in text.split() if word not in allStopWords])
    return text

def createUMLSTable(work_file):
    import sqlite3 as sqlite
    with sqlite.connect(work_file) as con:
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS UMLS_Entities")
        cur.execute('''CREATE TABLE UMLS_Entities(umls_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, comment_id TEXT,
        term TEXT, semtype TEXT, cui TEXT)''')


def findUMLSTerms(work_file,types):
    import sqlite3 as sqlite
    from quickumls import QuickUMLS
    quickumls_fp = '/usr/share/QuickUMLS-master/quickUMLS-install'  ###will need to do all this in scratch
    matcher = QuickUMLS(quickumls_fp, 'length', .8, 5, 'jaccard', 3, types)

    with sqlite.connect(work_file) as con:
        ###query database for text
        cur = con.cursor()
        # cur.execute("DELETE FROM UMLS_Entities")
        cur.execute("SELECT comment_id FROM UMLS_Entities WHERE ROWID= (SELECT MAX(ROWID) FROM UMLS_Entities)")
        commentID=cur.fetchall()
        if commentID: ####fetch appropriate rowID
            # print 'found row'
            commentID=commentID[0][0]
            cur.execute("SELECT ROWID FROM Comment WHERE comment_id=:commentID",{'commentID':commentID})
            counter=cur.fetchall()
            counter=counter[0][0]+1
            # print counter
        else: ## start form beginning
            counter=1
            # print 'here'
        #
        cur.execute("SELECT MAX(ROWID) FROM Comment")
        total=cur.fetchall()
        rowLimit=total[0][0]
        # print counter
        while counter <= rowLimit:
            cur.execute("SELECT comment_id,body FROM Comment WHERE ROWID=:row_id",{'row_id':counter})
            counter+=1
            commentValues=cur.fetchall()
            text=commentValues[0][1]
            text = removeCommonWords(text)
            if len(text)==0: continue
            commentID=commentValues[0][0]
            # print text
            umlsTerms = matcher.match(text, best_match=True, ignore_syntax=False)
            umlsString = "INSERT OR IGNORE INTO UMLS_Entities (comment_id, term, semtype, cui) VALUES (?,?,?,?)"
            for line in umlsTerms:
                for term in line:
                    semTypes = term['semtypes']
                    semString = ''
                    for thisType in semTypes:
                        if thisType in types:
                            semString = thisType
                            break
                    umlsValues = [commentID,term['term'], semString,term['cui']]
                    cur.execute(umlsString,umlsValues)
            if counter % 1000 == 0:  ###return every thousand in case of crash
                con.commit()
            # return commentValues


types=[
'T023',  # Body Part, Organ, or Organ Component
'T031',  # Body Substance
'T060',  # Diagnostic Procedure
'T047',  # Disease or Syndrome
'T200',  # Clinical Drug
'T203',  # Drug Delivery Device
'T033',  # Finding
'T184',  # Sign or Symptom
'T034',  # Laboratory or Test Result
'T037',  # Injury or Poisoning
'T061',  # Therapeutic or Preventive Procedure
'T048',  # Mental or Behavioral Dysfunction
'T046',  # Pathologic Function
'T121',  # Pharmacologic Substance
'T201']  # Clinical Attribute


# createUMLSTable('/home/john/Desktop/discussing-drugs/database_code/reddit-opiates.db')

findUMLSTerms('/home/john/Desktop/discussing-drugs/database_code/reddit-opiates.db',types)




# matcher= QuickUMLS(quickumls_fp,overlapping_criteria,threshold,similarity_name,window,accepted_semtypes)

# filePath ='/home/john/Desktop/brat-v1.3_Crunchy_Frog/data/to-annotate/617-classified.txt'

def openFileAsString(path):
    with open(path,'r') as myfile:
        data=myfile.read()
        return data
# text=openFileAsString(filePath)


# print x


# print allStopWords
# print commonWords
