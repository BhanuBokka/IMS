import sqlite3
from flask import Flask, jsonify, render_template, request
conn=sqlite3.connect('myims.db')
app=Flask(__name__)

def idgenerator(tab):
    conn=sqlite3.connect('myims.db')
    cn= conn.cursor()
    idval = ''
    print(tab)
    if tab=='CUSTOMER':
        idval = 'CUST_ID'
    if tab=='PRODUCT':
        idval = 'PRODUCT_ID'
    if tab=='ORDERS':
        idval = 'ORDER_ID'
    if tab=='SUPPLIER':
        idval = 'SUPPLIER_ID'
    print(tab,idval)
    cn.execute(f"SELECT {idval} FROM {tab}")
    new = cn.fetchall()
    cud = str(new[len(new)-1][0])
    for i in range(len(str(cud))):
        if cud[i].isnumeric():
            f = i
            break
    myint = cud[f:]
    myint = int(myint)+1
    return idval[0:3]+str(myint)

@app.route('/')
def home():
    return render_template('index.html')
@app.route('/show-customers')
def customer_show():
    conn=sqlite3.connect('myims.db')
    cn=conn.cursor()
    cn.execute('select * from customer')
    data=[]
    for i in cn.fetchall():
        customer={}
        customer['cust_id']=i[0]
        customer['cust_name']=i[1]
        customer['cust_addr']=i[2]
        customer['cust_email']=i[3]
        data.append(customer)
    print(data)
    return render_template('showcustomers.html',data=data)
@app.route('/show-suppliers')
def supplier_show():
    conn=sqlite3.connect('myims.db')
    cn=conn.cursor()
    cn.execute('select * from supplier')
    data=[]
    for i in cn.fetchall():
        supplier={}
        supplier['supplier_id']=i[0]
        supplier['supplier_name']=i[1]
        supplier['supplier_addr']=i[2]
        supplier['supplier_mail']=i[3]
        data.append(supplier)
    return render_template('showsuppliers.html',data=data)
@app.route('/show-products')
def product_show():
    conn=sqlite3.connect('myims.db')
    cn=conn.cursor()
    cn.execute('select * from product')
    data=[]
    for i in cn.fetchall():
        product={}
        product['product_id']=i[0]
        product['product_name']=i[1]
        product['product_price']=i[2]
        product['stock']=i[3]
        product['supplier_id']=i[4]
        data.append(product)
    return render_template('showproducts.html',data=data)

@app.route('/show-orders')
def orders_show():
    conn=sqlite3.connect('myims.db')
    cn=conn.cursor()
    cn.execute('select * from orders')
    data=[]
    for i in cn.fetchall():
        orders={}
        orders['orders_id']=i[0]
        orders['product_id']=i[1]
        orders['customer_id']=i[2]
        orders['quantity']=i[3]
        data.append(orders)
    return render_template('showorders.html',data=data)
@app.route('/add-customers', methods = ['GET','POST'])
def add_customer():
    if request.method == 'POST':
        conn=sqlite3.connect('myims.db')
        cn=conn.cursor()
        #customer_id= request.form.get('customer_id')
        customer_name= request.form.get('customer_name')
        customer_address= request.form.get('customer_addr')
        customer_mail= request.form.get('customer_mail')
        ID = idgenerator('CUSTOMER')
        cn.execute(f"insert into customer(cust_id,cust_name,cust_addr,cust_mail) values('{ID}','{customer_name}','{customer_address}','{customer_mail}')")
        conn.commit()
        print('Data has been inserted successfully!')
        return jsonify({'message':'successful'})
    else:
        return render_template('addcustomers.html')
@app.route('/add-suppliers', methods= ['GET','POST'])
def add_supplier():
    print(request.method)
    if request.method == 'POST':
        conn=sqlite3.connect('myims.db')
        cn=conn.cursor()
        supplier_name= request.form.get('supplier_name')
        supplier_address= request.form.get('supplier_addre')
        supplier_mail= request.form.get('supplier_mail')
        ID = idgenerator('SUPPLIER')
        cn.execute(f"insert into supplier(supplier_id,supplier_name,supplier_addr,supplier_mail) values('{ID}','{supplier_name}','{supplier_address}','{supplier_mail}')")
        conn.commit()
        print('Data has been inserted successfully!')
        return jsonify({'message':'successful'})
    else:
        return render_template('addsuppliers.html')
@app.route('/add-products',methods=['GET','POST'])
def add_product():
    if request.method == 'POST':
        conn=sqlite3.connect('myims.db')
        cn=conn.cursor()
        product_name= request.form.get('product_name')
        product_price= request.form.get('product_price')
        product_stock= request.form.get('product_stock')
        product_supplier_id=request.form.get('product_supplier_id')
        ID = idgenerator('PRODUCT')
        print(ID)
        cn.execute(f"insert into product(product_id,product_name,product_price,stock,supplier_id) values('{ID}','{product_name}','{product_price}','{product_stock}','{product_supplier_id}')")
        conn.commit()
        print('Data has been inserted successfully!')
        return jsonify({'message':'successful'})
    else:
        return render_template('addproducts.html')
@app.route('/add-orders',methods=['GET','POST'])
def add_orders():
    if request.method=='POST':
        conn=sqlite3.connect('myims.db')
        cn=conn.cursor()
        product_id=request.form.get('product_id')
        customer_id=request.form.get('customer_id')
        quantity=request.form.get('quantity')
        ID = idgenerator('ORDERS')
        cn.execute(f"insert into orders(order_id,product_id,customer_id,quantity) values('{ID}','{product_id}','{customer_id}','{quantity}')")
        conn.commit()
        print('Data has been inserted successfully')
        return jsonify({'message':'successful'})
    else:
        return render_template('addorders.html')

@app.route('/update-customers',methods= ['GET','POST'])
def update_customers():
    if request.method== 'POST':
        conn=sqlite3.connect('myims.db')
        cn=conn.cursor()
        customer_id= request.form.get('customer_id')
        change= request.form.get('change')
        newvalue= request.form.get('newvalue')
        print(customer_id,change,newvalue)
        cn.execute(f"update customer set {change}='{newvalue}' where cust_id='{customer_id}'")
        conn.commit()
        print('data has been updated successfully!')
        return jsonify({'message':'successful'})
    else:
        return render_template('updatecustomer.html')

@app.route('/update-suppliers',methods=['GET','POST'])
def update_suppliers():
    if request.method== 'POST':
        conn=sqlite3.connect('myims.db')
        cn=conn.cursor()
        supplier_id=request.form.get('supplier_id')
        change=request.form.get('change')
        newvalue=request.form.get('newvalue')
        cn.execute(f"update supplier set {change}='{newvalue}' where supplier_id='{supplier_id}'")
        conn.commit()
        print('data has been updated successfully')
        return jsonify({'message':'successful'})
    else:
        return render_template('updatesupplier.html')
    
@app.route('/update-products',methods=['GET','POST'])
def update_products():
    if request.method== 'POST':
        conn=sqlite3.connect('myims.db')
        cn=conn.cursor()
        product_id=request.form.get('product_id')
        change=request.form.get('change')
        newvalue=request.form.get('newvalue')
        cn.execute(f"update product set {change}='{newvalue}' where product_id = '{product_id}'")
        conn.commit()
        print('data has been updated successfully')
        return jsonify({'message':'successful'})
    else:
        return render_template('updateproduct.html')

@app.route('/update-orders',methods= ['GET','POST'])
def update_orders():
    if request.method== 'POST':
        conn=sqlite3.connect('myims.db')
        cn=conn.cursor()
        orders_id= request.form.get('order_id')
        change= request.form.get('change')
        newvalue= request.form.get('newvalue')
        cn.execute(f"update orders set {change}='{newvalue}' where order_id='{orders_id}'")
        conn.commit()
        print('data has been updated successfully!')
        return jsonify({'message':'successful'})
    else:
        return render_template('updateorders.html')
    
@app.route('/delete-customers',methods=['GET','POST'])
def delete_customers():
    if request.method== 'POST':
        conn=sqlite3.connect('myims.db')
        cn=conn.cursor()
        cust_id=request.form.get('cust_id')
        print(cust_id)
        cn.execute(f"delete from customer where cust_id='{cust_id}'")
        conn.commit()
        print('Data has been deleted successfully ')
        return jsonify({'message':'successful'})
    else:
        return render_template('deletecustomers.html')

@app.route('/delete-products',methods=['GET','POST'])   
def delete_products():
    if request.method=='POST':
        conn=sqlite3.connect('myims.db')
        cn=conn.cursor()
        product_id=request.form.get('product_id')
        cn.execute(f"delete from product where product_id='{product_id}' ")
        conn.commit()
        print('Data has been deleted successfully ')
        return jsonify({'message':'successful'})
    else:
        return render_template('deleteproducts.html')
    
@app.route('/delete-suppliers', methods=['GET', 'POST'])
def delete_suppliers():
    if request.method=='POST':
        conn=sqlite3.connect('myims.db')
        cn=conn.cursor()
        supplier_id=request.form.get('supplier_id')
        cn.execute(f"delete from supplier where supplier_id='{supplier_id}'")
        conn.commit()
        print('Data has been deleted successfully')
        return jsonify({'message':'successful'})
    else:
        return render_template('deletesuppliers.html')
    
@app.route('/delete-orders',methods=['GET','POST'])
def delete_orders():
    if request.method== 'POST':
        conn=sqlite3.connect('myims.db')
        cn=conn.cursor()
        order_id=request.form.get('order_id')
        cn.execute(f"delete from orders where order_id='{order_id}'")
        conn.commit()
        print('Data has been deleted successfully')
        return jsonify({'message':'successful'})
    else:
        return render_template('deleteorders.html')
    

if __name__=='__main__':
    # app.run()
    app.run(host='0.0.0.0',port=5000,debug=True) #for deploying the project by creating the port number