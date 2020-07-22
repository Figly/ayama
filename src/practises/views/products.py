from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http.response import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic

from .. import forms, models


class AddProductView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    template_name = "practises/add_product_detail.html"
    form_class = forms.AddPrductDetailForm
    model = models.ProductDetail

    def test_func(self):
        return self.request.user.is_administrator or self.request.user.is_superuser

    def form_valid(self, form):
        model = form.save(commit=False)
        model.modified_by = self.request.user
        model.practise_id_fk = self.request.user.Administrator.practise_id_fk
        model.save()

        messages.add_message(
            self.request, messages.SUCCESS, "product successfully added."
        )
        self.success_url = reverse_lazy("home")

        return super(AddProductView, self).form_valid(form)


class ProductlistView(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    template_name = "practises/product_list.html"
    model = models.ProductDetail

    def test_func(self):
        return self.request.user.is_administrator or self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super(ProductlistView, self).get_context_data(**kwargs)

        practise = self.request.user.Administrator.practise_id_fk
        products = models.ProductDetail.objects.filter(practise_id_fk=practise)

        context = {"products": products}

        return context


class EditProductView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    template_name = "practises/edit_product_detail.html"
    model = models.ProductDetail
    fields = (
        "product_type",
        "product_name",
        "product_company",
        "is_active",
    )

    def test_func(self):
        return self.request.user.is_administrator or self.request.user.is_superuser

    def form_valid(self, form):
        if "cancel" in self.request.POST:
            url = reverse_lazy("home")
            return HttpResponseRedirect(url)

        model = form.save(commit=False)
        model.modified_by = self.request.user
        model.save

        messages.add_message(
            self.request, messages.SUCCESS, "product successfully edited."
        )
        self.success_url = reverse_lazy("home")
        return super(EditProductView, self).form_valid(form)


class LinkClientProductView(generic.View):
    template_name = "practises/link_client_product.html"
    model = models.ProductDetail

    def test_func(self):
        return (
            self.request.user.is_administrator
            or self.request.user.is_superuser
            or self.request.user.is_advisor
        )

    def get(self, *args, **kwargs):

        if self.request.user.is_administrator and self.request.user.is_advisor:
            practise = self.request.user.Advisor.practise_id_fk
            products = models.ProductDetail.objects.filter(practise_id_fk=practise)
            context = {"products": products}

        elif self.request.user.is_administrator:
            practise = self.request.user.Administrator.practise_id_fk
            products = models.ProductDetail.objects.filter(practise_id_fk=practise)
            context = {"products": products}
        elif self.request.user.is_advisor:
            practise = self.request.user.Advisor.practise_id_fk
            products = models.ProductDetail.objects.filter(practise_id_fk=practise)
            context = {"products": products}

        return context

    def form_valid(self, form):
        if "cancel" in self.request.POST:
            url = reverse_lazy("home")
            return HttpResponseRedirect(url)

        model = form.save(commit=False)
        model.modified_by = self.request.user
        model.save

        messages.add_message(
            self.request, messages.SUCCESS, "product successfully edited."
        )
        self.success_url = reverse_lazy("home")
        return super(LinkClientProductView, self).form_valid(form)
