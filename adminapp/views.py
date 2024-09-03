from django.shortcuts import render
import pymysql
# Create your views here
def adminlogin(request):
    return render(request,'adminapp/Login.html')
def adminhome(request):
    return render(request,'adminapp/AdminHome.html')
def LogAction(request):
    username=request.POST.get('username')
    password=request.POST.get('password')
    con=pymysql.connect(host="localhost",user="root",password="",database="food_calories")
    cur=con.cursor()
    cur.execute("select *  from admin where username='"+username+"'and password='"+password+"'")
    data=cur.fetchone()
    if data is not None:      
        return render(request,'adminapp/AdminHome.html')
    else:
        context={'data':'Login Failed ....!!'}
        return render(request,'adminapp/Login.html',context)
def AddFoodCalories(request):
    return render(request,'adminapp/AddFoodCalories.html')
def AddFoodCaloriesAction(request):
    name=request.POST['name']
    calories=request.POST['calories']
    carbs=request.POST['carbs']
    facts=request.POST['facts']
    protein=request.POST['protein']

    con=pymysql.connect(host="localhost",user="root",password="",database="food_calories")
    cur=con.cursor()
    cur.execute("select * from food_calories where item_name='"+name+"'")
    dd=cur.fetchone()
    if dd is not None:
      context={'data':'Food Item Already Exist...!!'}
      return render(request,'adminapp/AddFoodCalories.html',context)
    else:
      cur1=con.cursor()
      i=cur1.execute("insert into food_calories values(null,'"+name+"','"+calories+"','"+carbs+"','"+facts+"','"+protein+"')")
      con.commit()
      if i>0:
        context={'data':'Food Item Added Successfully...!!'}
        return render(request,'adminapp/AddFoodCalories.html',context)
      else:
        context={'data':'Failed To Add Food Item...!!'}
        return render(request,'adminapp/AddFoodCalories.html',context)
def ViewFoodCalories(request):
    con=pymysql.connect(host="localhost",user="root",password="",database="food_calories")
    cur=con.cursor()
    cur.execute("select * from food_calories")
    data=cur.fetchall()
    strdata="<table border='1'><tr style='color:red;background:skyblue;height:60px;text-align:center;'><th>Food Item Name</th><th>Calories</th><th>Carbohydrates</th><th>Facts</th><th>Proteins</th></tr>"
    for i in data:
     strdata+="<tr><td>"+str(i[1])+"</td><td>"+str(i[2])+"</td><td>"+str(i[3])+"</td><td>"+str(i[4])+"</td><td>"+str(i[5])+"</td></tr>"
    context={'data':strdata}
    return render(request,'adminapp/ViewFoodCalories.html',context)







