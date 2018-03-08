from django.shortcuts import render
from .forms import UserForm , UserProfileForm , LoginForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout

# Create your views here.


def register(request):
	#set False defaultly to judge whether the register is successful
	registered = 'False'
	if request.method == 'POST':
		user_form = UserForm(request.POST)
		profile_form = UserProfileForm(request.POST)
		username = request.POST.get('username')
		password = request.POST.get('password')

		if user_form.is_valid() and profile_form.is_valid():
			#save User
			user = user_form.save()
			#hash the password with the set_password method.
			user.set_password(user.password)
			user.save()

			#save Profile
			#set commit=False. This delays saving the model until ready to avoid integrity problems.
			profile = profile_form.save(commit = False)
			profile.user = user
			#save picture
			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']
			profile.save()
			
			registered = 'True'
			user = authenticate(username=username,password=password)
			login(request,user)
			context = {
			'user' : user
			}
			return render(request, 'blog/index.html' , context=context)
			
		else:
			#invalid forms
			context = {
					'user_form': user_form,
					'profile_form': profile_form,
					'registered': registered
		}
			return render(request , 'account/register.html' , context = context)
	else:
		# not a http post
		user_form = UserForm()
		profile_form = UserProfileForm()
		context = {
					'user_form': user_form,
					'profile_form': profile_form,
					'registered': registered
		}
		return render(request, 'account/register.html' , context = context)

def log_in(request):
	nowstatus = True
	username = None
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

	# use django's authenticate function to confirm the account
		user = authenticate(username=username,password=password)

	#if confirm , return a User object , if not , return None
		if user:
			if user is not None:
				login(request,user)
				context = {
				'user' : user
				}
				return render(request, 'blog/index.html' , context=context)
			else:
				#disabled account
				nowstatus = 'disabled'
				context={
				'nowstatus': nowstatus
				}
				return render(request, 'account/login.html' , context=context)
		else:
			nowstatus = 'error password'
			context = {
			'nowstatus' : nowstatus
			}
			return render(request , 'account/login.html' , context=context)

	else:
		login_form = LoginForm()
		context = {
		'login_form' : login_form,
		}
		return render(request , 'account/login.html' , context = context)

def log_out(request):
	logout(request)
	return render(request , 'blog/index.html' )





