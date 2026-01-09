from django.shortcuts import render ,redirect
from django.http import HttpResponse , JsonResponse
from .models import admin_table,payment_table,katha_table
import bcrypt
from .serializers import admin_serializer , payment_serializer ,katha_serializer
from django.db.models import Q
import jwt
from project.settings import SECRET_KEY
from datetime import date


# Create your views here.
def home(req):
    if req.method == "POST" :
        name = req.POST.get("name")
        password = req.POST.get("password").encode("utf-8")
        user = admin_table.objects.get(user_name = name)
        if bcrypt.checkpw(password,user.password.encode("utf-8")):
            print("login succesfull")
            responce = redirect('main')
            pay_load = {
                "login" : True,
                "role" : "admin"

            }
            token = jwt.encode(pay_load,SECRET_KEY,algorithm = "HS256")
            responce.set_cookie(
                key = "jwt",
                value=token
            )
            print(token)
            return responce

        else:
            print("failed")
            return render(req,"home.html")
        print(hash)
    # hash = password.
    return render(req,"home.html")

def createaccount(req):
        
        token = req.COOKIES.get('jwt')
        if not token:
            return render(req,"home.html")


        df = admin_serializer(data=req.POST)
        if df.is_valid():
            password = df.validated_data["password"].encode("utf-8")
            salt = bcrypt.gensalt(rounds=12)
            hash = bcrypt.hashpw(password,salt)
            df.validated_data["password"]=hash.decode("utf-8")
            df.save()
            return render(req,"home.html")
        return render(req,"create.html")
def main(req):
    token = req.COOKIES.get('jwt')
    if not token:
        return render(req,"home.html")
    # print(token)
    # data = jwt.decode(token,SECRET_KEY,algorithms= ["HS256"])
    # print(data)


    data=payment_table.objects.all()
    data = payment_serializer(data ,many= True).data
    ac=[]
    today=date.today().isoformat()
    print(today)
    for i in data:
        if i['purchase_date']== today:
            ac.append(i)
    # print(ac)

    return render(req,"main.html",{"data":ac})
    

def makepayment(req):
    data = req.POST
    print(data)
    sf = payment_serializer(data =data)
    if sf.is_valid():
        print("valid")
        sf.save()
        return render(req,"payment.html")


    return render(req,"payment.html")

def search(request):
    token = request.COOKIES.get('jwt')
    if not token:
        return render(request,"home.html")
    query = request.GET.get("query")

    data = payment_table.objects.none()

    if query:
        data = payment_table.objects.filter(
            Q(id__icontains=query) |
            Q(user_name__icontains=query) |
            Q(phone_number__icontains=query)
        )

    serializer = payment_serializer(data, many=True)

    return render(request, "search.html", {
        "data": serializer.data
    })
def createkatha(req):
    token = req.COOKIES.get('jwt')
    if not token:
        return render(req,"home.html")
    data = req.POST
    df = katha_serializer(data = data)
    if df.is_valid():
        password = df.validated_data["password"].encode("utf-8")
        salt = bcrypt.gensalt(rounds=12)
        hash = bcrypt.hashpw(password,salt)
        df.validated_data["password"]=hash.decode("utf-8")
        df.save()
        return render(req,"main.html")
    return render(req,"katha.html")

def all_data(req):
    token = req.COOKIES.get('jwt')
    if not token:
        return render(req,"home.html")
    data=payment_table.objects.all()
    data = payment_serializer(data ,many= True).data
    # print(data)
    return render(req,"all.html",{"data":data})
def logout(req):
    token = req.COOKIES.get('jwt')
    if not token:
        return render(req,"home.html")
    response = render(req, "home.html")  
    response.delete_cookie("jwt")  
    return response

def viewkathas(req):
    token = req.COOKIES.get('jwt')
    if not token:
        return render(req,"home.html")
    data = katha_table.objects.all()
    df = katha_serializer(data , many=True).data
    return render(req,"kathas.html",{"data" : df})
from django.db.models import Sum

def personpayments(req, id):
    token = req.COOKIES.get('jwt')
    if not token:
        return render(req, "home.html")


    katha = katha_table.objects.get(id=id)
    phone_number = katha.phone_number


    month = req.GET.get('month')
    year = req.GET.get('year')


    payments = payment_table.objects.filter(phone_number=phone_number)


    if month:
        payments = payments.filter(purchase_date__month=int(month))

    if year:
        payments = payments.filter(purchase_date__year=int(year))

    total_amount = payments.aggregate(
        total=Sum('amount')
    )['total'] or 0

    return render(
        req,
        "member.html",
        {
            "data": payments,
            "total_amount": total_amount,
            "month": month,
            "year": year,
            "user": katha
        }
    )



def user(req):
    print(req.method)
    if  req.method == "POST":
        id = req.POST.get("name")
        password = req.POST.get("password").encode('utf-8')
        print(id,password)
        try:
            data = katha_table.objects.get(id=id)
            print(data)
            print(data.password.encode('utf-8'))
        except Exception as e:
            print(e)

        if bcrypt.checkpw(password,data.password.encode('utf-8')):

            print("login successfull")
            pay_load = {
                "login" : True,
                "role" : "user",
                "id" :data.id

            }
            token = jwt.encode(pay_load,SECRET_KEY,algorithm = "HS256")
            responce=redirect("usermain")
            responce.set_cookie(
                key = "jwt",
                value=token
            )

            
            print(token)
            return responce
        else:
            print("login failed")
            return render(req,'user.html')



    return render(req,'user.html')
def usermain(req):
    token = req.COOKIES.get('jwt')
    if not token:
        return render(req,'user.html')
    data =jwt.decode(token,SECRET_KEY,algorithms= ["HS256"])
    id=data['id']
    data = katha_table.objects.filter(id=id).first()
    # data=katha_serializer(id=id).data
    phone_number=data.phone_number
    data = payment_table.objects.filter(phone_number=phone_number)

    return render(req,"usermain.html",{"data":data})
    # return HttpResponse("request....")
def userlogout(req):
    token = req.COOKIES.get('jwt')
    if not token:
        return render(req,"user.html")
    response = render(req, "user.html")  
    response.delete_cookie("jwt") 
    print('from user') 
    return response

def land(req):
    return render(req,"landing.html")