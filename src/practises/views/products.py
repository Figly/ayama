from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic

from clients.models import ClientDetail, ClientProduct

from .. import forms, models


class AddProductView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    template_name = "practises/add_product_detail.html"
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
        model.save()

        messages.add_message(
            self.request, messages.SUCCESS, "product successfully edited."
        )
        self.success_url = reverse_lazy("home")
        return super(EditProductView, self).form_valid(form)


class ViewClientProductView(generic.View):
    model = models.ProductDetail

    def test_func(self):
        return (
            self.request.user.is_administrator
            or self.request.user.is_superuser
            or self.request.user.is_advisor
        )

    def get(self, *args, **kwargs):
        template_name = "practises/link_client_product.html"

        if self.request.user.is_administrator and self.request.user.is_advisor:
            client_id = self.kwargs["client_id"]

            practise = self.request.user.Advisor.practise_id_fk

            if client_id is not None:
                client_products = ClientProduct.objects.filter(client_id_fk=client_id)

            client_products_filter = client_products.values_list(
                "product_id_fk", flat=True
            )

            available_products = models.ProductDetail.objects.filter(
                practise_id_fk=practise, is_active=True
            ).exclude(
                id__in=client_products_filter.all()
            )  # can't add same product twice

            context = {
                "products": available_products,
                "client_products": client_products,
                "client_id": client_id,
            }

        elif self.request.user.is_administrator:
            client_id = self.kwargs["client_id"]

            practise = self.request.user.Administrator.practise_id_fk

            if client_id is not None:
                client_products = ClientProduct.objects.filter(client_id_fk=client_id)

            client_products_filter = client_products.values_list(
                "product_id_fk", flat=True
            )

            available_products = models.ProductDetail.objects.filter(
                practise_id_fk=practise, is_active=True
            ).exclude(id__in=client_products_filter.all())

            context = {
                "products": available_products,
                "client_products": client_products,
                "client_id": client_id,
            }
        elif self.request.user.is_advisor:
            client_id = self.kwargs["client_id"]

            practise = self.request.user.Advisor.practise_id_fk

            if client_id is not None:
                client_products = ClientProduct.objects.filter(client_id_fk=client_id)

            client_products_filter = client_products.values_list(
                "product_id_fk", flat=True
            )

            available_products = models.ProductDetail.objects.filter(
                practise_id_fk=practise, is_active=True
            ).exclude(id__in=client_products_filter.all())

            context = {
                "products": available_products,
                "client_products": client_products,
                "client_id": client_id,
            }

        return render(self.request, template_name, context)


def AddClientProductView(request):
    if request.method == "POST":
        client_id = request.POST["client_id_fk"]
        product_id = request.POST["product_id_fk"]

        if client_id is None or product_id is None:
            messages.add_message(
                request, messages.ERROR, "product could not be added to client."
            )
            request.success_url = reverse_lazy("home")
            return HttpResponseRedirect("/")

        try:
            model = ClientProduct()
            client = ClientDetail.objects.get(id=client_id)
            product = models.ProductDetail.objects.get(id=product_id)

            model.client_id_fk = client
            model.product_id_fk = product
            model.modified_by_id = request.user.id

            model.save()
            messages.add_message(request, messages.SUCCESS, "Product added.")
        except Exception as e:
            messages.add_message(request, messages.ERROR, e)
    return redirect("practises:view-client-product", client_id=client_id)

    if request.method == "GET":
        return HttpResponseRedirect("/")
