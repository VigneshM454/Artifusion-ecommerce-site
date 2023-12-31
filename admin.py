from flask import Blueprint, Flask,render_template,request,jsonify,make_response,redirect,url_for ,session,flash
from functions import *
admin_page=Blueprint(
    "artifusion/admin",__name__,static_folder="static",
    template_folder="templates")


@admin_page.route("/order")
def aorder():
    user_data= session.get('login')
    data,imgdata=getdata('admin',user_data[4])
    cursor1=db.cursor()
    cursor1.execute('SELECT  buyerid,sellerid,shipping_addr,orderstatus,orderdate,proddetail,totamt,paymethod FROM demoorders ')
    ordertable=cursor1.fetchall()
    cursor1.close()
        
    return render_template("adminorder.html",ordertable=ordertable,user_data=user_data,imgdata=imgdata)

@admin_page.route("/product")
def aprod():
    user_data= session.get('login')
    data,imgdata=getdata('admin',user_data[4])
    #prod table
    cursor2=db.cursor()
    cursor2.execute('SELECT prodimg1,prodname,prodprice,proddesc,qtyavail,sellerid FROM products')
    prodtable=cursor2.fetchall()
    #prodtable=list(prodtable1)
    cursor2.close()
    prodtable1=[]
    tupletolist(prodtable,prodtable1)
    '''
    for elem in prodtable:
        temp=[]
        for item in elem:
            temp.append(item)
        prodtable1.append(temp)
    '''
    for i in range(len(prodtable1)):
        a=removeblob(prodtable1[i][0])
        prodtable1[i][0]=a
    
    return render_template("adminprod.html",prodtable=prodtable1,user_data=user_data,imgdata=imgdata)
   
@admin_page.route("/buyer")
def abuyer():
    user_data= session.get('login')
    data,imgdata=getdata('admin',user_data[4])
    #buyer table
    cursor1=db.cursor()
    cursor1.execute('SELECT * from demouser2')
    buyertable=cursor1.fetchall()
    buyertable1=[]
    tupletolist(buyertable,buyertable1)
    for i in range(len(buyertable1)):
        a=removeblob(buyertable1[i][7])
        buyertable1[i][7]=a
    cursor1.close()
    return render_template("adminbuyer.html",buyertable1=buyertable1,user_data=user_data,imgdata=imgdata)

@admin_page.route("/seller")
def aseller():
    user_data= session.get('login')
    data,imgdata=getdata('admin',user_data[4])
    #seller table
    cursor1=db.cursor()
    cursor1.execute("SELECT profile,firstname,lastname,phone,email,address,shopname from demoseller2")    
    sellertable=cursor1.fetchall()
    sellertable1=[]
    tupletolist(sellertable,sellertable1)
    for i in range(len(sellertable1)):
        a=removeblob(sellertable1[i][0])
        sellertable1[i][0]=a
    cursor1.close()    
    return render_template("adminseller.html",sellertable1=sellertable1,user_data=user_data,imgdata=imgdata)

@admin_page.route("/home")
def ahome():
    print("in seller home page")
    #user_data={'firstname':'user name','emailid':'user@gmail.com'}
    user_data= session.get('login')
    data,imgdata=getdata('admin',user_data[4])
    print(user_data) 
    
    cursor2=db.cursor()
    cursor2.execute("SELECT COUNT(*) FROM demoorders ")
    ordercount=cursor2.fetchone()[0]
    cursor2.close()

    cursor2=db.cursor()
    cursor2.execute("SELECT COUNT(*) FROM demouser2 ")
    usercount=cursor2.fetchone()[0]
    cursor2.close()

    cursor2=db.cursor()
    cursor2.execute("SELECT COUNT(*) FROM products ")
    prodcount=cursor2.fetchone()[0]
    cursor2.close()

    cursor2=db.cursor()
    cursor2.execute("SELECT totamt FROM demoorders ")
    orderprice=cursor2.fetchall()
    tot=0
    print(orderprice)
    cursor2.close()
    for i in range(len(orderprice)):
        tot+=orderprice[i][0]
    
    print(tot)
    '''    
    #0- orderid, 1-buyerid, 2-productid, 3-shiping_addr
    #4- proddetail, 5- totamt, 6- paymethod, 7- orderstatus, 
    #8- orderdate, 9- sellerid  
    #return render_template("sellorders.html",user_data=user_data,imgdata=imgdata,orderdata=orderdata)
    '''
    return render_template("adminhome.html",user_data=user_data,imgdata=imgdata,ordercount=ordercount,usercount=usercount,prodcount=prodcount,tot=tot)

@admin_page.route("/userprofile")
def adminprofile():
    user_data=session.get('login')
    print("-------------------------------------")
    print(user_data)
    data,imgdata=getdata('admin',user_data[4])
    return render_template("adminprofile.html",user_data=user_data,imgdata=imgdata)

@admin_page.route("/userprofile/edit",methods=['POST'])
def editsadminprof():
    user_data=session.get('login')
    data,imgdata=getdata('admin',user_data[4])
    req=request.get_json()
    if(req):
        query=''
        values=()
        cursor=db.cursor()

        if req['pwd']=='':
            query="UPDATE admindemo SET firstname = %s,lastname = %s,phone = %s,profile = %s   WHERE email= %s"
            values=(req['fname'],req['lname'],req['phone'],req['pimgarr'],user_data[4])
        else:
            query="UPDATE admindemo SET firstname = %s,lastname = %s,phone = %s,password = %s,profile = %s   WHERE email= %s"
            values=(req['fname'],req['lname'],req['phone'],req['pwd'],req['pimgarr'],user_data[4])
        
        cursor.execute(query,values)
        db.commit()
        cursor.close()   
        session['login'],imgstr=getdata('admin',user_data[4])
        user_data=session.get('login')
        return jsonify({'status_code': 200, 'imgdata': 'hi'})

    else:
        print('problem iruku')
        return jsonify({'status_code': 500, 'imgdata':'bye'})   

