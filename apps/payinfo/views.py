from django.shortcuts import render


def payinfo(request):
    return render(request, 'payinfo/payinfo.html')
