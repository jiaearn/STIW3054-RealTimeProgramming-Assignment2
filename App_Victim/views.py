from django.shortcuts import render
from .models import Victim


def victim(request):
    if request.method == "POST":
        name = request.POST["name"]
        icNum = request.POST["icNum"]
        phone = request.POST["phone"]

        if not Victim.objects.filter(ic_no=icNum).exists():
            victimDetail = Victim(name=name, ic_no=icNum, phone=phone)
            victimDetail.save()
            respond = "{} has been successfully add to the victim list.".format(name)
            return render(request, 'App_Victim/victim.html', {"status": respond})
        else:
            respond = "Fail. This victim is already exist. Please insert again."
            return render(request, 'App_Victim/victim.html', {"status": respond})
    return render(request, 'App_Victim/victim.html')


def victim_report(request):
    victim_list = Victim.objects.all().order_by("-ic_no")
    return render(request, 'App_Victim/victim_report.html', context={'victim_list': victim_list})


def index(request):
    victims = Victim.objects.all()
    return render(request, 'App_Victim/index.html', context={'victims': victims})


def victim_detail(request, ic_no):
    victim = Victim.objects.get(pk=ic_no)  # pk='primary key'

    if request.method == "POST":
        name = request.POST["name"]
        icNum = request.POST["icNum"]
        phone = request.POST["phone"]

        victim.icNo = icNum
        victim.name = name
        victim.phone = phone
        victim.save()
        victim_list = Victim.objects.all().order_by("-ic_no")
        return render(request, 'App_Victim/victim_report.html', context={'victim_list': victim_list})

    return render(request, 'App_Victim/victim_detail.html', context={'victim': victim})
