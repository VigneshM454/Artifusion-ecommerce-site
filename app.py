import json
from database1 import initialize_db
from flask import Flask,render_template,request,jsonify,make_response,redirect,url_for ,session,flash
import base64
from functions import *
from admin import admin_page
from buyer import buyer_page
from seller import seller_page
import time
app=Flask(__name__)
app.secret_key='hackylazy'
db=initialize_db()

app.register_blueprint(admin_page,url_prefix="/artifusion/admin")
app.register_blueprint(buyer_page,url_prefix="/artifusion/buyer")
app.register_blueprint(seller_page,url_prefix="/artifusion/seller")

@app.route("/")
def copy():
    return render_template("index2.html")

#login/signin/frontpage
@app.route("/artifusion")
def home():
    return render_template("login.html")

@app.route("/artifusion/login-user",methods=['POST'])
def checkdata():
    req=request.get_json()
    if(req):
        tem=req['testemail']
        pwd=req['testpwd']
        print(tem, pwd)
        cursor=db.cursor()
        cursor.execute('SELECT COUNT(*) FROM demouser2 WHERE email="{0}" AND password="{1}"'.format(tem, pwd))
        count=cursor.fetchone()[0]
        cursor.close()
        if count==0:
             print("invalid")
             res=make_response(jsonify({'message':'Incorrect login details'}),400)
             return res
        else:
            print('Successfully loged in')
            session['login'],imgstr=getdata('buyer',tem)
            res=make_response(jsonify({'message':'Json Received in user login account'}),200)
            return res
        
        
@app.route("/artifusion/create-user",methods=['POST'])
def handledata():
    req =request.get_json()
    if req:
        print(req)
        print(req['firstname'])
        em=req['emailid']
        print(em)
        demoimg="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA0NDggNTEyIj48IS0tISBGb250IEF3ZXNvbWUgUHJvIDYuNC4yIGJ5IEBmb250YXdlc29tZSAtIGh0dHBzOi8vZm9udGF3ZXNvbWUuY29tIExpY2Vuc2UgLSBodHRwczovL2ZvbnRhd2Vzb21lLmNvbS9saWNlbnNlIChDb21tZXJjaWFsIExpY2Vuc2UpIENvcHlyaWdodCAyMDIzIEZvbnRpY29ucywgSW5jLiAtLT48cGF0aCBkPSJNMjI0IDI1NkExMjggMTI4IDAgMSAwIDIyNCAwYTEyOCAxMjggMCAxIDAgMCAyNTZ6bS00NS43IDQ4Qzc5LjggMzA0IDAgMzgzLjggMCA0ODIuM0MwIDQ5OC43IDEzLjMgNTEyIDI5LjcgNTEySDQxOC4zYzE2LjQgMCAyOS43LTEzLjMgMjkuNy0yOS43QzQ0OCAzODMuOCAzNjguMiAzMDQgMjY5LjcgMzA0SDE3OC4zeiIvPjwvc3ZnPg=="
        cursor=db.cursor()
        cursor.execute('SELECT COUNT(*) FROM demouser2 WHERE email="{}"'.format(em))
        count=cursor.fetchone()[0]
        cursor.close()
        if count>0:
            res=make_response(jsonify({'message':'Json Received in user create account'}),404)
            return jsonify({'status_code': 404, 'user_data':'', 'redirect_url': url_for('home')})
        else:
            print('User added successfully')
            cursor=db.cursor()
            query="INSERT INTO demouser2 (firstname,lastname,email,password,phone,address,profile) VALUES(%s,%s,%s,%s,%s,%s,%s)"
            values=(req['firstname'],req['lastname'],req['emailid'],req['passwd'],req['phoneno'],req['address'],demoimg)
            try:
                cursor.execute(query,values)
                db.commit()
                print('Account Created successfully')                  
                res=make_response(jsonify({'message':'Json Received in user create account'}),200)
                cursor.close()

            except Exception as e:
                print('excetpion',e)
                return jsonify({'status_code': 400, 'user_data':"demo", 'redirect_url': url_for('home'),'res':'json receied-'})
            #else:     
            session['login'],imgstr=getdata('buyer',req['emailid'])
            print('validity')  
            return jsonify({'status_code': 200, 'user_data':"demo"})
    else:
        return jsonify({'status_code': 500, 'user_data':'', 'redirect_url': url_for('home')})
        
#seller-home
@app.route("/artifusion/login-seller",methods=['POST'])
def checksellerdata():
    req=request.get_json()
    if(req):
        print(req)
        tem=req['testemail']
        pwd=req['testpwd']
        print(tem, pwd)
        cursor3=db.cursor()
        cursor3.execute('SELECT COUNT(*) FROM demoseller2 WHERE email="{0}" AND password="{1}"'.format(tem, pwd))
        count=cursor3.fetchone()[0]
        cursor3.close()
        if count==0:
             print("invalid")
             res=make_response(jsonify({'message':'Incorrect login details'}),400)
             return res
        else:
            print('Successfully loged in')
            session['login'],imgstr=getdata('seller',tem)
            res=make_response(jsonify({'message':'Json Received in seller login account'}),200)
            return res
        
        
@app.route("/artifusion/create-seller",methods=['POST'])
def handlesellerdata():
    req =request.get_json()
    if req:
        print(req)
        
        em=req['emailid']
        ar=req['category']
        demoimg="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA0NDggNTEyIj48IS0tISBGb250IEF3ZXNvbWUgUHJvIDYuNC4yIGJ5IEBmb250YXdlc29tZSAtIGh0dHBzOi8vZm9udGF3ZXNvbWUuY29tIExpY2Vuc2UgLSBodHRwczovL2ZvbnRhd2Vzb21lLmNvbS9saWNlbnNlIChDb21tZXJjaWFsIExpY2Vuc2UpIENvcHlyaWdodCAyMDIzIEZvbnRpY29ucywgSW5jLiAtLT48cGF0aCBkPSJNMjI0IDI1NkExMjggMTI4IDAgMSAwIDIyNCAwYTEyOCAxMjggMCAxIDAgMCAyNTZ6bS00NS43IDQ4Qzc5LjggMzA0IDAgMzgzLjggMCA0ODIuM0MwIDQ5OC43IDEzLjMgNTEyIDI5LjcgNTEySDQxOC4zYzE2LjQgMCAyOS43LTEzLjMgMjkuNy0yOS43QzQ0OCAzODMuOCAzNjguMiAzMDQgMjY5LjcgMzA0SDE3OC4zeiIvPjwvc3ZnPg=="
        #def index():
        cursor=db.cursor()
        cursor.execute('SELECT COUNT(*) FROM demoseller2 WHERE email="{}"'.format(em))
        count=cursor.fetchone()[0]
        print(count)
        cursor.close()
        if count>0:
            res=make_response(jsonify({'message':'An account with same mail id  already exist'}),300)
            return res
        else:
            cursor1=db.cursor()
            query="INSERT INTO demoseller2 (firstname,lastname,email,password,phone,address,shopname,category,profile) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            values=(req['firstname'],req['lastname'],req['emailid'],req['passwd'],req['phoneno'],req['address'],req['shop'],req['category'],demoimg)
            try:# sellerid,firstname,lastname,phone,email,address,shopname 
                #demoimg
                cursor1.execute(query,values)
                db.commit()
                cursor1.close()
                print('Account Created successfully')                              
                session['login'],imgstr=getdata('seller',em)
                print('no exception')
                res=make_response(jsonify({'message':'Json Received in user create account'}),200)
                return res

            except Exception as e:
                print('excetpion',e)
                res=make_response(jsonify({'message':'problems'}),550)
                return res
    else:
            res=make_response(jsonify({'message':'problem'}),404)
            return res

'''    
@app.route("/artifusion/login-admin",methods=['POST'])
def handleadmin():
    req=request.get_json()
    if req:
        aearr=['vignesh@gmail.com','hackylazy454@gmail.com','hacky@gmail.com']
        aparr=['password1','password2','password3']  
        tem=req['testemail']
        tpwd=req['testpwd']
        val=0
        for i in range(3):
            if tem==aearr[i] and tpwd==aparr[i]:
                val=1  
                break
            else:
                val=0
                
        if val==0:
            print("invalid")
            res=make_response(jsonify({'message':'Incorrect login details'}),400)
        else:
            print('Successfully loged in')
            res=make_response(jsonify({'message':'Json Received in seller login account'}),200)    
    return res         
'''  
@app.route("/artifusion/admintest", methods=['POST'])
def testadmin():
    print('hello')
    req=request.get_json()
    if req:
        print("******************************************")
        print(req)
        em=req['testemail']
        pd=req['testpwd']
        cursor1=db.cursor()
        try:
            cursor1.execute("SELECT COUNT(*) FROM admindemo WHERE email= '{0}' AND password= '{1}'".format(em,pd))
            count=cursor1.fetchone()[0]
            cursor1.close()
            print(count)
            # if count==0:
            #    return jsonify({'message':"demo message",'status_code':404})
            if count ==1:
                print('Successfully loged in')
                session['login'],imgstr=getdata('admin',em)
                print("--------------------------------------")
                return jsonify({'message':"demo message",'status_code':200})
            else:
                return jsonify({'message':"demo message",'status_code':300})
        except Exception as e:
             return jsonify({'message':e,'status_code':454})
   
#/artifusion/userprofile/edit
@app.route("/artifusion/about")
def about():
    user_data=session.get('login')
    data,imgdata=getdata('buyer',user_data[4])
    return render_template("about.html",user_data=user_data,imgdata=imgdata)

@app.route("/artifusion/buyer/logout")
def logout():
    session.clear()
    return redirect('/artifusion')

@app.route("/artifusion/seller/logout")
def logoutseller():
    session.clear()
    print(session)
    return redirect('/artifusion')

@app.route("/artifusion/admin/logout")
def adminseller():
    session.clear()
    return redirect('/artifusion')

@app.route("/artifusion/payment")
def payment():
    return render_template('payment.html')
    
app.run(debug=True)

'''
                demodata={}
                demodata['sellerid'] 
                demodata['firstname'] 
                demodata['lastname'] 
                demodata['phone'] 
                demodata['email'] 
                demodata['address'] 
                demodata[''] 
'''

'''
        copydata=dict(req)
        print("///////////////////////////////////////////")
        print(copydata)
        print("///////////////////////////////////////////")
        copydata.pop('passwd')
        loginarr=[]
        for value in copydata.values():
            print(values)
            loginarr.append(values)
            print(loginarr)
            logintuple=tuple(loginarr)
            print("login tuple ", logintuple)
            print('copydata')
            print(copydata)
            #session['login'],imgstr=logintuple,demoimg
'''    
               