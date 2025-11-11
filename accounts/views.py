from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from sidebar.models import LogHistory  # ✅ Import the LogHistory model

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # ✅ Create a log entry for successful login
            LogHistory.objects.create(
                staff=user,
                action_taken="LOGIN"
            )

            return redirect('home')  # Redirect to home.html after login
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'accounts/login.html')


def logout_view(request):
    # ✅ Optional: log the logout action as well
    if request.user.is_authenticated:
        LogHistory.objects.create(
            staff=request.user,
            action_taken="LOGOUT"
        )

    logout(request)
    return redirect('login')  # Redirect back to login after logout
