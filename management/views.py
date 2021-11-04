from django.shortcuts import render

def management(request):

    return render(request, 'management/management.html')
