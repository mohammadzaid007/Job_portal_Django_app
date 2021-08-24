from django.shortcuts import render,HttpResponseRedirect,redirect
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import authenticate,login,logout
from datetime import date

# Create your views here.
def index(request):
    return render(request,'index.html')

def contact(request):
    return render(request,'Contact.html')

def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        try:
            if user.is_staff:
                login(request,user)
                obj1 = StudentUser.objects.get(user=user)
                usertype = obj1.type
                request.session['type'] = usertype
                request.session['username'] = username
                if usertype == 'admin':
                    return render(request, 'Admin_home.html')

            else:
                return render(request, 'Admin_login.html', {'data': "*Invalid Email Or Password."})
        except:
            return render(request, 'Admin_login.html', {'data': "*Invalid Email Or Password."})

    else:
        return render(request, 'Admin_login.html')


def admin_home(request):
   if not request.user.is_authenticated:
       return redirect('admin_login')
   user = request.user
   student = StudentUser.objects.get(user=user)
   d = {'student': student}
   return render(request,'admin_home.html',d)


def admin_logout(request):
    logout(request)
    return redirect('index')


def change_password_admin(request):
    if  not request.user.is_authenticated:
        return redirect('admin_login')
    error=""

    if request.method=="POST":
        c=request.POST['pwd']
        n=request.POST['newpwd']

        try:
            u=User.objects.get(id=request.user.id)
            if u.check_password(c):
                u.set_password(n)
                u.save()
                error="no"

            else:
                error="no"
        except:
            error="yes"
    d={'error':error}
    return render(request,'change_password_admin.html',d)




def user_login(request):
    if request.method=='POST':
        username=request.POST['email']
        password=request.POST['password']

        obj=authenticate(username=username,password=password)
        try:
            if obj:
                obj1=StudentUser.objects.get(user=obj)
                login(request, obj)
                usertype=obj1.type
                request.session['type']=usertype
                request.session['email']=username
                if  usertype=='student':
                    return render(request, 'User_home.html')


            else:
                return render(request, 'User_login.html', {'data': "*Invalid Email Or Password."})
        except:
            return render(request, 'User_login.html', {'data': "*Invalid Email Or Password."})

    else:
        return render(request,'User_login.html')


def user_signup(request):
    if request.method=='GET':
        return render(request,'User_signup.html')
    elif request.method=='POST':
        fname=request.POST['fname']
        lname = request.POST['lname']
        image = request.FILES['image']
        contact=request.POST['contact']
        email = request.POST['email']
        password = request.POST['pwd']
        gender = request.POST['gender']

        obj=User.objects.create_user(first_name=fname,last_name=lname,username=email,password=password)
        obj1=StudentUser.objects.create(user=obj,mobile=contact,image=image,gender=gender,type="student")

        obj.save()
        obj1.save()
        return render(request, 'User_signup.html',{'data':"Signup Successful !!"})

    else:
        return render(request, 'User_signup.html', {'data': "Signup Was Not Successful !!"})



def user_home(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    user = request.user
    student = StudentUser.objects.get(user=user)
    d = {'student': student}
    return render(request, 'User_home.html', d)



def user_logout(request):
    logout(request)
    return redirect('index')



def change_password_user(request):
    if  not request.user.is_authenticated:
        return redirect('user_login')
    error=""

    if request.method=="POST":
        c=request.POST['pwd']
        n=request.POST['newpwd']

        try:
            u=User.objects.get(id=request.user.id)
            if u.check_password(c):
                u.set_password(n)
                u.save()
                error="no"

            else:
                error="no"
        except:
            error="yes"
    d={'error':error}
    return render(request,'change_password_user.html',d)


def view_users(request):
    if  not request.user.is_authenticated:
        return redirect('admin_login')
    data=StudentUser.objects.all()
    d={'data':data}
    return render(request,'View_users.html',d)


def delete_user(request,pid):
    if  not request.user.is_authenticated:
        return redirect('admin_login')
    data=User.objects.get(id=pid)
    data.delete()
    d={'data':data}
    return redirect('view_users')

def recruiter_pending(request):
    if  not request.user.is_authenticated:
        return redirect('admin_login')
    data=Recruiter.objects.filter(status='Pending')
    d={'data':data}
    return render(request,'Recruiter_pending.html',d)



def change_status(request,pid):
    if  not request.user.is_authenticated:
        return redirect('admin_login')
    error=""
    recruiter=Recruiter.objects.get(id=pid)
    if request.method=="POST":
        s=request.POST['status']
        recruiter.status=s
        try:
            recruiter.save()
            error="no"
        except:
            error="yes"
    d={'recruiter':recruiter,'error':error}
    return render(request,'change_status.html',d)

def recruiter_accepted(request):
    if  not request.user.is_authenticated:
        return redirect('admin_login')
    data=Recruiter.objects.filter(status='Accept')
    d={'data':data}
    return render(request,'Recruiter_accepted.html',d)

def recruiter_rejected(request):
    if  not request.user.is_authenticated:
        return redirect('admin_login')
    data=Recruiter.objects.filter(status='Reject')
    d={'data':data}
    return render(request,'Recruiter_rejected.html',d)

def recruiter_all(request):
    if  not request.user.is_authenticated:
        return redirect('admin_login')
    data=Recruiter.objects.all()
    d={'data':data}
    return render(request,'Recruiter_all.html',d)


def add_job(request):
    if  not request.user.is_authenticated:
        return redirect('recruiter_login')
    elif request.method=='POST':
        job_title=request.POST['jobtitle']
        sdate = request.POST['startdate']
        ldate = request.POST['lastdate']
        salary=request.POST['salary']
        logo = request.FILES['logo']
        exp = request.POST['experience']
        location = request.POST['location']
        skills = request.POST['skills']
        descriptions=request.POST['descriptions']

        user=request.user
        recruiter=Recruiter.objects.get(user=user)

        obj=Job.objects.create(recruiter=recruiter,title=job_title,start_date=sdate,end_date=ldate,salary=salary,image=logo,description=descriptions,experience=exp,location=location,skills=skills,job_posting_date=date.today())
        obj.save()
        return render(request, 'Add_job.html',{'data':"Job Posted Successfully !!"})
    else:

        return render(request,'Add_job.html')



def job_list(request):
    if  not request.user.is_authenticated:
        return redirect('recruiter_login')
    user = request.user
    recruiter = Recruiter.objects.get(user=user)
    job = Job.objects.filter(recruiter=recruiter)
    d={'job':job}
    return render(request,'Job_list.html',d)


def edit_job(request,pid):
    if  not request.user.is_authenticated:
        return redirect('recruiter_login')

    error=""
    job = Job.objects.get(id=pid)
    if request.method=='POST':

        job_title=request.POST['jobtitle']
        sdate = request.POST['startdate']
        ldate = request.POST['lastdate']
        salary=request.POST['salary']
        exp = request.POST['experience']
        location = request.POST['location']
        skills = request.POST['skills']
        descriptions=request.POST['descriptions']

        job.title=job_title
        job.start_date=sdate
        job.end_date=ldate
        job.salary=salary
        job.description=descriptions
        job.experience=exp
        job.location=location
        job.skills=skills
        

        try:
            job.save()
            error="no"                                
        except:
            error="yes"  

        if sdate:
            try:
                job.start_date=sdate
                job.save()
            except:
                pass
        else:
            pass

        if ldate:
            try:
                job.end_date=ldate
                job.save()
            except:
                pass
        else:
            pass

    d={'error':error,'job':job}
    return render(request,'Edit_job_details.html',d)
    

    


def recruiter_home(request):
    if  not request.user.is_authenticated:
        return redirect('recruiter_login')
    user=request.user
    recruiter=Recruiter.objects.get(user=user)
    d={'recruiter':recruiter}
    return render(request,'Recruiter_home.html',d)

def autherror(request):
    return render(request,'AuthError.html')

def recruiter_login(request):
    if request.method=='POST':
        username=request.POST['email']
        password=request.POST['password']

        obj=authenticate(username=username,password=password)
        if obj:
            obj1 = Recruiter.objects.get(user=obj)
            usertype = obj1.type
            status = obj1.status
            request.session['type'] = usertype
            request.session['email'] = username
            request.session['status'] = status
            if usertype == 'recruiter' and status == "Pending":
                return render(request, 'Recruiter_login.html',
                              {'data': "Your Login Status Is Pending Wait For ADMIN's Approvel..."})
            else:
                login(request,obj)
                return render(request, 'Recruiter_home.html')
        else:
            return render(request, 'Recruiter_login.html', {'data': "*Invalid Email Or Password."})

    else:
        return render(request,'Recruiter_login.html')



def recruiter_signup(request):
    if request.method=='GET':
        return render(request,'Recruiter_signup.html')
    elif request.method=='POST':
        fname=request.POST['fname']
        lname = request.POST['lname']
        image = request.FILES['image']
        contact=request.POST['contact']
        email = request.POST['email']
        password = request.POST['pwd']
        gender = request.POST['gender']
        company=request.POST['company']

        obj=User.objects.create_user(first_name=fname,last_name=lname,username=email,password=password)
        obj1=Recruiter.objects.create(user=obj,mobile=contact,image=image,gender=gender, company=company,type="recruiter",status="Pending")

        obj.save()
        obj1.save()

        return render(request, 'Recruiter_signup.html',{'data':"Signup Successful !!"})
    else:
        return render(request,'Recruiter_signup.html',{'data':"Signup Was Not Successful !!"})



def recruiter_logout(request):
    logout(request)
    return redirect('index')

def change_password_recruiter(request):
    if  not request.user.is_authenticated:
        return redirect('recruiter_login')
    error=""

    if request.method=="POST":
        c=request.POST['pwd']
        n=request.POST['newpwd']

        try:
            u=User.objects.get(id=request.user.id)
            if u.check_password(c):
                u.set_password(n)
                u.save()
                error="no"

            else:
                error="no"
        except:
            error="yes"
    d={'error':error}
    return render(request,'change_password_recruiter.html',d)



def latest_jobs(request):
    job=Job.objects.all().order_by("-start_date")
    d={'job':job}
    return render(request,'Latest_jobs.html',d)

def user_job_list(request):
    job=Job.objects.all().order_by("-start_date")
    user=request.user
    student=StudentUser.objects.get(user=user)
    data= Apply.objects.filter(student=student)
    li=[]
    for i in data:
        li.append(i.job.id)
    d={'job':job,'li':li}
    return render(request,'User_job_list.html',d)

def job_detail(request,pid):
    job=Job.objects.get(id=pid)
    d={'job':job}
    return render(request,'Job_detail.html',d)

def apply_for_job(request,pid):
    if  not request.user.is_authenticated:
        return redirect('user_login')
    error=""
    user=request.user
    student=StudentUser.objects.get(user=user)
    job=Job.objects.get(id=pid)
    date1=date.today()
    if job.end_date < date1:
        error="close"
    elif job.start_date > date1:
        error="notopen"
    else:
        if request.method=="POST":
            r=request.FILES['resume']
            Apply.objects.create(job=job,student=student,resume=r,applydate=date.today())
            error="done"
    d={'error':error}
    return render(request,'Apply_for_job.html',d)


def candidates_applied(request):
    if  not request.user.is_authenticated:
        return redirect('recruiter_login')
    data=Apply.objects.all()

    d={'data':data}
    return render(request,'Applied_candidates.html',d)