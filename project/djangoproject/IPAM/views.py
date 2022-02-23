from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Vlan
from .models import History_vlan, History_sousreseau, History_adresseip , History_tacheanalyse
from django.db.models import Q
from .models import Sousreseau
from .models import Adresseip
from .models import Tacheanalyse
from .models import Hote
from django.db.models import Count
from datetime import datetime
import pytz
from django.core.exceptions import ValidationError
import time
from django.utils import timezone
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
import webbrowser
from .serializers import vlanSerializer, sousreseauSerializer, adresseipSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view



# Create your views here.

def demo(request):
    idsr=request.GET.get('idsr')
    idvlan=request.GET.get('idvlan')
    vlans=Vlan.objects.all()
    sousreseaux=Sousreseau.objects.filter(vlan_id=idvlan).all()
    ipadress=Adresseip.objects.filter(sousreseau_id=idsr).all()
    disp=Adresseip.objects.filter(etat=False,sousreseau_id=idsr).count()
    utilis=Adresseip.objects.filter(etat=True,sousreseau_id=idsr).count()
    paginator=Paginator(ipadress, 20)
    page_number=request.GET.get("page", 1)
    page=paginator.get_page(page_number)
    return render(request,'demo.html',{'idvlan':idvlan,'idsr':idsr,'vlans':vlans,'sousreseaux':sousreseaux,'page':page,'disp':disp,'utilis':utilis})

def loginPage(request):
	
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('dashboard')
			else:
				messages.info(request, 'Nom utilisateur ou mot de passe est incorrect')

		context = {}
		return render(request, 'login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')

@login_required(login_url='login')
def dashboard(request):
    template=loader.get_template('dashboard.html')
    sousreseaux=Sousreseau.objects.all().count()
    vlans=Vlan.objects.all().count()
    adressesip=Adresseip.objects.all().count()
    res1='0.'+str(vlans)
    r1=int(float(res1)*100)
    res3='0.'+str(sousreseaux)
    r3=int(float(res3)*100)
    res4='0.'+str(adressesip)
    r4=int(float(res4)*100)
    attrib=Adresseip.objects.all().filter(etat=True).count()
    nonattrib=Adresseip.objects.filter(etat=False).count()
    sr=Sousreseau.objects.all()
    idsr=request.GET.get('idsr')
    ad=request.GET.get('ad')
    utilis=Adresseip.objects.filter(utliser=True,sousreseau_id=idsr).count()
    dispo=Adresseip.objects.filter(disponible=False,sousreseau_id=idsr).count()
    tot=Adresseip.objects.filter(sousreseau_id=idsr).count()
    data={'profile': request.user.username, 'email':request.user.email,'vlans':vlans,'sousreseaux':sousreseaux,'adressesip':adressesip,'attrib':attrib,'nonattrib':nonattrib,'sr':sr,'tot':tot,'utilis':utilis,'dispo':dispo,'idsr':idsr,'ad':ad}
    return HttpResponse(template.render(data))

@login_required(login_url='login')  
def vlan(request):
    search_query=request.GET.get('search','')
    if search_query:
        vlans=Vlan.objects.filter(Q(nom=search_query) | Q(idvlan=search_query))
    else:
        vlans=Vlan.objects.all().order_by('idvlan')
    paginator=Paginator(vlans, 5)
    page_number=request.GET.get('page',1)
    page=paginator.get_page(page_number)
    if page.has_next():
        next_url=f'?page={page.next_page_number()}'
    else:
        next_url=''
    if page.has_previous():
        prev_url= f'?page={page.previous_page_number()}'
    else:
        prev_url=''
    profile=request.user.username
    email=request.user.email
    return render(request,'vlan.html',{'profile':profile, 'email':email,'page':page,'next_page_url':next_url,'prev_page_url':prev_url})

    
@login_required(login_url='login')
def ajoutervlan(request):
    if request.method=='POST':
        idvlan=request.POST['idvlan']
        nomvlan=request.POST['nomvlan']
        description=request.POST['description']
        vl=Vlan.objects.filter(nom=nomvlan)
        if vl:
            messages.error(request, 'Nom de Vlan doit être unique!')
        else:
            Vlan.objects.create(idvlan=idvlan,nom=nomvlan,description=description)
            return redirect('vlan')
    idsvlans=range(1, 4097)
    profile=request.user.username
    email=request.user.email
    return render(request,'ajoutvlan.html',{'profile':profile,'email':email,'idsvlans':idsvlans})

@login_required(login_url='login')
def modifvlan(request,id):
    if request.method=='POST':
        idvlan=request.POST['idvlan']
        nomvlan=request.POST['nomvlan']
        description=request.POST['description']
        vl=Vlan.objects.filter(nom=nomvlan)
        if vl:
            messages.error(request, 'Nom de Vlan doit être unique!')
        else:
            Vlan.objects.filter(id=id).update(idvlan=idvlan,nom=nomvlan,description=description)
            return redirect('vlan')
    idsvlans=range(1, 4097)
    vlan=Vlan.objects.get(id=id)
    profile=request.user.username
    email=request.user.email
    return render(request,'modifvlan.html',{'profile':profile,'email':email,'vlan':vlan,'idsvlans':idsvlans})

def suppvlan(request,id):
    sres=Sousreseau.objects.filter(vlan_id=id)[:1]
    if sres:
        messages.error(request,'Vlan est utilisé dans un sous-réseau!!!')
    else:
        Vlan.objects.filter(id=id).delete()
    return redirect('vlan')

@login_required(login_url='login')
def historyvlan(request):
    search_query=request.GET.get('search','')
    if search_query:
        histvlans=History_vlan.objects.filter(Q(action=search_query) | Q(nouveau_nom=search_query) | Q(ancien_nom=search_query))
    else:
        histvlans=History_vlan.objects.all()
    paginator=Paginator(histvlans, 12)
    page_number=request.GET.get('page',1)
    page=paginator.get_page(page_number)
    if page.has_next():
        next_url=f'?page={page.next_page_number()}'
    else:
        next_url=''
    if page.has_previous():
        prev_url= f'?page={page.previous_page_number()}'
    else:
        prev_url=''
    profile=request.user.username
    email=request.user.email
    return render(request,'historyvlan.html',{'profile':profile,'email':email,'page':page, 'next_page_url':next_url,'prev_page_url':prev_url})

def supphistovlan(request):
    History_vlan.objects.all().delete()
    return redirect('historyvlan')

@login_required(login_url='login')
def sousreseau(request):
    search_query=request.GET.get('search','')
    if search_query:
        sousreseaux=Sousreseau.objects.filter(Q(nom=search_query) | Q(adresse=search_query))
    else:
        sousreseaux=Sousreseau.objects.all().order_by('adresse')
    paginator=Paginator(sousreseaux, 5)
    page_number=request.GET.get('page',1)
    page=paginator.get_page(page_number)
    if page.has_next():
        next_url=f'?page={page.next_page_number()}'
    else:
        next_url=''
    if page.has_previous():
        prev_url= f'?page={page.previous_page_number()}'
    else:
        prev_url=''
    profile=request.user.username
    email=request.user.email
    return render(request,'sousreseau.html',{'profile':profile, 'email':email,'page':page, 'next_page_url':next_url,'prev_page_url':prev_url})


@login_required(login_url='login')
def ajoutsousreseau(request):
    if request.method=='POST':
        nomsousreseau=request.POST['nomsousreseau']
        adresse=request.POST['adresse']
        taille=request.POST['taille']
        vlan=request.POST.get('idvlan')
        adsres=Sousreseau.objects.filter(adresse=adresse)
        if adsres:
            messages.error(request, 'Adresse du sous-réseau doit être unique!')
        else:
            Sousreseau.objects.create(nom=nomsousreseau,adresse=adresse,taille=taille,vlan_id=vlan)
            return redirect(sousreseau)
    lst=Vlan.objects.all()
    profile=request.user.username
    email=request.user.email
    return render(request,'ajoutsousreseau.html',{'profile':profile,'email':email,'lst':lst})

@login_required(login_url='login')
def detailsousreseau(request,id):
    sresx=Sousreseau.objects.filter(id=id).all()
    utilis=Adresseip.objects.filter(utliser=True,sousreseau_id=id).count()
    dispo=Adresseip.objects.filter(disponible=False,sousreseau_id=id).count()
    tot=Adresseip.objects.filter(sousreseau_id=id).count()
    profile=request.user.username
    email=request.user.email
    return render(request,'detailsousreseau.html',{'profile':profile, 'email':email,'sresx':sresx,'utilis':utilis,'dispo':dispo,'tot':tot})

def suppsousreseau(request,id):
    Adresseip.objects.filter(sousreseau_id=id).delete()
    Sousreseau.objects.filter(id=id).delete()
    return redirect('sousreseau')

@login_required(login_url='login')
def historysousreseau(request):
    search_query=request.GET.get('search','')
    if search_query:
        histsres=History_sousreseau.objects.filter(Q(action=search_query) | Q(nouveau_nom=search_query) | Q(nouveau_adresse=search_query))
    else:
        histsres=History_sousreseau.objects.all()
    paginator=Paginator(histsres, 12)
    page_number=request.GET.get('page',1)
    page=paginator.get_page(page_number)
    if page.has_next():
        next_url=f'?page={page.next_page_number()}'
    else:
        next_url=''
    if page.has_previous():
        prev_url= f'?page={page.previous_page_number()}'
    else:
        prev_url=''
    profile=request.user.username
    email=request.user.email
    return render(request,'historysousreseau.html',{'profile':profile,'email':email,'page':page, 'next_page_url':next_url,'prev_page_url':prev_url})

def supphistosousreseau(request):
    History_sousreseau.objects.all().delete()
    return redirect('historysousreseau')


@login_required(login_url='login')
def ipsousreseau(request,id):
    if request.method=='POST':
        taille=int(request.POST.get('taille'))+1
        for i in range(1,taille):
            ip=request.POST.get('adresse')[:-1]
            ipadress=ip+str(i)
            nomhote="Hôte"+str(i)
            Adresseip.objects.create(adresse=ipadress,sousreseau_id=id)
            Hote.objects.create(nom=nomhote,sousreseau_id=id)
        #return redirect('sousreseau') 
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    sreseau=Sousreseau.objects.get(id=id)
    idsr=Adresseip.objects.filter(sousreseau_id=id).all()[:1]
    profile=request.user.username
    email=request.user.email
    return render(request,'ipsousreseau.html',{'profile':profile,'email':email,'sreseau':sreseau,'idsr':idsr})


@login_required(login_url='login')
def ipadresses(request,id):
    etat=request.GET.get('etat')
    if etat:
        ipadress=Adresseip.objects.filter(sousreseau_id=id, etat=etat).all()
        paginator=Paginator(ipadress, 12)
        page_number=request.GET.get('pagee',1)
        page=paginator.get_page(page_number)
        p=request.GET.get('ad')
        if page.has_next():
            next_url=f'?pagee={page.next_page_number()}&ad={p}&etat={etat}'
        else:
            next_url=''
        if page.has_previous():
            prev_url= f'?pagee={page.previous_page_number()}&ad={p}&etat={etat}'
        else:
            prev_url=''
    else:
        ipadress=Adresseip.objects.filter(sousreseau_id=id).all()
        paginator=Paginator(ipadress, 12)
        page_number=request.GET.get('page',1)
        page=paginator.get_page(page_number)
        p=request.GET.get('ad')
        if page.has_next():
            next_url=f'?page={page.next_page_number()}&ad={p}'
        else:
            next_url=''
        if page.has_previous():
            prev_url= f'?page={page.previous_page_number()}&ad={p}'
        else:
            prev_url=''
    profile=request.user.username
    email=request.user.email
    disp=Adresseip.objects.filter(disponible=False,sousreseau_id=id).count()
    utilis=Adresseip.objects.filter(utliser=True,sousreseau_id=id).count()
    sreseau=id
    sr=Hote.objects.filter(sousreseau_id=id,etat=False).all()
    return render(request,'ipadresses.html',{'profile':profile, 'email':email,'page':page,'next_page_url':next_url,'prev_page_url':prev_url,'disp':disp,'utilis':utilis,'sreseau':sreseau,'p':p,'etat':etat})

@login_required(login_url='login')
def attadressesip(request,id):
    idsr=request.GET.get('idadsr')
    sr=Hote.objects.filter(sousreseau_id=idsr,etat=False).all()
    idadip=id
    sreseau=idsr
    profile=request.user.username
    email=request.user.email
    return render(request,'attadressesip.html',{'profile':profile, 'email':email,'sr':sr,'idadip':idadip, 'sreseau':sreseau})


@login_required(login_url='login')
def attribipadresses(request,id):
    if request.method=='POST':
        hote=request.POST.get('hote')
        idadsr=request.GET.get('idadsr')
        Adresseip.objects.filter(id=id).update(nom=hote,etat=True,utliser=True,disponible=True)
        Hote.objects.filter(nom=hote, sousreseau_id=idadsr).update(etat=True)
        messages.error(request,'Attribuer avec succès')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



@login_required(login_url='login')
def anulattribipadresses(request,id,hote):
    idsr=request.GET.get('idadsr')
    Adresseip.objects.filter(id=id).update(nom="",etat=False,utliser=False,disponible=False)
    Hote.objects.filter(nom=hote, sousreseau_id=idsr).update(etat=False)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def historyadresseip(request):
    search_query=request.GET.get('search','')
    if search_query:
        histadip=History_adresseip.objects.filter(Q(nouveau_nom=search_query) | Q(nouveau_adresse=search_query))
    else:
        histadip=History_adresseip.objects.all()
    paginator=Paginator(histadip, 12)
    page_number=request.GET.get('page',1)
    page=paginator.get_page(page_number)
    if page.has_next():
        next_url=f'?page={page.next_page_number()}'
    else:
        next_url=''
    if page.has_previous():
        prev_url= f'?page={page.previous_page_number()}'
    else:
        prev_url=''
    profile=request.user.username
    email=request.user.email
    return render(request,'historyadresseip.html',{'profile':profile,'email':email,'page':page,'next_page_url':next_url,'prev_page_url':prev_url})

def supphistoadresseip(request):
    History_adresseip.objects.all().delete()
    return redirect('historyadresseip')


@login_required(login_url='login')
def scan(request,id):
    sreseau=Sousreseau.objects.get(id=id)
    ipadress=Adresseip.objects.filter(sousreseau_id=id).all()
    disp=Adresseip.objects.filter(disponible=False,sousreseau_id=id).count()
    utilis=Adresseip.objects.filter(utliser=True,sousreseau_id=id).count()
    profile=request.user.username
    email=request.user.email
    return render(request,'scan.html',{'profile':profile,'email':email,'ipadress':ipadress,'sreseau':sreseau,'disp':disp,'utilis':utilis})
    


@login_required(login_url='login')
def tacheanalyse(request): 
    search_query=request.GET.get('search','')
    if search_query:
        tach=Tacheanalyse.objects.filter(Q(nom=search_query))
    else:
        tach=Tacheanalyse.objects.all()
    paginator=Paginator(tach, 5)
    page_number=request.GET.get('page',1)
    page=paginator.get_page(page_number)
    if page.has_next():
        next_url=f'?page={page.next_page_number()}'
    else:
        next_url=''
    if page.has_previous():
        prev_url= f'?page={page.previous_page_number()}'
    else:
        prev_url=''
    profile=request.user.username
    email=request.user.email
    nbtach=Tacheanalyse.objects.all().count()
    return render(request,'tacheanalyse.html',{'profile':profile,'email':email,'page':page,'nbtach':nbtach})

@login_required(login_url='login')
def creetacheanalyse(request):
    if request.method=='POST':
       tache=request.POST['tache']
       tm=request.POST['temps']
       date=request.POST['date']
       etat=request.POST['etat']
       sreseau=request.POST.get('idsreseau')
       Tacheanalyse.objects.create(nom=tache,temp=tm,etat=etat,date_tache=date,date_creation=str(timezone.now()),sousreseau_id=sreseau)
       return redirect('tacheanalyse')
    sr=Sousreseau.objects.all()
    profile=request.user.username
    email=request.user.email
    return render(request,'creetacheanalyse.html',{'profile':profile,'email':email,'sr':sr})

@login_required(login_url='login')
def modiftacheanalyse(request,id):
    if request.method=='POST':
       tache=request.POST['tache']
       tm=request.POST['temps']
       date=request.POST['date']
       etat=request.POST['etat']
       sreseau=request.POST.get('idsreseau')
       Tacheanalyse.objects.filter(id=id).update(nom=tache,temp=tm,etat=etat,date_tache=date,date_creation=str(timezone.now()),sousreseau_id=sreseau)
       return redirect('tacheanalyse')
    tch=Tacheanalyse.objects.get(id=id)
    sr=Sousreseau.objects.all()
    profile=request.user.username
    email=request.user.email
    return render(request,'modiftacheanalyse.html',{'profile':profile,'email':email,'sr':sr,'tch':tch})

def supptacheanalyse(request,id):
    Tacheanalyse.objects.filter(id=id).delete()
    return redirect('tacheanalyse')

@login_required(login_url='login')
def historytacheanalyse(request):
    search_query=request.GET.get('search','')
    if search_query:
        histtach=History_tacheanalyse.objects.filter(Q(action=search_query) | Q(nouveau_nom=search_query) | Q(ancien_nom=search_query))
    else:
        histtach=History_tacheanalyse.objects.all()
    paginator=Paginator(histtach, 12)
    page_number=request.GET.get('page',1)
    page=paginator.get_page(page_number)
    if page.has_next():
        next_url=f'?page={page.next_page_number()}'
    else:
        next_url=''
    if page.has_previous():
        prev_url= f'?page={page.previous_page_number()}'
    else:
        prev_url=''

    sr=Sousreseau.objects.all()
    profile=request.user.username
    email=request.user.email
    return render(request,'historytacheanalyse.html',{'profile':profile,'email':email,'page':page, 'next_page_url':next_url,'prev_page_url':prev_url,'sr':sr})

def supphistotacheanalyse(request):
    History_tacheanalyse.objects.all().delete()
    return redirect('historytacheanalyse')

def scanplanif():
    global scheduler
    tach=Tacheanalyse.objects.filter(etat=True)
    if tach:
        print('Scan lancer.....')
    for t in tach:
        idsr=t.sousreseau_id
        Sousreseau.objects.filter(id=idsr).update(etat=True,derniere_scan=str(datetime.now())) 
        #url = "http://127.0.0.1:8000/ipadresses/scan/"+str(t.sousreseau_id)
        #webbrowser.open(url,new=2) 
        scheduler.pause()
        #scheduler.shutdown(wait=True)
     
def hour():
    tch=Tacheanalyse.objects.filter(etat=True).all()
    for t in tch:
        h=t.temp[:-3]
    #h=tch[0].temp[:-3]
        return h

def minute():
    tch=Tacheanalyse.objects.filter(etat=True)
    for t in tch:
        m=t.temp[3:5]
    #m=tch[0].temp[3:5]
        return m


def date():
    tch=Tacheanalyse.objects.filter(etat=True)
    for t in tch:
        dend=t.date_tache
    #dend=tch[0].date_tache
        return dend

h=hour()
#print(h)
m=minute()
#print(m)
d=date()
#dte=str(d)
#print(dte)


executors = {
    'default': ThreadPoolExecutor(20),
    'processpool': ProcessPoolExecutor(5)
}

job_defaults = {
    'coalesce': False,
    'max_instances': 10,
}

scheduler = BackgroundScheduler(executors=executors, job_defaults=job_defaults, timezone='Africa/Tunis')
scheduler.add_job(scanplanif, trigger='cron', hour=h, minute=m, start_date=d)
scheduler.start()


@login_required(login_url='login')
def rapport(request):
    idsr=request.POST.get('sreseau')
    adsres=Adresseip.objects.filter(sousreseau_id=idsr).all()
    lst=Sousreseau.objects.all()
    adrs=Sousreseau.objects.filter(id=idsr).all()
    profile=request.user.username
    email=request.user.email
    return render(request,'rapport.html',{'profile':profile,'email':email,'adsres':adsres,'lst':lst,'adrs':adrs})


