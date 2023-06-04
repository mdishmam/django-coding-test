from pprint import pprint
from .models import Variant, Product, ProductVariant, ProductVariantPrice

# product = Product.objects.get(title='Vintage Alarm Clock Retro Oil Lamp')
# variants = ProductVariant.objects.filter(product=product)
#
# print(product.title)
# for i in variants:
#     print('\t'+i.variant_title)
#     vp = ProductVariantPrice.objects.filter(product=product, product_variant_one=i)
#
#     for i in vp:
#         print(
#             # f'{i.product.title} - '
#             f'\t\t{i.product_variant_one.variant_title} '
#             f'- {i.product_variant_two.variant_title} -'
#             f' {i.product_variant_three.variant_title} : '
#             f'{i.price}, {i.stock}')

# v1 = variants[0]
# vp = ProductVariantPrice.objects.filter(product=product, product_variant_one=v1)
#
# for i in vp:
#     print(
#         f'{i.product.title} - {i.product_variant_one.variant_title} - {i.product_variant_two.variant_title} - {i.product_variant_three.variant_title} : {i.price}, {i.stock}')


variants = Variant.objects.filter(active=True)

all_variants_out = []
for variant in variants:
    p_variants = ProductVariant.objects.filter(variant=variant).values('variant_title')
    p_variants = [i['variant_title'] for i in p_variants]
    tmp = {
        'varient_name':variant.title,
        'varients':set(p_variants)
    }
    all_variants_out.append(tmp)

print(all_variants_out)