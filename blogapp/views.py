from django.shortcuts import render,HttpResponse,redirect
from .models import *
from django.shortcuts import get_object_or_404
from django.db.models import Q,Count
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from .models import ContactUs,Ajaxx
from django.core.mail import send_mail
from django.conf import settings


def home(request):
  categories = Category.objects.all()
  featured_post=Blogs.objects.filter(is_featured=True,status='published')
  posts=Blogs.objects.filter(is_featured=False,status='published').order_by('-created_at')
  paginator=Paginator(posts,3)
  page=request.GET.get('page')
  paged_post=paginator.get_page(page)
  latestpost_list = Blogs.objects.all().order_by('-created_at')[:3]
  
  

  
  context={
    'categories':categories,
    'featured_post':featured_post,
    'posts':paged_post,
    'latestpost_list':latestpost_list,
    
  }
  return render(request,'index.html',context)

def category(request,category_id):
  #category_counts=Category.objects.all().count()
  #fetch the posts that belongs to the category with id
  posts = Blogs.objects.filter(status='published',category=category_id)
  '''used this when u want to perform ur own action'''
  try:
    category=Category.objects.get(pk=category_id)
  except:
    return redirect('index')
    #return HttpResponse("Category doesn't exist ")
  

  '''use this when u want to show 404 error'''
  #category=get_object_or_404(Category,pk=category_id)
  
  context={
    'posts':posts,
    'category':category,
    

  }
  return render(request,'category.html',context)

def blogdeatil(request,slug):
  single_post=get_object_or_404(Blogs,slug=slug,status='published')
  lastest_post=Blogs.objects.all().order_by('-created_at')[:3]


  
  context={
    'single_post':single_post,
    'lastest_post':lastest_post
    
  }
  return render(request,'blogs.html',context)

def search(request):
  keyword=request.GET.get('keyword')
  blogs=Blogs.objects.filter(Q(title__icontains=keyword) | Q(short_description__icontains=keyword),status='published')
  
  context={
    'blogs':blogs,
    'keyword':keyword,
   
  }
  return render(request,'search.html',context)

def register(request):
  return render(request,'register.html')


def contact(request):
  if request.method=='POST':
    name=request.POST.get('name')
    email=request.POST.get('email')
    message=request.POST.get('message')
    contact=ContactUs(
      name=name,
      email=email,
      message=message
    )
    contact.save()
    send_mail(
      "Got a message from contact form",
      'Hi team ,\n\n we have recieved a message from user,please find the below information\nName:'+name+' \nEmail:'+email+'\nMessage:'+message+'',
      settings.EMAIL_HOST_USER,
      ['dineshtech0208@gmail.com'],
      fail_silently=False)
    send_mail(
      'Thanks for contacting us',
      'Hi'+name+' \n thankyou for submitting.Our team will get in touch with you shortly.\n\nBest Regards \n Dinesh',
      settings.EMAIL_HOST_USER,
      [email],
      fail_silently=False)
    return redirect('index')
  return render(request,'contact.html')
  
def ajax(request):
  if request.method=='POST':
    name=request.POST['name']
    email=request.POST['email']
    bio=request.POST['bio']
    ajax=Ajaxx(
      name=name,
      email=email,
      bio=bio
    )
    ajax.save()
    success='User' + name + 'created successfully'
    return HttpResponse(success)


  return render(request,'ajax.html')