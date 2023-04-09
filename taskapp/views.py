from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views import generic, View
from django.http import Http404, HttpResponseRedirect
from braces.views import SelectRelatedMixin
from django.shortcuts import get_object_or_404, redirect

from . import models
from . import forms

User = get_user_model()

# Create your views here.
class ListItems(LoginRequiredMixin, generic.ListView):
    model = models.Item
    template_name = 'taskapp/items.html'
    context_object_name = 'item_user'

    def post(self, *args, **kwargs):
        return self.get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ListItems, self).get_context_data(**kwargs)
        if 'FilterForm' not in context:
                context['form'] = forms.FilterForm()
        return context

    def get_queryset(self, *args, **kwargs):
        form = forms.FilterForm(self.request.POST)
        if form.is_valid():
            date_sort = form.cleaned_data['date_sort']
            category_sort = form.cleaned_data['category_sort']
            completed_sort = form.cleaned_data['completed_sort']

            data = super().get_queryset(*args, **kwargs).filter(user=self.request.user)

            if date_sort == "1":
                data = super().get_queryset(*args, **kwargs).filter(user=self.request.user).order_by("due_date")
            elif date_sort == "2":
                data = super().get_queryset(*args, **kwargs).filter(user=self.request.user).order_by("-due_date")

            if category_sort != None:
                data = data.filter(category=category_sort.id)

            if completed_sort != "1":
                if completed_sort == "2":
                    data = data.filter(status=True)
                elif completed_sort == "3":
                    data = data.filter(status=False)

            return data

        else:
            return super().get_queryset(*args, **kwargs).filter(user=self.request.user).order_by("due_date")

class CreateCategory(LoginRequiredMixin, SelectRelatedMixin, generic.CreateView):
    model = models.Category
    form_class = forms.CategoryForm
    template_name = 'taskapp/add_category.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('taskapp:add_item')

class CreateItem(LoginRequiredMixin, SelectRelatedMixin, generic.CreateView):
    model = models.Item
    form_class = forms.ItemAddForm
    template_name = 'taskapp/add_item.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.status = False
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('taskapp:items')

@login_required
def EditItem(request, pk):
    obj = get_object_or_404(models.Item, pk=pk)
    obj.status = True
    obj.save()
    return redirect('taskapp:items')

class DeleteItem(LoginRequiredMixin, generic.DeleteView):
    model = models.Item

    def get_success_url(self):
        return reverse_lazy('taskapp:items')

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(user = self.request.user)

    def delete(self, *args, **kwargs):
        messages.success(self.request, 'Item Deleted')
        return super().delete(*args, **kwargs)
