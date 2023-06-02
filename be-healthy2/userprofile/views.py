from django.shortcuts import render


def auth(request):
    # if request.method == 'POST':
    #     form = RegisterForm(request.POST)
    #     if form.is_valid():
    #         login(request, form.save())
    #         return redirect('/')
    return render(request, 'userprofile/auth.html', {
        # 'reg_form': RegisterForm(request.POST),
        # 'log_form': LoginForm(request.GET),
    })
