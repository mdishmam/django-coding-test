from django.db import models
from config.g_model import TimeStampMixin


# Create your models here.
class Variant(TimeStampMixin):
    title = models.CharField(max_length=40, unique=True)
    description = models.TextField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Product(TimeStampMixin):
    title = models.CharField(max_length=255)
    sku = models.SlugField(max_length=255, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class ProductImage(TimeStampMixin):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    file_path = models.URLField()


class ProductVariant(TimeStampMixin):
    variant_title = models.CharField(max_length=255)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.product.title} - {self.variant_title}'


class ProductVariantPrice(TimeStampMixin):
    product_variant_one = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, null=True,
                                            related_name='product_variant_one')
    product_variant_two = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, null=True,
                                            related_name='product_variant_two')
    product_variant_three = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, null=True,
                                              related_name='product_variant_three')
    price = models.FloatField()
    stock = models.FloatField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.product.title}'

    @property
    def return_combined_variant(self):
        out = ''
        if self.product_variant_one is not None:
            out += self.product_variant_one.variant_title
        if self.product_variant_two is not None:
            out += f' - {self.product_variant_two.variant_title}'
        if self.product_variant_three is not None:
            out += f' - {self.product_variant_three.variant_title}'
        return out

    @property
    def return_combined_variant_slash_sep(self):
        out = ''
        if self.product_variant_one is not None:
            out += f'{self.product_variant_one.variant_title}/'
        if self.product_variant_two is not None:
            out += f'{self.product_variant_two.variant_title}/'
        if self.product_variant_three is not None:
            out += f'{self.product_variant_three.variant_title}/'
        return out
