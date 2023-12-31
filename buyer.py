import json
from flask import Blueprint, Flask,render_template,request,jsonify,make_response,redirect,url_for ,session,flash
from functions import *

checkdatajs=[]
checkdataobj={}

buyer_page=Blueprint(
    "artifusion/buyer",__name__,static_folder="static",
    template_folder="templates")

#buyer-home
@buyer_page.route("/")
def buyhome():
    user_data= session.get('login')
    data,imgdata=getdata('buyer',user_data[4])
    return render_template('home.html',user_data=user_data,imgdata=imgdata)

@buyer_page.route("/",methods=["POST"])
def buyhome1():
    user_data= session.get('login')
    #data,imgdata=getdata('seller',user_data[4])
    req =request.get_json()
    if(req):
        #cursor =db.cursor()
        #cursor.execute('SELECT * FROM products')
        #count=cursor.fetchall()
        
        cursor1=db.cursor()
        cursor1.execute('SELECT productid, prodname,prodprice,prodimg1,category FROM products')
        count2=cursor1.fetchall()
        cursor1.close()
        print("---------------------------------")
       # print(count2)
        dictarr2=[]
        countlist2=[]
        keys2=['productid','prodname','prodprice','prodimg1','category']

        for i in  range(len(count2)):#6,7,8
            countlist2.append(list(count2[i]))

        for i in range(len(countlist2)):            
            countlist2[i][3]=removeblob(countlist2[i][3])
            dictarr2.append(dict(zip(keys2,countlist2[i])))
        js22=json.dumps(dictarr2)
        print(js22)

        print("---------------------------------")
        '''
        print(len(count))
        dictarr=[]
        countlist=[]
        keys=['productid','prodname','prodprice','proddesc','qtyavail','qtysold','prodimg1','prodimg2','prodimg3','netamt','sellerid','category']
        for i in  range(len(count)):#6,7,8
            countlist.append(list(count[i]))

        for i in range(len(countlist)):            
            countlist[i][6]=removeblob(countlist[i][6])
            countlist[i][7]=removeblob(countlist[i][7])
            countlist[i][8]=removeblob(countlist[i][8])
            dictarr.append(dict(zip(keys,countlist[i])))
        js=json.dumps('hi im hacky')
        js1=json.dumps(dictarr)
        js2=jsonify(countlist)
        js3=jsonify(dictarr)
        # return ({'js':js1,'status_code':200})
        '''
        return ({'js':js22,'status_code':200})


@buyer_page.route("/searchdemo",methods=["POST"])
def searchprods():
    req =request.get_json()
    if(req):
        cursor =db.cursor()
        cursor.execute('SELECT * FROM products where prodname like "%{}%" '.format(req))
        count=cursor.fetchall()
        dictarr=[]
        countlist=[]
        keys=['productid','prodname','prodprice','proddesc','qtyavail','qtysold','prodimg1','prodimg2','prodimg3','netamt','sellerid','category']
        for i in  range(len(count)):#6,7,8
            countlist.append(list(count[i]))

        for i in range(len(countlist)):            
            countlist[i][6]=removeblob(countlist[i][6])
            countlist[i][7]=removeblob(countlist[i][7])
            countlist[i][8]=removeblob(countlist[i][8])
            dictarr.append(dict(zip(keys,countlist[i])))
        #print(dictarr)
        js=json.dumps('hi im hacky')
        js1=json.dumps(dictarr)
        js2=jsonify(countlist)
        js3=jsonify(dictarr)
       # res=make_response(js,200)
        print(js1)
        return ({'js':js1,'status_code':200})
        #js=dictarr
        #print(js)


#wishlist
@buyer_page.route("/wishlist")
def wishlist():
    user_data=session.get('login')
    data,imgdata=getdata('buyer',user_data[4])
    return render_template("wishlist.html",user_data=user_data,imgdata=imgdata)

@buyer_page.route("/wishlist",methods=["POST"])
def wishlistshow():
    user_data= session.get('login')  
    req=request.get_json()
    cursor=db.cursor()#check product already in cart//  productid = "{0}" AND //req['productid'],
    cursor.execute('SELECT COUNT(*) FROM wishlist WHERE   buyerid="{0}"'.format(user_data[0]))
    count=cursor.fetchone()[0]
    cursor.close()
    print(count)
    
    if count==0:
        return ({'js':'demo','status_code':500})

    elif req:
            js1=showprod("wishlist") 
            print(js1)       
            return ({'js':js1,'status_code':200})

    else:
        return ({'js':"error",'status_code':404})

@buyer_page.route("/cart")
def cart():
    user_data=session.get('login')
    data,imgdata=getdata('buyer',user_data[4])
    return render_template("cart.html",user_data=user_data,imgdata=imgdata)

@buyer_page.route("/cart",methods=["POST"])
def cartshow():
    user_data= session.get('login')
    req=request.get_json()
    
    cursor=db.cursor()#check product already in cart//  productid = "{0}" AND //req['productid'],
    cursor.execute('SELECT COUNT(*) FROM cart WHERE   buyerid="{0}"'.format(user_data[0]))
    count=cursor.fetchone()[0]
    cursor.close()
    print(count)
    if count==0:
        return ({'js':'demo','status_code':500})

    elif req:
        js1=showprod('cart')
        return ({'js':js1,'status_code':200})

    else:
        return ({'js':"error",'status_code':404})

@buyer_page.route("/cart/remove",methods=['POST'])
def cartremove():
    req =request.get_json()
    user_data= session.get('login')
    if req:    
        print(req['productid'])        
        cursor2=db.cursor()
        cursor2.execute('DELETE  FROM cart WHERE productid = "{0}" AND  buyerid="{1}"'.format(req['productid'],user_data[0]))
        cursor2.close()
        return jsonify({'status_code':200,'message':'success'})
    else:
        return jsonify({'status_code':400,'message':'success'})

@buyer_page.route("/cart/later",methods=['POST'])
def cart2wishlist():
    req =request.get_json()
    user_data= session.get('login')
    if req:
        cursor=db.cursor()
        cursor.execute('DELETE FROM cart WHERE productid = "{}" AND buyerid = "{}"'.format(req['productid'],user_data[0]))    
        cursor.close()
        insertwish(req['productid'],user_data[0])
        return jsonify({'status_code':200,'message':'success'})


@buyer_page.route("/prod/wish",methods=["POST"])
def addwish():
    req =request.get_json()
    user_data= session.get('login')
    if req:
        print(req['productid'])
        cursor=db.cursor()#check product already in cart
        cursor.execute('SELECT COUNT(*) FROM cart WHERE productid = "{0}" AND  buyerid="{1}"'.format(req['productid'],user_data[0]))
        count=cursor.fetchone()[0]
        cursor.close()
        cursor2=db.cursor()#check product already in wihlist
        cursor2.execute('SELECT COUNT(*) FROM wishlist WHERE productid = "{0}" AND  buyerid="{1}"'.format(req['productid'],user_data[0]))
        count2=cursor2.fetchone()[0]
        cursor2.close()
        if count==0 and  count2==0:
            insertwish(req['productid'],user_data[0])
            return ({'status_code':200})
        else:
            return ({'status_code':300})
    else:
        print("no request recieved")
        return ({'status_code':500,'message':'error'})

@buyer_page.route("/prod/cart",methods=["POST"])
def addcart():
    req =request.get_json()
    print(req['productid'])
    user_data= session.get('login')
    if req:
        id=req['productid']
        cursor=db.cursor()#check product already in cart
        cursor.execute('SELECT COUNT(*) FROM cart WHERE productid = "{0}" AND  buyerid="{1}"'.format(req['productid'],user_data[0]))
        count=cursor.fetchone()[0]
        cursor.close()
        cursor2=db.cursor()#check product already in wihlist
        cursor2.execute('SELECT COUNT(*) FROM wishlist WHERE productid = "{0}" AND  buyerid="{1}"'.format(req['productid'],user_data[0]))
        count2=cursor2.fetchone()[0]
        if count==0:#if it is not already present in cart 
            if count2>0:
                cursor2.execute('DELETE  FROM wishlist WHERE productid = "{0}" AND  buyerid="{1}"'.format(req['productid'],user_data[0]))
                cursor2.close()
                #return

            try:
                cursor1=db.cursor()
                query='INSERT INTO cart (productid,buyerid) VALUES(%s,%s)'
                values=(req['productid'],user_data[0])
                cursor1.execute(query,values)
                db.commit()
                cursor1.close()
            except Exception as e:
                print("excetption ",e)
                return jsonify({'status_code':404,'message':'error occured'})
            return jsonify({'status_code':200,'message':'success'})

        else:
            return jsonify({'status_code':300})
    else:
        print("no request recieved")
        return jsonify({'status_code':500,'message':'error'})

@buyer_page.route("/wishlist/remove",methods=["POST"])
def deletewishlist():
    req =request.get_json()
    user_data= session.get('login')

    if req:    
        print(req['productid'])        
        print(user_data[0])

        cursor2=db.cursor()
        cursor2.execute('DELETE  FROM wishlist WHERE productid = "{0}" AND  buyerid="{1}"'.format(req['productid'],user_data[0]))
        cursor2.close()
        return jsonify({'status_code':200,'message':'success'})
    else:
        return jsonify({'status_code':400,'message':'success'})
                
@buyer_page.route("/checkout")
def checkout():
    user_data=session.get('login')
    data,imgdata=getdata('buyer',user_data[4])
    return render_template("checkout.html",user_data=user_data,imgdata=imgdata)

    
@buyer_page.route("/cart/checkout",methods=["POST"])
def addcheckdata():
    user_data=session.get('login')
    req=request.get_json()
    print(req)
    a=json.dumps(req)
    if req:
        js1=showprod('cart')
        session['checkoutobj']=a
        return ({'js':js1,'object':a,'status_code':200})

    else:
        return ({'js':"error",'object':'errorreq','status_code':404})
        
@buyer_page.route("/checkout/123",methods=['POST'])
def checkoutGpdata():
    js1=showprod('cart')
    cobj=session.get('checkoutobj')
    if js1 and cobj:
        return ({'js':js1,'object':cobj,'status_code':200})
    else:
        return ({'js':js1,'object':'no object present','status_code':404})

    
@buyer_page.route("/checkout/buy",methods=['POST'])
def placeorder():
    req =request.get_json()
    user_data= session.get('login')
    if req:
        print('user id ',user_data[0])
        print(req)
        totamt=req['totamt']
        proddetailarr=req['proddetailarr']
        prodqtarr=req['prodqtarr']
        prodidarr=req['prodidarr']
        ordertime=req['ordertime']
        shipaddr=req['shipaddr']
        paymethod=req['paymethod']
        prodpricearr=req['prodpricearr']
        cursor=db.cursor()#check product already in cart
        cursor.execute('SELECT COUNT(*) FROM cart WHERE productid = "{0}" AND  buyerid="{1}"'.format(prodidarr[0],user_data[0]))
        count=cursor.fetchone()[0]
        cursor.close()
        print(count)
        if count==0:#if it is not already present in cart 
            try:
                cursor2=db.cursor()
                query='INSERT INTO demoorders (buyerid,productid,shipping_addr,proddetail,totamt,paymethod,orderstatus,orderdate) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)'
                values=(user_data[0],prodidarr[0],shipaddr,proddetailarr[0],totamt,paymethod,'yet to be delivered',ordertime)
                cursor2.execute(query,values)
                db.commit()
                cursor2.close()
            except Exception as e:
                print("excetption ",e)
                return jsonify({'status_code':404,'message':'error occured'})
            return jsonify({'status_code':200,'message':'success'})

        else:
            try:
                for i in range(len(prodidarr)):
                    cursor1=db.cursor()
                    query='INSERT INTO demoorders (buyerid,productid,shipping_addr,proddetail,totamt,paymethod,orderstatus,orderdate) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)'
                    values=(user_data[0],prodidarr[i],shipaddr,proddetailarr[i],prodpricearr[i],paymethod,'yet to be delivered',ordertime)
                    cursor1.execute(query,values)
                    db.commit()
                    cursor1.close()
                for i in range(len(prodidarr)):
                    cursor2=db.cursor()
                    cursor2.execute('DELETE  FROM cart WHERE productid = "{0}" AND  buyerid="{1}"'.format(prodidarr[i],user_data[0]))
                    cursor2.close()

                prods=len(prodidarr)
                return jsonify({'status_code':200,'message':'success'})
            except Exception as e:
                print('Exception occured',e)        
                return jsonify({'status_code':300})

    else:
        print("no request recieved")
        return jsonify({'status_code':500,'message':'error'})

    
@buyer_page.route("/prod/buy",methods=['POST'])
def buyprod():
    user_data=session.get('login')
    req=request.get_json()
    print(req['productid'])
    return jsonify({'status_code':200,'message':'success'})

@buyer_page.route("/userprofile/edit",methods=['POST'])
def editprof():
    user_data=session.get('login')
    data,imgdata=getdata('buyer',user_data[4])
    req=request.get_json()
    if(req):
        query=''
        values=()
        cursor=db.cursor()
        if req['pwd']=='':
            query="UPDATE demouser2 SET firstname = %s,lastname = %s,phone = %s,address = %s,profile = %s   WHERE email= %s"
            values=(req['fname'],req['lname'],req['phone'],req['addr'],req['pimgarr'],user_data[4])
        else:
            query="UPDATE demouser2 SET firstname = %s,lastname = %s,phone = %s,address = %s,password = %s,profile = %s   WHERE email= %s"
            values=(req['fname'],req['lname'],req['phone'],req['addr'],req['pwd'],req['pimgarr'],user_data[4])
        
        cursor.execute(query,values)
        db.commit()
        cursor.close()   
        session['login'],imgstr=getdata('buyer',user_data[4])
        user_data=session.get('login')
        return jsonify({'status_code': 200, 'imgdata': 'hi'})

    else:
        print('problem iruku')
        return jsonify({'status_code': 500, 'imgdata':''})


@buyer_page.route("/userprofile")
def profile():
    user_data=session.get('login')
    data,imgdata=getdata('buyer',user_data[4])
    return render_template("userprofile.html",user_data=user_data,imgdata=imgdata)

#buyer-product
@buyer_page.route("/product/<product_id>")
def product(product_id):
    user_data=session.get('login')
    data,imgdata=getdata('buyer',user_data[4])
    cursor =db.cursor()
    cursor.execute('SELECT * FROM products WHERE productid = {0}'.format(product_id))
    count=cursor.fetchall()
    cursor.close()
    
    dictarr=[]
    countlist=[]
    keys=['productid','prodname','prodprice','proddesc','qtyavail','qtysold','prodimg1','prodimg2','prodimg3','netamt','sellerid','category']
    for i in  range(len(count)):#6,7,8
        countlist.append(list(count[i]))

    for i in range(len(countlist)):            
        countlist[i][6]=removeblob(countlist[i][6])
        countlist[i][7]=removeblob(countlist[i][7])
        countlist[i][8]=removeblob(countlist[i][8])
        dictarr.append(dict(zip(keys,countlist[i])))
    js=json.dumps('hi im hacky')
    js1=json.dumps(dictarr)
    dictarr1=dictarr[0]
    return render_template("product.html",user_data=user_data,imgdata=imgdata,proddata=dictarr1)
