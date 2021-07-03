from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from App_Login.forms import SignUpForm, UserProfileChange, ProfilePic

#-------------sign up part------------
def sign_up(request):

    # form = UserCreationForm ()
    form = SignUpForm() # now here, i use existing form instead of jango built in form and this form can override in built in form 
    registered = False
    if request.method == 'POST':
        # form = UserCreationForm(data=request.POST)
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            form.save()
            registered = True

    dict = {'form':form, 'registered': registered}
    return render(request, 'App_Login/signup.html', context=dict)

#----------Login part----------------
def login_page(request):
    form = AuthenticationForm() #calling function to authenticate 

    if request.method =="POST":
        form = AuthenticationForm(data=request.POST) #taking user given data from input fields 
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user =authenticate(username=username, password=password)
            if user is not None:    #checking user whether it exists in database or not 
                login(request, user)
                return HttpResponseRedirect(reverse('index')) #if exists a user then, it will load index page 

    return render(request, 'App_Login/login.html', context={'form':form}) #for fresh load a page, it will load login page to login                
                 
#----------Log out part-----------
@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

#----------Profile part------------
@login_required
def profile(request):
    return render(request, 'App_Login/profile.html', context={})

#---------User Profile Change Part--------------
@login_required
def profile_change(request):
    current_user = request.user
    form = UserProfileChange(instance=current_user)
    if request.method == 'POST':
        form = UserProfileChange(request.POST, instance=current_user)
        if form.is_valid():
            form.save()
            form = UserProfileChange(instance=current_user)
    return render(request, 'App_Login/change_profile.html', context={'form':form})

#--------- Password Change Part---------------
@login_required
def pass_change(request):
    current_user = request.user
    changed = False
    form = PasswordChangeForm(current_user)
    if request.method =='POST':
        form = PasswordChangeForm(current_user, data=request.POST)
        if form.is_valid():
            form.save()
            changed = True
    return render(request, 'App_Login/change_pass.html', context={'form':form, 'changed':changed})

 #--------- Profile Pic Adding Part--------------- 
@login_required
def add_pro_pic(request):
    if request.method == 'POST':
        form = ProfilePic(request.POST, request.FILES) # taking files from user and saveing into form
        if form.is_valid(): # checking whether form is empty or not
         user_obj = form.save(commit=False) # commit false means that for which user i want to set profile picture is not defined yet. 
         user_obj.user = request.user # setting user for whom i want to set profile picture
         user_obj.save() # after taking picture form is saved
        return HttpResponseRedirect(reverse('App_Login:profile')) # setting picture it redirect the profile page 
    else:
        form = ProfilePic()
    return render(request, 'App_Login/pro-pic-add.html', context={'form':form})
 
 #--------- Profile Pic Changing Part--------------- 
@login_required
def change_pro_pic(request):
    form = ProfilePic(instance=request.user.user_profile)
    if request.method == 'POST':
        form = ProfilePic(request.POST, request.FILES, instance=request.user.user_profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('App_Login:profile'))
    return render(request, 'App_Login/pro-pic-add.html', context={'form':form})