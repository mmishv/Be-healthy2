from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.forms import formset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, CreateView

from recipes.models import Product
from .forms import CalculatorForm, MixerProductFormSet, MixerProductForm, CreateArticleForm
from .models import Article


def get_article_page(request):
    articles = Article.objects.filter(moderated=True)
    paginator = Paginator(articles, 3)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return page


def index(request):
    form = CalculatorForm(request.GET)
    result = 0
    if form.is_valid():
        sex = request.GET['sex']
        weight = request.GET['weight']
        height = request.GET['height']
        age = request.GET['age']
        activity = request.GET['activity']
        goal = request.GET['goal']
        result = 447.6 + 9.2 * float(weight) + 3.1 * float(height) - 4.3 * float(age) if sex == 'F' else \
            88.36 + 13.4 * float(weight) + 4.8 * float(height) - 5.7 * float(age)
        result *= float(activity) * float(goal)
        result = int(result)
    return render(request, 'main/main.html', {
        'form': CalculatorForm(request.GET),
        'result': result,
        'page': get_article_page(request),
    })


class FullArticleView(DetailView):
    model = Article
    template_name = 'main/article_detail.html'
    context_object_name = 'article'


def product_base(request):
    return render(request, 'main/products.html', {
        'products': Product.objects.all(),
        'mixer_formset': MixerProductFormSet(prefix='product_amount')
    })


class MixerFormSetView(View):
    formset_class = formset_factory(MixerProductForm, extra=1)
    template_name = 'main/mixer.html'

    def get(self, request):
        formset = self.formset_class(request.GET, prefix='product_amount')
        products = []
        total = {'k': 0, 'b': 0, 'j': 0, 'u': 0}
        weight = 0
        if formset.is_valid():
            for form in formset:
                product = form.cleaned_data['product']
                unit = form.cleaned_data['unit']
                quantity = form.cleaned_data['quantity']
                weight += quantity
                per_100 = lambda x: round(quantity * x / 100, 1)
                products.append({'product': product, 'unit': unit, 'quantity': quantity,
                                 'kbju': {'k': per_100(product.calories), 'b': per_100(product.proteins),
                                          'j': per_100(product.fats), 'u': per_100(product.carbohydrates)}})
                for k, v in total.items():
                    total[k] = v + products[-1]['kbju'][k]
            total['weight'] = weight
            return render(request, self.template_name, {'ingredients': products, 'total': total})

        return render(request, 'main/products.html', {'mixer_formset': formset})


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    template_name = 'main/create_article.html'
    form_class = CreateArticleForm
    success_url = reverse_lazy('my articles')

    def post(self, request, *args, **kwargs):
        form = CreateArticleForm(request.POST)
        if form.is_valid():
            return self.form_valid(form, request.user)
        else:
            return HttpResponseRedirect(self.get_success_url())

    def form_valid(self, form, user):
        self.object = form.save(commit=False)
        self.object.author = user
        self.object.save()
        form.save_m2m()
        return HttpResponseRedirect(self.get_success_url())
