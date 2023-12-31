from flask import Blueprint, Flask,render_template,request,jsonify,make_response,redirect,url_for ,session,flash
from functions import *
seller_page=Blueprint(
    "artifusion/seller",__name__,static_folder="static",
    template_folder="templates")

#seller-home
@seller_page.route("/home")
def sellerhome():
    user_data= session.get('login')
    print(user_data)
    sellerid=user_data[0]
    cursor=db.cursor()
    cursor.execute('SELECT COUNT(*) FROM demoorders WHERE sellerid="{0}"'.format(sellerid))
    c=cursor.fetchall()[0]
    cursor.close()
    
    cursor1=db.cursor()
    cursor1.execute('SELECT totamt FROM demoorders WHERE sellerid="{0}"'.format(sellerid))
    count=cursor1.fetchall()
    print(count)
    tot=0
    cursor1.close()   
         
    for i in range(len(count)):
        b=count[i][0]
        print(b)
        tot+=b
    print('total amt = ',tot)
    
    totamt='₹'+str(tot)
    countorders=c[0]
    print('countorders = ',countorders)
    
    cursor2=db.cursor()
    cursor2.execute('SELECT COUNT(*) FROM products WHERE sellerid = {}'.format(user_data[0]))
    prodscount=cursor2.fetchall()[0]
    print(prodscount)
    cursor2.close()
    
    data,imgdata=getdata('seller',user_data[4])
    return render_template("sellerhome.html",user_data=user_data,imgdata=imgdata,countorders=countorders,totamt=totamt,prodscount=prodscount)

#seller-order
@seller_page.route("/order")
def order():
    user_data= session.get('login')
    data,imgdata=getdata('seller',user_data[4])
    sellerid=user_data[0]
    cursor1=db.cursor()
    cursor1.execute('SELECT buyerid,productid,shipping_addr,proddetail,totamt,paymethod,orderstatus,orderdate FROM demoorders WHERE sellerid="{0}"'.format(sellerid))
    orderdata=cursor1.fetchall()
    print(orderdata)
    print(len(orderdata))
    return render_template("sellorders.html",user_data=user_data,imgdata=imgdata,orderdata=orderdata)

@seller_page.route("/products")
def products():
    user_data= session.get('login')
    data,imgdata=getdata('seller',user_data[4])
    return render_template("sellproducts.html",user_data=user_data,imgdata=imgdata)

@seller_page.route("/products",methods=["POST"])
def pprods():
    user_data= session.get('login')
    data,imgdata=getdata('seller',user_data[4])
    req =request.get_json()
    if(req):
        cursor =db.cursor()
        print(user_data[0])
        cursor.execute('SELECT * FROM products WHERE sellerid = {}'.format(user_data[0]))
        count=cursor.fetchall()
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
        js=json.dumps('hi im hacky')
        js1=json.dumps(dictarr)
        return ({'js':js1,'status_code':200})
  

@seller_page.route("/products/create-new",methods=['POST'])
def createnewprod():
    req=request.get_json()
    if(req):
        print(req['pname'])
        base64img=req['pimgarr'][0]
        user_data= session.get('login')
        cursor=db.cursor()
        try:
            query="INSERT INTO products (prodname,prodprice,proddesc,qtyavail,prodimg1,prodimg2,prodimg3,sellerid,category) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            values=(req['pname'],req['pprice'],req['pdesc'],req['pqty'],req['pimgarr'][0],req['pimgarr'][1],req['pimgarr'][2],user_data[0],req['prodcat'])
            cursor.execute(query,values)
            db.commit()
        except Exception as e:
            print("exception",e)
        cursor.close()           
        return jsonify({'status_code': 200, 'imgdata':'hello hi' })

    else:
        print('problem iruku')
        return jsonify({'status_code': 500, 'imgdata':''})
   

#seller-home
@seller_page.route("/review")
def review():
    user_data={'firstname':'user name','emailid':'user@gmail.com'}
    user_data= session.get('login')
    data,imgdata=getdata('seller',user_data[4])
    return render_template("sellreview.html",user_data=user_data,imgdata=imgdata)

#seller
@seller_page.route("/userprofile")
def sellerprofile():
    user_data=session.get('login')
    print("-------------------------------------")
    print(user_data)
    data,imgdata=getdata('seller',user_data[4])
    return render_template("sellerprofile.html",user_data=user_data,imgdata=imgdata)

@seller_page.route("/userprofile/edit",methods=['POST'])
def editsprof():
    user_data=session.get('login')
    data,imgdata=getdata('seller',user_data[4])
    req=request.get_json()
    if(req):
        query=''
        values=()
        cursor=db.cursor()

        if req['pwd']=='':
            query="UPDATE demoseller2 SET firstname = %s,lastname = %s,phone = %s,address = %s,profile = %s,shopname=%s   WHERE email= %s"
            values=(req['fname'],req['lname'],req['phone'],req['addr'],req['pimgarr'],req['shop'],user_data[4])
        else:
            query="UPDATE demoseller2 SET firstname = %s,lastname = %s,phone = %s,address = %s,password = %s,profile = %s,shopname=%s   WHERE email= %s"
            values=(req['fname'],req['lname'],req['phone'],req['addr'],req['pwd'],req['pimgarr'],req['shop'],user_data[4])
        
        cursor.execute(query,values)
        db.commit()
        cursor.close()   
        session['login'],imgstr=getdata('seller',user_data[4])
        user_data=session.get('login')
        return ({'status_code': 200, 'imgdata': 'hi'})

    else:
        print('problem iruku')
        return ({'status_code': 500, 'imgdata':''})   

