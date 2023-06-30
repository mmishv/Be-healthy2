import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from datetime import datetime as dt, time

from django.urls import reverse
from django.views.generic import CreateView, DeleteView

from diary.forms import CreateMealForm, MealProductFormSet
from diary.models import Meal
from userprofile.models import Profile


@login_required
def get_current_page(request):
    return get_diary_page(request, f'{datetime.date.today()}')


@login_required
def get_page_by_date(request, year, month, day):
    return get_diary_page(request, f'{year}-{month}-{day}')


def get_diary_page(request, date):
    page_date = dt.strptime(date, "%Y-%m-%d").date()
    start_time = dt.combine(page_date, time.min)
    end_time = dt.combine(page_date, time.max)
    year, month, day = date.split('-')
    return render(request, 'diary/diary.html', {
        'profile': Profile.objects.get(user=request.user),
        'meals': Meal.objects.filter(user=request.user, date__range=(start_time, end_time)),
        'total': Meal.get_daily_total(request.user, page_date),
        'date': {'full_date': date, 'year': year, 'month': month, 'day': day},
        'create_form': CreateMealForm(),
        'create_formset': MealProductFormSet(),
    })


class MealCreateView(LoginRequiredMixin, CreateView):
    model = Meal
    template_name = 'diary/diary.html'
    form_class = CreateMealForm

    def post(self, request, *args, **kwargs):
        self.object = None
        form = CreateMealForm(request.POST, request.FILES)
        formset = MealProductFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset, request.user)
        else:
            return self.form_invalid(form, formset)

    def form_valid(self, form, formset, user):
        self.object = form.save(commit=False)
        self.object.user = user

        year, month, day = self.kwargs['year'], self.kwargs['month'], self.kwargs['day']
        date_string = f'{year}-{month}-{day}'
        date = dt.strptime(date_string, '%Y-%m-%d')
        self.object.date = date

        self.object.save()
        form.save_m2m()

        formset.instance = self.object
        formset.instance.user = self.request.user
        formset.save()

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, formset):
        return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def get_success_url(self):
        year = self.kwargs['year']
        month = str(self.kwargs['month']).zfill(2)
        day = str(self.kwargs['day']).zfill(2)
        success_url = reverse('diary', kwargs={'year': year, 'month': month, 'day': day})

        return success_url


class MealDeleteView(DeleteView):
    model = Meal

    def get_object(self, queryset=None):
        meal = get_object_or_404(Meal, id=self.kwargs['id'])
        return meal

    def get_success_url(self):
        return reverse('diary', kwargs={'year': self.kwargs['year'], 'month': str(self.kwargs['month']).zfill(2),
                                        'day': str(self.kwargs['day']).zfill(2)})
