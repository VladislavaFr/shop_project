from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .models import Product

# Список всех продуктов
class ProductListView(ListView):
    model = Product
    template_name = "catalog/product_list.html"
    context_object_name = "products"

# Создание продукта
class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    fields = ["name", "description", "price", "image"]
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("product_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.status = "draft"
        return super().form_valid(form)

# Миксин для проверки прав владельца или модератора
class OwnerOrModeratorMixin(UserPassesTestMixin):
    def test_func(self):
        product = self.get_object()
        user = self.request.user

        if product.owner == user:
            return True

        if user.groups.filter(name="Модератор продуктов").exists():
            return True

        return False

# Редактирование продукта
class ProductUpdateView(LoginRequiredMixin, OwnerOrModeratorMixin, UpdateView):
    model = Product
    fields = ["name", "description", "price", "image", "status"]
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("product_list")

# Удаление продукта
class ProductDeleteView(LoginRequiredMixin, OwnerOrModeratorMixin, DeleteView):
    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy("product_list")
