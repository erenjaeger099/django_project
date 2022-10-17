from ast import Param
from colorsys import TWO_THIRD
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.core.files.storage import FileSystemStorage
from datetime import date
import mysql.connector
from django.template import loader
# from  import Two_face

login = ''
club = ''

mydb=mysql.connector.connect(host="localhost",user="root",password="",charset='utf8',database="susanoo")

def check_user(name,password):
    cursor=mydb.cursor()
    cursor.execute('SELECT * FROM user WHERE name = %s and password = %s', (name, password))
    account = cursor.fetchone()
    if account:
        return True
    return False

def id():
    cursor=mydb.cursor(buffered=True)
    cursor.execute('SELECT id FROM event ORDER BY id DESC')
    a=cursor.fetchone()
    return a[0]

def event(club,genre,time):
    c=[]
    bash=0
    cash=0
    hash=0
    today=date.today()
    g=['technical','art','dance','music','other']
    cl=['prayas_india','hncc','arts','iete','iste','model','leo','rotract','sports','nss','eco','sarjana','ls','grs','painting','photographic','dhatvika','quimica','sae']
    cursor=mydb.cursor(buffered=True)
    s="SELECT * FROM event "
    for i in range(len(club)):
        if club[i] != 'off':
            if(bash==0):
                s=s+"where (club = '"+cl[i]
                bash=1
            else:
                s=s+"' or club = '"+cl[i]
    if(bash!=0):
        s=s+"')"
    for j in range(len(genre)):
        if genre[j] != 'off':
            if(bash==0):
                s=s+"where (genere = '"+g[j]
                bash=1
                cash=1
            elif(cash==0):
                s=s+" and (genere = '"+g[j]
                cash=1
            else:
                s=s+"' or genere = '"+g[j]
    if(cash!=0):
        s=s+"')"
    for k in range(len(time)):
        if time[k] != 'off':
            if(bash==0 and cash==0):
                if(k==0):
                    s=s+"where (start>'"+str(today)+"'"
                elif(k==1):
                    s=s+"where ((start<='"+str(today)+"' and end>='"+str(today)+"')"
                elif(k==2):
                    s=s+"where (end<'"+str(today)+"'"
                bash=1
                cash=1
                hash=1
            elif(hash==0):
                if(k==0):
                    s=s+" and (start>'"+str(today)+"'"
                elif(k==1):
                    s=s+" and ((start<='"+str(today)+"' and end>='"+str(today)+"')"
                elif(k==2):
                    s=s+" and (end<'"+str(today)+"'"
                hash=1
            else:
                if(k==0):
                    s=s+" or start>'"+str(today)+"'"
                elif(k==1):
                    s=s+" or (start<='"+str(today)+"' and end>='"+str(today)+"')"
                elif(k==2):
                    s=s+" or end<'"+str(today)+"'"
    if(hash!=0):
        s=s+")"
    s=s+' order by id desc'
    cursor.execute(s)
    a = cursor.fetchone()
    while(a):
        b={'name':a[2],'start':a[3],'end':a[4],'club':a[5],'genre':a[6],'eligibility':a[7],'description':a[8],'prize':a[10], 'link':a[11], 'date':a[13], 'poster':a[1]}
        c.append(b)
        a = cursor.fetchone()
    return c

def delete(id):
    cursor=mydb.cursor(buffered=True)
    cursor.execute('DELETE FROM event WHERE id=%s',(id,))
    mydb.commit()

def club_event(name):
    c=[]
    cursor=mydb.cursor()
    cursor.execute('SELECT * FROM event WHERE club = %s order by id desc', (name,))
    a = cursor.fetchone()
    while(a):
        b={'id':a[0],'name':a[2],'start':a[3],'end':a[4],'club':a[5],'genre':a[6],'eligibility':a[7],'description':a[8],'prize':a[10], 'link':a[11], 'date':a[13], 'poster':a[1]}
        c.append(b)
        a = cursor.fetchone()
    return c

def insert_event(id, poster, name, start, end, club, genre, eligibility, short_desc, description, prize, link, add_link, today):
    cursor=mydb.cursor(buffered=True)
    cursor.execute('INSERT INTO event VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (id, poster, name, start, end, club, genre, eligibility, short_desc, description, prize, link, add_link, today))
    mydb.commit()

def home(request):
    dict={}
    time=[request.POST.get('upcomming','off'),request.POST.get('ongoing','off'),request.POST.get('past','off')]
    genre=[request.POST.get('technical','off'),request.POST.get('art','off'),request.POST.get('dance','off'),request.POST.get('music','off'),request.POST.get('other','off')]
    club=[request.POST.get('prayas_india','off'),request.POST.get('hncc','off'),request.POST.get('arts','off'),request.POST.get('iete','off'),request.POST.get('iste','off'),request.POST.get('model','off'),request.POST.get('leo','off'),request.POST.get('rotract','off'),request.POST.get('sports','off'),request.POST.get('nss','off'),request.POST.get('eco','off'),request.POST.get('sarjana','off'),request.POST.get('ls','off'),request.POST.get('grs','off'),request.POST.get('painting','off'),request.POST.get('photographic','off'),request.POST.get('dhatvika','off'),request.POST.get('quimica','off'),request.POST.get('sae','off')]
    g=['technical','art','dance','music','other']
    cl=['prayas_india','hncc','arts','iete','iste','model','leo','rotract','sports','nss','eco','sarjana','ls','grs','painting','photographic','dhatvika','quimica','sae']
    t=['upcomming','ongoing','past']
    for i in range(len(time)):
        if(time[i]!='off'):
            dict[t[i]]='checked'
        else:
            dict[t[i]]=''
    for i in range(len(genre)):
        if(genre[i]!='off'):
            dict[g[i]]='checked'
        else:
            dict[g[i]]=''
    for i in range(len(club)):
        if(club[i]!='off'):
            dict[cl[i]]='checked'
        else:
            dict[cl[i]]=''
    param={'event':event(club,genre,time),'check':dict}
    return render(request,'home.html',param)

def about_us(request):
    return render(request,'about_us.html')

def signin(request):
    global login, club
    if login:
        return redirect('c_home')
    msg=''
    name=request.POST.get('name','')
    password=request.POST.get('password','')
    if(name != '' and password != ''):
        if not check_user(name,password):
            msg="Incorrect Username or Password"
        else:
            login=True
            club=name
            return redirect('c_home')
    param={'msg':msg}
    return render(request,'signin.html',param)

def logout(request):
    global login, club
    login=False
    club=''
    return redirect('home')

def club_home(request):
    global club, login
    id=request.POST.get('delete','none')
    if id != 'none':
        delete(id)
    if not login:
        return redirect('signin')
    param={'event':club_event(club)}
    return render(request,'c_home.html',param)

def add_event(request):
    global club
    msg=''
    msg1=''
    if not login:
        return redirect('signin')
    if request.method == "POST":
        n=int(id())+1
        poster=request.FILES['poster']
        poster_name=str(n)+"_poster."+(poster.name).split('.')[-1]
        name=request.POST.get('name','')
        start=request.POST.get('start','')
        end=request.POST.get('end','')
        genre=request.POST.get('genre','')
        eligibility=request.POST.get('eligibility','')
        short_desc=request.POST.get('short_desc','')
        description=request.POST.get('description','')
        prize=request.POST.get('prize','')
        link=request.POST.get('link','')
        add_link=request.POST.get('add_link','')
        today=date.today()
        if name != '' and start != '' and end != '' and genre != '':
            if(len(short_desc)>200):
                msg='Short Description must be under 200 words'
            elif(start>end):
                msg='Event Starting date is ahead of Ending date'
            else:
                fs = FileSystemStorage()
                fs.save(poster_name,poster)
                insert_event(n, poster_name, name, start, end, club, genre, eligibility, short_desc, description, prize, link, add_link,today)
                msg1='Event added Successfully'
    param={'msg':msg,'msg1':msg1}
    return render(request,'add_event.html',param)



def update(request, id):
    
    cursor=mydb.cursor(id=id)
    template = loader.get_template('update.html')
    context = {
    'mycursor': cursor,

  }
    return HttpResponse(template.render(context, request,'update.html',Param))
