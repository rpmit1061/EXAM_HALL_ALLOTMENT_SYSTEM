from django.shortcuts import render, redirect
from django.http import HttpResponse
from .form import UserFrom, LoginForm
from .models import Destination
from django.views.decorators.cache import cache_control
# Create your views here.


def index(request):
    username = 'not logged in'
    if request.method == 'POST':
        myloginform = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password1']
        desst = Destination.objects.filter(username=username, password1=password).exists()
        if desst:
            request.session['username'] = username
            return render(request, 'user.html', {"username": username})
        else:
            resp_body = '<script>alert("Username And Password Not Matched");\
                             window.location="/"</script>'
            return HttpResponse(resp_body)
    else:
        form = LoginForm()
        context = {'form': form}
        return render(request, 'home.html', context)

# To Register Account with the GPCS with the help of form.
def register(request):
    if request.method == "POST":
        form = UserFrom(request.POST)
        if form.is_valid():
            form.save()
        resp_body = '<script>alert("User Created Successfully.");\
                                            window.location="/"</script>'
        return HttpResponse(resp_body)
    else:
        form = UserFrom()
        context = {'form': form}
        return render(request, 'register.html', context)


def user(request):
    return render(request, 'user.html')


def home(request):
    if request.session.get('username') is not None:
        return render(request, 'user.html')
    else:
        return redirect('/')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout(request):
    try:
        del request.session['username']
    except KeyError:
        pass
    resp_body = '<script>alert("You are logged out Successfully.");\
                                    window.location="/"</script>'
    return HttpResponse(resp_body)







