import json
from flask import jsonify ,session
from database1 import initialize_db

db=initialize_db()

#global imgstr
def removeblob(img): 
    string_number = str(img)
    trimstr =string_number.rstrip()
    imgstr = f"{trimstr[2:-1]}"
    return imgstr

def tupletolist(tuple,list):
    for elem in tuple:
        temp=[]
        for item in elem:
            temp.append(item)
        list.append(temp)


def getdata(table,mail):
    img='please god help me--------------------------------'
    if table=='buyer':    
        cursor2=db.cursor()
        cursor1=db.cursor()
        
        print("from getdata fn",table ,mail)
        #try:
        cursor2.execute('SELECT buyerid,firstname,lastname,phone,email,address FROM demouser2 WHERE email = "{}"'.format(mail) )
        udata=cursor2.fetchone()  
        cursor1.execute('SELECT profile FROM demouser2 WHERE email = "{}"'.format(mail))
        img=cursor1.fetchone()[0]
        cursor1.close()
        print(img)
        #except Exception as e:
        #print('problem iruku pola-----------------------------')
        #print(e)
        #   print(img)
        
    elif table=='seller':#seller  
        print("hello")  
        print("mail : ",mail)
        print('table: ',table)
        cursor2=db.cursor()
        cursor1=db.cursor()
        cursor2.execute('SELECT sellerid,firstname,lastname,phone,email,address,shopname FROM demoseller2 WHERE email = "{}"'.format(mail) )
        udata=cursor2.fetchone()
        print(udata)
        print(type(udata))
        cursor1.execute('SELECT profile FROM demoseller2 WHERE email = "{}"'.format(mail))
        img1=cursor1.fetchone()
        print(img1)
        print(type(img1))
        img=img1[0]
        print('image is not none')

        '''
        if img1 is not None:
            img=img1[0]
            print('image is not none')
        else:
            img=None
            print('image is none')
        '''
        cursor1.close()
    else:#admin
        print("hi , hello bye")
        cursor2=db.cursor()
        cursor1=db.cursor()
        cursor2.execute('SELECT id,firstname,lastname,phone,email FROM admindemo WHERE email = "{}"'.format(mail) )
        udata=cursor2.fetchone()
    #    print(udata)
        cursor1.execute('SELECT profile FROM admindemo WHERE email = "{}"'.format(mail))
        img=cursor1.fetchone()[0]
        print(img)
        cursor1.close()
        

    #print(img)
    cursor2.close()
    cursor1.close()
   # print(udata)
    #if len(img)>5: 
    imgstr=''
    print("----outer---")
    print(img)
    if img is not None:    
        print('hi image is present')
        string_number = str(img)
        trimstr =string_number.rstrip()
        imgstr = f"{trimstr[2:-1]}"

    session['login']=udata
    a=session['login']
    ##print(udata)
    #a=session['userdb']#0-id,1-firstname,2-lastname,3-phone,4-mail,5-pwd,6-prof 
    #print(a)
    return a,imgstr

def showprod(place):
    user_data= session.get('login')  
    print(user_data[0],place)
    cursor4=db.cursor()
    print("hello da botu ")
    cursor4.execute('SELECT productid FROM {} WHERE buyerid="{}"'.format(place,user_data[0]))
    prods=cursor4.fetchall()
    cursor4.close()
    print(prods)
    prodarr=[]
    #print(prods[0][0])
    #print(prods[1][0])
    #print(len(prods))
    if prods:
        for i in range(len(prods)):
            print(prods[i][0],"-----------------------------")
            prodarr.append(prods[i][0])
        print(prodarr)
        cursor2=db.cursor()
        placeholders = ', '.join(['%s'] * len(prodarr))
        query = f"SELECT * FROM products WHERE productid IN ({placeholders})"
        cursor2.execute(query,prodarr)
        count=cursor2.fetchall()
        cursor2.close()
        dictarr=[]
        countlist=[]
        keys=['productid','prodname','prodprice','proddesc','qtyavail','qtysold','prodimg1','prodimg2','prodimg3','netamt','sellerid']
        for i in  range(len(count)):#6,7,8
            countlist.append(list(count[i]))

        for i in range(len(countlist)):            
            countlist[i][6]=removeblob(countlist[i][6])
            countlist[i][7]=removeblob(countlist[i][7])
            countlist[i][8]=removeblob(countlist[i][8])
            dictarr.append(dict(zip(keys,countlist[i])))
        js1=json.dumps(dictarr)
       # print(js1)
        return js1


def insertwish(pid,uid):
    try:
        cursor1=db.cursor()
        query='INSERT INTO wishlist (productid,buyerid) VALUES(%s,%s)'
        values=(pid,uid)
        cursor1.execute(query,values)
        db.commit()
        cursor1.close()
    except Exception as e:
        print("excetption ",e)
        return jsonify({'status_code':404,'message':'error occured'})
    return jsonify({'status_code':200,'message':'success'})
            
