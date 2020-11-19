from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


class Product(models.Model):
    category = models.ForeignKey("Category", on_delete=models.CASCADE, null=True, blank=True,
                                 verbose_name=_("Category"))
    name = models.CharField(_("Title"), max_length=128)
    slug = models.SlugField(_("Slug"), db_index=True, unique=True)
    description = models.TextField(_("discription"))
    create_at = models.DateTimeField(_("Create at"), auto_now_add=True)
    update_at = models.DateTimeField(_("Update at"), auto_now=True)
    price = models.FloatField(_("price"))

    image = models.ImageField(_("image"), upload_to='post/images')

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self):
        return self.name


class SellProduct(models.Model):
    order = models.ForeignKey("Sell", on_delete=models.CASCADE)
    number = models.SmallIntegerField()
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Sellproduct")
        verbose_name_plural = _("Sellproducts")


class Sell(models.Model):
    create_at = models.DateTimeField(_("Create at"), auto_now_add=True)
    buyer = models.ForeignKey(User, verbose_name=_(
        "buyer"), on_delete=models.CASCADE)
    dicount_id = models.ForeignKey("Discount", verbose_name=_("buyer"), on_delete=models.CASCADE,
                                   null=True, blank=True)
    products = models.ManyToManyField(Product, verbose_name=_("product"), through=SellProduct
                                      )

    class Meta:
        verbose_name = _("Sells")
        verbose_name_plural = _("Sells")


class Comment(models.Model):
    content = models.TextField(_("Content"))
    product = models.ForeignKey(Product, verbose_name=_(
        "Post"), on_delete=models.CASCADE)
    create_at = models.DateTimeField(_("Create at"), auto_now_add=True)
    update_at = models.DateTimeField(_("Update at"), auto_now=True)
    author = models.ForeignKey(User, verbose_name=_(
        "Author"), on_delete=models.CASCADE)
    is_confirmed = models.BooleanField(_("confirm"), default=True)

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    def __str__(self):
        return self.product.name


class Category(models.Model):
    title = models.CharField(_("title"), max_length=50)
    slug = models.SlugField(_("Slug"), unique=True, db_index=True)
    parent = models.ForeignKey('self', verbose_name=_("parent"), on_delete=models.SET_NULL,
                               null=True, blank=True,
                               related_query_name="childrens", related_name="childrens")

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Category")


class Discount(models.Model):
    code = models.SmallIntegerField()
    minimum_order = models.FloatField(null=True, blank=True)
    maximum_order = models.FloatField(null=True, blank=True)
    percentage = models.SmallIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    count = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = _("Discount")
        verbose_name_plural = _("Discounts")
