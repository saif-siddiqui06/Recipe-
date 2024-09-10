from django.shortcuts import render, get_object_or_404, redirect
from .models import Recipe, Comment, Rating
from .forms import CommentForm, RatingForm, RecipeForm
from django.contrib.auth.decorators import login_required
from .forms import CommentForm, RatingForm
from django.contrib import messages
from django.contrib.auth.models import User 

from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm


def home(request):
    return render(request,'recipe_book/home.html')

def recipe_list(request):
    query = request.GET.get('q')
    recipes = Recipe.objects.all()

    if query:
        recipes = recipes.filter(title__icontains=query)

    return render(request, 'recipe_book/recipe_list.html', {'recipes': recipes, 'query': query})


def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    comments = Comment.objects.filter(recipe=recipe)
    ratings = Rating.objects.filter(recipe=recipe)
    average_rating = calculate_average_rating(ratings)

    comment_form = CommentForm()
    rating_form = RatingForm()

    return render(request, 'recipe_book/recipe_detail.html', {
        'recipe': recipe,
        'comments': comments,
        'ratings': ratings,
        'average_rating': average_rating,
        'comment_form': comment_form,
        'rating_form': rating_form,
    })



@login_required
def add_comment(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.recipe = recipe
            comment.user = request.user
            comment.save()
            return redirect('recipe_detail', recipe_id=recipe_id)
    else:
        form = CommentForm()

    return render(request, 'recipe_book/add_comment.html', {'form': form})

@login_required
def add_rating(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)

    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.recipe = recipe
            rating.user = request.user
            rating.save()
            return redirect('recipe_detail', recipe_id=recipe_id)
    else:
        form = RatingForm()

    return render(request, 'recipe_book/add_rating.html', {'form': form})
  
@login_required
def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            print('save')
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            return redirect('recipe_list')
    else:
        form = RecipeForm()

    return render(request, 'recipe_book/add_recipe.html', {'form': form})

@login_required
def edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)

    if request.user != recipe.author:
        return render(request, 'recipe_book/permission_denied.html')

    if request.method == 'POST':
        form = RecipeForm(request.POST, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('recipe_detail', recipe_id=recipe_id)
    else:
        form = RecipeForm(instance=recipe)

    return render(request, 'recipe_book/edit_recipe.html', {'form': form, 'recipe': recipe})

def calculate_average_rating(ratings):
    if ratings:
        total_ratings = sum([rating.value for rating in ratings])
        average_rating = total_ratings / len(ratings)
        return round(average_rating, 1)
    return 0

# views.py

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('recipe_list')
    return render(request, 'registration/login.html')

def user_logout(request):
    logout(request)
    return redirect('recipe_list')



def user_signup(request):
     print('start')
     if request.method == 'POST':
          username = request.POST.get('username')
          email = request.POST.get('email')
          password = request.POST.get('password')
          
          print("Profile updated")
          user = User.objects.filter(username=username)
          
          if user.exists():
               messages.info(request,'Already have username')
               print('Profile already exists')
               return redirect('.')
          
          user = User.objects.create(
               username=username,
               email = email,
                              )
          
          print("Profile created")
          user.set_password(password)
          user.save()
          
          messages.success(request, "Profile Created.")
          return redirect('.')
          # return HttpResponse('Registration successful')
     
     return render(request, 'registration/signup.html')