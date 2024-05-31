from django.shortcuts import render
from django.http import JsonResponse
from django.core.mail import send_mail, EmailMessage
from app.models import *
from dotenv import load_dotenv
import os

from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# Create your views here.
from django.contrib.auth.decorators import login_required

# Load environment variables from .env file
load_dotenv()

@login_required
def home_page(request):
    all_blogs = BlogPost.objects.all()[:6]  
    travel_blog = BlogPost.objects.filter(tags__name="Travel")[:4]
    culture_blog = BlogPost.objects.filter(tags__name="Culture")[:4]


    return render(request, 'home_page.html', {'all_blogs': all_blogs ,'travel_blog':travel_blog, 'culture_blog':culture_blog})

def login_page(request):
    if request.method == 'POST':
        try:
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(request, username=email, password=password)
            
            if user is not None:
                login(request, user)
                return JsonResponse({'success': True, 'redirect_url': 'home'})
            else:
                return JsonResponse({'message': 'Invalid email or password'})
        
        except Exception as e:
         
            print(f'Error during login: {e}')
            return JsonResponse({'message': 'An error occurred. Please try again later.'})

    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')

        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        print(name,email,password)

        if CustomUser.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Email is already in use.'})

        user = CustomUser.objects.create_user(email=email, password=password, name=name)
        return JsonResponse({'success': True})
    return render(request,'register.html')


@login_required
def all_blogs(request):
    tag_name = request.GET.get("tag")
    page = request.GET.get('page', 1)

    if tag_name:
        filtered_blogs = BlogPost.objects.filter(tags__name__iexact=tag_name)
    else:
        filtered_blogs = BlogPost.objects.all()

    paginator = Paginator(filtered_blogs, 5)
    
    try:
        all_cat_blogs = paginator.page(page)
    except PageNotAnInteger:
        all_cat_blogs = paginator.page(1)
    except EmptyPage:
        all_cat_blogs = paginator.page(paginator.num_pages)

    if request.method=="GET" and "tag" in request.GET:
        all_data = list(all_cat_blogs.object_list.values())
        data = {
            "filtered_blogs": all_data,
            "has_other_pages": all_cat_blogs.has_other_pages(),
            "has_previous": all_cat_blogs.has_previous(),
            "previous_page_number": all_cat_blogs.previous_page_number() if all_cat_blogs.has_previous() else None,
            "has_next": all_cat_blogs.has_next(),
            "next_page_number": all_cat_blogs.next_page_number() if all_cat_blogs.has_next() else None,
            "num_pages": paginator.num_pages,
            "current_page": all_cat_blogs.number,
        }
        return JsonResponse(data)

    all_tags = Tag.objects.all()
    return render(request, 'all_blogs.html', {"all_cat_blogs": all_cat_blogs, "all_tags": all_tags, "tag_name": tag_name})



def show_blog(request, id):
    blog_post = BlogPost.objects.get(id=int(id))
    comments = blog_post.comments.all()
    return render(request, 'blog_detail.html', {'blog_post': blog_post,'comments': comments})

def save_comment(request):
    if request.method =="POST":
        text = request.POST.get('text')
        blog_post_id = request.POST.get('blog_post_id')
        author = request.user if request.user.is_authenticated else None
        try:
            comment = Comment.objects.create(
                blog_post_id=blog_post_id,
                author=author,
                text=text
            )

            return JsonResponse({'success': True, 'comment': {'text': comment.text}, 'message': 'Comment saved successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'error_message': str(e)})
    else:
        return JsonResponse({'success': False, 'error_message': 'Invalid request'})


def share_blog_post(request, pk):
    blog_post = get_object_or_404(BlogPost, pk=int(pk))

    if request.method == 'POST':
        email = request.POST.get('email')
        print(email)
        message = request.POST.get('message')
        subject = f"{request.user} shared a blog post with you: {blog_post.title}"
      
        sender =  os.environ.get('EMAIL_HOST_USER')
        smtp_server = os.environ.get('EMAIL_HOST')
        port = int(os.getenv('EMAIL_PORT', 587))
        sender_email = os.environ.get('EMAIL_HOST_USER')
        password =  os.getenv('EMAIL_HOST_PASSWORD')
      
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

# Send the email
        try:
            with smtplib.SMTP_SSL(smtp_server, port) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, email, msg.as_string())
                return JsonResponse({'success': True})
            print("Email sent successfully.")
        except Exception as e:
            print(f"Error: {e}")
        
            return JsonResponse({'success': False, 'error_message': str(e)})
       