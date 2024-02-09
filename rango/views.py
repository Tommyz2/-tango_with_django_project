from django.http import HttpResponse
from django.shortcuts import render
from rango.models import Category
from rango.models import Page
from django.shortcuts import get_object_or_404
from rango.forms import PageForm
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.models import User
from rango.forms import UserForm, UserProfileForm



def about(request):
    return render(request, 'rango/about.html')


def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]  # 获取浏览次数最多的五个页面
    context_dict = {
        'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!',
        'categories': category_list,
        'pages': page_list,
    }
    return render(request, 'rango/index.html', context=context_dict)
def some_view(request):
    categories = Category.objects.all()  
    return render(request, 'rango/template.html', {'categories': categories})
def show_category(request, category_name_slug):

    category = get_object_or_404(Category, slug=category_name_slug)
      
    pages = Page.objects.filter(category=category)
    
    context_dict = {'pages': pages, 'category': category}
    
    return render(request, 'rango/category.html', context=context_dict)
def add_category(request):
    form = CategoryForm()
    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)
            # Now that the category is saved, we could confirm this.
            # For now, just redirect the user back to the index view.
            return redirect('/rango/')
    else:
        # Handle the case when the form is not valid.
        pass
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None
# You cannot add a page to a Category that does not exist...
    if category is None:
       return redirect('/rango/')
    form = PageForm()
    if request.method == 'POST':
      form = PageForm(request.POST)
      if form.is_valid():
        if category:
           page = form.save(commit=False)
           page.category = category
           page.views = 0
           page.save()
           return redirect(reverse('rango:show_category',
                                   kwargs={'category_name_slug':
                                   category_name_slug}))
        else:
             print(form.errors)
    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)
if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
else:# Save the user's form data to the database.
 def register(request):
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # 这里应该继续您的用户注册逻辑，比如设置密码，保存用户档案等

            # 最后重定向到一个新的URL或者渲染一个确认页面
            return redirect('some-success-url')
        else:
            # 如果表单无效，显示表单错误
            print(user_form.errors, profile_form.errors)
    else:
        # 对于非POST请求，提供空的表单实例
        user_form = UserForm()
        profile_form = UserProfileForm()

        # 渲染注册页面，并传递表单实例到模板
        return render(request, 'rango/register.html', {'user_form': user_form, 'profile_form': profile_form})


