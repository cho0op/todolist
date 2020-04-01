from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login,logout, authenticate
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'todo/home.html')

def signupuser(request):
    if request.method=='GET':
        return render(request, 'todo/signupuser.html', {'form':UserCreationForm()})
    else:
        if request.POST['password1']==request.POST['password2']:
            try:
                user=User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currenttodos')
            except IntegrityError:
                return render(request, 'todo/signupuser.html', {'form': UserCreationForm(), 'error': 'this name is already taken'})
        else:
            print("error")
            return render(request, 'todo/signupuser.html', {'form': UserCreationForm(), 'error':'passwod didn\'t math'})


def loginuser(request):
    if request.method=='GET':
        return render(request, 'todo/loginuser.html', {'form':AuthenticationForm()})
    else:
        user=authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/loginuser.html', {'form':AuthenticationForm(),'error':'username or password don\'t match'})
        else:
            login(request, user)
            return redirect('currenttodos')

@login_required
def logoutuser(request):
    if(request.method=="POST"):
        logout(request)
        return redirect(home)

@login_required
def createtodo(request):
    todos=Todo.objects.filter(user=request.user, completing_date__isnull=True)
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html', {'form': TodoForm()})
    else:
        try:
            form=TodoForm(request.POST)
            newTodo=form.save(commit=False)
            newTodo.user=request.user
            newTodo.save()
            return render(request,'todo/currenttodos.html', {'todos':todos})
        except ValueError:
            return render(request, 'todo/createtodo.html', {'form': TodoForm(),'error' : 'value in form doesn\'t mathc'})

@login_required
def currenttodos(request):
    todos= Todo.objects.filter(user=request.user, completing_date__isnull=True)
    return render(request, 'todo/currenttodos.html', {'todos':todos})

@login_required
def viewtodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'todo/viewtodo.html', {'todo' : todo, 'form':form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/viewtodo.html', {'todo':todo, 'form':form,'error' : 'value in form doesn\'t mathc'})

@login_required
def completetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.completing_date = timezone.now()
        todo.save()
        return redirect('currenttodos')

@login_required
def deletetodo(request, todo_pk ):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos')

@login_required
def completedtodos(request):
    todos = Todo.objects.filter(user=request.user, completing_date__isnull=False).order_by('-completing_date')
    return render(request, 'todo/copletedtodos.html', {'todos': todos})