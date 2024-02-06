from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url='/login/')
def recipes(request):
    if request.method == "POST":
        data = request.POST

        # Access data
        recipes_name = data.get('recipes_name')
        recipes_description = data.get('recipes_description')
        recipes_image = request.FILES.get('recipes_image')
        print(recipes_name)
        print(recipes_description)   
        print(recipes_image)  

        # creating object
        Recipes.objects.create(
            recipes_name = recipes_name,
            recipes_description = recipes_description,
            recipes_image = recipes_image
            )
        # redirecting the page
        return redirect('/recipes/')

    # show data
    queryset = Recipes.objects.all()

    if request.GET.get('search'):
        # print(request.GET.get('search'))
        queryset = queryset.filter(recipes_name__icontains = request.GET.get('search'))

    context = {'recipes' : queryset}
    return render(request,"vege_temp/recipes.html", context)

# for delete-update operation
@login_required(login_url='/login/')
def delete_recipes(request, id):
    queryset = Recipes.objects.get(id = id)
    queryset.delete()
    return redirect('/recipes/')


@login_required(login_url='/login/')
def update_recipes(request, id):
    queryset = Recipes.objects.get(id = id)
    if request.method == "POST":
        data = request.POST
        recipes_name = data.get('recipes_name')
        recipes_description = data.get('recipes_description')
        recipes_image = request.FILES.get('recipes_image')

        queryset.recipes_name = recipes_name
        queryset.recipes_description = recipes_description

        if recipes_image:
            queryset.recipes_image = recipes_image
        
        queryset.save()
        return redirect('/recipes/')

    context = {'recipes': queryset}
    return render(request, 'vege_temp/update_recipes.html', context)



# for login-logout-register page
def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username = username).exists():
            messages.error(request, 'Invailid username')
            return redirect('/login/')

        user = authenticate(username = username, password = password)
        if user is None:
            messages.error(request, 'Invailid password')
            return redirect('/login/')
        else:
            login(request, user)
            return redirect('/recipes/')


    return render(request, 'vege_temp/login.html')





def logout_page(request):
    logout(request)
    return redirect('/login/')




def register(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username = username)

        if user.exists():
            messages.info(request, 'username already exist')
            return redirect('/register/')

        user = User.objects.create(
        first_name = first_name,
        last_name = last_name,
        username = username
        )
        user.set_password(password)
        user.save()
        messages.info(request, 'Account created successfully')

        return redirect('/register/')
    return render(request, 'vege_temp/register.html')


