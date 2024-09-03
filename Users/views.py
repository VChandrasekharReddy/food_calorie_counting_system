from django.shortcuts import render
import pymysql
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import linear_model
import os
import datetime

# Create your views here.
def index(request):
  return render(request,'Users/index.html')
def userlogin(request):
  return render(request,'Users/Users.html')
def register(request):
  return render(request,'Users/Register.html')
def userhome(request):
  return render(request,'Users/UserHome.html')
def RegAction(request):
  name=request.POST['name']
  email=request.POST['email']
  mobile=request.POST['mobile']
  address=request.POST['address']
  username=request.POST['username']
  password=request.POST['password']

  con=pymysql.connect(host="localhost",user="root",password="",database="food_calories")
  cur=con.cursor()
  i=cur.execute("insert into user values(null,'"+name+"','"+email+"','"+mobile+"','"+address+"','"+username+"','"+password+"')")
  con.commit()
  con.close()
  cur.close()
  if i>0:
    context={'data':'Registration Successful...!!'}
    return render(request,'Users/Register.html',context)
  else:
    context={'data','Registration Failed...!!'}
    return render(request,'Users/Register.html',context)
def LogAction(request):
  username=request.POST.get('username')
  password=request.POST.get('password')
  con=pymysql.connect(host="localhost",user="root",password="",database="food_calories")
  cur=con.cursor()
  cur.execute("select *  from user where username='"+username+"'and password='"+password+"'")
  data=cur.fetchone()
  if data is not None:
    request.session['user']=username
    request.session['userid']=data[0]
    return render(request,'Users/UserHome.html')
  else:
    context={'data':'Login Failed ....!!'}
    return render(request,'Users/Users.html',context)

def CaloryLimit(request):
  return render(request,'Users/EnterDetails.html');
def CaloryLimitSetAction(request):
  patient=request.POST['patient']
  print(patient)
  if patient=="Sugar":
    return render(request,'Users/EnterDetails2.html');
  else:
    return render(request,'Users/EnterDetails1.html');
def SugarAction(request):
  sugar=request.POST['sugar']

  s=int(sugar)
  if s>100 and s<125:
    context={'data':1500}
    return render(request,'Users/Limit.html',context)
  elif s>125 and s<140:
    context={'data':1700}
    return render(request,'Users/Limit.html',context)
  elif s>140 and s<190:
    context={'data':1900}
    return render(request,'Users/Limit.html',context)
  else:
    context={'data':2000}
    return render(request,'Users/Limit.html',context)




  
global data
global X
global y
global X_train,X_test,y_train,y_test
global model
def CaloryLimitAction(request):
  global data
  global X
  global y
  global X_train,X_test,y_train,y_test
  global model
  age=request.POST['age']
  height=request.POST['height']
  weight=request.POST['weight']
  a=int(age)
  h=int(height)
  w=int(weight)
  BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
  data=pd.read_csv(BASE_DIR+"\\dataset\\CalorieLimit.csv")
  X=data[['age','height','weight']]
  y=data[['limit']]
  X_train,X_test,y_train,y_test=train_test_split(X,y, test_size=0.2)
  model=linear_model.LinearRegression()
  model.fit(X_train,y_train)
  pred=model.predict([[a,h,w]])
  r=int(pred)
  context={'data':r}
  return render(request,'Users/Limit.html',context)
  
def ConfirmCalory(request):
    calory=request.POST['calory']
    print(calory)
    con=pymysql.connect(host="localhost",user="root",password="",database="food_calories")
    
    uid=str(request.session['userid'])
    tday=datetime.date.today()
    tt=str(tday);
    cur=con.cursor()
    cur.execute("select * from calory where date='"+tt+"' and user_id='"+uid+"'")
    dd=cur.fetchone()
    if dd is not None:
      context={'data':'Calory Limit Already Set For This Day...!!'}
      return render(request,'Users/Confirmed.html',context)
    else:
      cur1=con.cursor()
      i=cur1.execute("insert into calory values(null,'"+uid+"','"+calory+"','"+tt+"')")
      con.commit()
      if i>0:
        context={'data':'Calory Limit Confirmed...!!'}
        return render(request,'Users/Confirmed.html',context)
      else:
        context={'data':'Failed To Confirm Limit...!!'}
        return render(request,'Users/Confirmed.html',context)
      

def AddItems(request):
  con=pymysql.connect(host="localhost",user="root",password="",database="food_calories")
  cur=con.cursor()
  cur.execute("select *  from food_calories")
  data=cur.fetchall()
  strdata="<table></tr><th>Select Food Item:</th><td><select name='name' style='wight:300px;border-radius:10px;height:50px;'>"
  for i in data:
    strdata+="<option value='"+str(i[1])+"'>"+str(i[1])+"</option>"
  strdata+="</select></td></tr><tr><th>No.of Items</th><td><input type='number' name='noof' required   style='wight:300px;border-radius:10px;height:50px;'></td></tr><tr><th></th><td><input type='submit' value='Add Item'style='wight:150px;border-radius:10px;height:50px;'> <input type='reset' value='Reset'style='wight:150px;border-radius:10px;height:50px;'></td></tr></table>"
  context={'data':strdata}
  return render(request,'Users/AddItems.html',context)

def AddItemAction(request):
  name=request.POST['name']
  noof=request.POST['noof']
  uid=str(request.session['userid'])
  con=pymysql.connect(host="localhost",user="root",password="",database="food_calories")
  cur1=con.cursor()
  c=0
  cur1.execute("select * from food_calories where item_name='"+name+"'")
  d=cur1.fetchone()
  if d is not None:
    c=int(d[2])

  n=int(noof)
  t=n*c;
  tt=str(t)
  cur=con.cursor()
  i=cur.execute("insert into items values(null,'"+uid+"','"+name+"','"+noof+"','"+tt+"')")
  con.commit()
  con.close()
  cur.close()
  if i>0:
    context={'data':'Item Added Successfully...!!'}
    return render(request,'Users/AddItems.html',context)
  else:
    context={'data','Item Adding Failed...!!'}
    return render(request,'Users/AddItems.html',context)

  
def ViewItems(request):
  uid=str(request.session['userid'])
  con=pymysql.connect(host="localhost",user="root",password="",database="food_calories")
  cur=con.cursor()
  cur.execute("select * from items where user_id='"+uid+"'")
  data=cur.fetchall()
  strdata="<table><tr><th>Item Name</th><th>No.of Items</th><th>Gain Calories</th><th>Delete</th></tr>"
  for i in data:
    strdata+="<tr><td>"+str(i[2])+"</td><td>"+str(i[3])+"</td><td>"+str(i[4])+"</td><td><a href='DeleteItem?id="+str(i[0])+"'>Click</a></td></tr>"
  context={'data':strdata}
  return render(request,'Users/ViewItems.html',context)
def DeleteItem(request):
  uid=str(request.session['userid'])
  iid=request.GET['id']
  con=pymysql.connect(host="localhost",user="root",password="",database="food_calories")
  cur1=con.cursor()
  cur1.execute("delete from items where id='"+iid+"'")
  con.commit()
  cur=con.cursor()
  cur.execute("select * from items where user_id='"+uid+"'")
  data=cur.fetchall()
  strdata="<table><tr><th>Item Name</th><th>No.of Items</th><th>Gain Calories</th><th>Delete</th></tr>"
  for i in data:
    strdata+="<tr><td>"+str(i[2])+"</td><td>"+str(i[3])+"</td><td>"+str(i[4])+"</td><td><a href='DeleteItem?id="+str(i[0])+"'>Click</a></td></tr>"
  context={'data':strdata}
  return render(request,'Users/ViewItems.html',context)



  
def AddExercise(request):
  return render(request,'Users/AddExercise.html')

def AddExerciseAction(request):
  name=request.POST['name']
  extime=request.POST['extime']
  calories=request.POST['calories']
  uid=str(request.session['userid'])
  con=pymysql.connect(host="localhost",user="root",password="",database="food_calories")
  cur=con.cursor()
  i=cur.execute("insert into exercise values(null,'"+uid+"','"+name+"','"+extime+"','"+calories+"')")
  con.commit()
  con.close()
  cur.close()
  if i>0:
    context={'data':'Exercise Added Successfully...!!'}
    return render(request,'Users/AddExercise.html',context)
  else:
    context={'data','Exercise Adding Failed...!!'}
    return render(request,'Users/AddExercise.html',context)
def ViewExercise(request):
  uid=str(request.session['userid'])
  con=pymysql.connect(host="localhost",user="root",password="",database="food_calories")
  cur=con.cursor()
  cur.execute("select * from exercise where user_id='"+uid+"'")
  data=cur.fetchall()
  strdata="<table><tr><th>Exercise Name</th><th>Time(Minutes)</th><th>Burned Calories</th><th>Delete</th></tr>"
  for i in data:
    strdata+="<tr><td>"+str(i[2])+"</td><td>"+str(i[3])+"</td><td>"+str(i[4])+"</td><td><a href='DeleteExercise?id="+str(i[0])+"'>Click</a></td></tr>"
  context={'data':strdata}
  return render(request,'Users/ViewExercise.html',context)
def DeleteExercise(request):
  uid=str(request.session['userid'])
  iid=request.GET['id']
  con=pymysql.connect(host="localhost",user="root",password="",database="food_calories")
  cur1=con.cursor()
  cur1.execute("delete from exercise where id='"+iid+"'")
  con.commit()
  cur=con.cursor()
  cur.execute("select * from exercise where user_id='"+uid+"'")
  data=cur.fetchall()
  strdata="<table><tr><th>Exercise Name</th><th>Time(Minutes)</th><th>Burned Calories</th><th>Delete</th></tr>"
  for i in data:
    strdata+="<tr><td>"+str(i[2])+"</td><td>"+str(i[3])+"</td><td>"+str(i[4])+"</td><td><a href='DeleteExercise?id="+str(i[0])+"'>Click</a></td></tr>"
  context={'data':strdata}
  return render(request,'Users/ViewExercise.html',context)
  
  
def ViewResult(request):
  uid=str(request.session['userid'])
  con=pymysql.connect(host="localhost",user="root",password="",database="food_calories")
  cur=con.cursor()
  cur.execute("select * from items where user_id='"+uid+"'")
  data=cur.fetchall()
  #food items calories(fcalory)
  fcalory=0
  for i in data:
    fcalory=fcalory+int(i[4])
  request.session['gain']=fcalory
  curr=con.cursor()
  curr.execute("select * from exercise where user_id='"+uid+"'")
  data2=curr.fetchall()
  #burned calories(excalory)
  excalory=0
  for ii in data2:
    excalory=excalory+int(ii[4])
  request.session['burned']=excalory
  #remaining=food items-burned(remaining)
  remaining=fcalory-excalory
  
  request.session['remains']=remaining
  
  currr=con.cursor()
  currr.execute("select * from calory where user_id='"+uid+"'")
  data3=currr.fetchall()
  #total limit
  limit=0
  for da in data3:
    limit=int(da[2])
  request.session['limit']=limit
  #final=limit-remaining(limit_total)
  limit_total=limit-remaining
  request.session['fflimit']=limit_total
  if limit>remaining and remaining>0:
    return render(request,'Users/ViewResults.html')
  if limit>remaining and remaining<0:
    return render(request,'Users/NegativeResults.html')
  if remaining>limit:
    return render(request,'Users/NExerciseResults.html')
    
    
