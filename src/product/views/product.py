import json
from datetime import datetime

from django.http import JsonResponse
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from pprint import pprint
from product.models import Variant, Product, ProductVariant, ProductVariantPrice


class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        product_data = json.loads(request.body.decode('utf-8'))
        new_product = Product()
        new_product.title = product_data.get('title')
        new_product.sku = product_data.get('sku')
        new_product.description = product_data.get('description')
        new_product.save()

        all_variants = Variant.objects.filter(active=True)

        for row in product_data.get('table_data'):
            variants = row.get('column1').split('/')
            product_varients = [None, None, None]
            for index, variant in enumerate(variants):
                if variant.strip() == '':
                    continue
                new_product_varient = ProductVariant()
                new_product_varient.variant_title = variant
                new_product_varient.variant = all_variants[index]
                new_product_varient.product = new_product
                new_product_varient.save()
                product_varients[index] = new_product_varient
                # ProductVariant.objects.create(
                #     variant_title = variant,
                #     variant = all_variants[index],
                #     product = new_product
                # )
            ProductVariantPrice.objects.create(
                product_variant_one = product_varients[0],
                product_variant_two = product_varients[1],
                product_variant_three = product_varients[2],
                price = row.get('column2'),
                stock = row.get('column3'),
                product = new_product
            )


        # print(product_data)
        print(product_data.get('table_data'))
        return JsonResponse({'Message': 'Saved'}, status=201)


    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context


class ProductListingView(generic.ListView):
    template_name =  'products/list.html'
    model = Product

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['products'] = list(Product.objects.all().values('title', 'description', 'created_at'))
    #     context['request'] = ''
    #     if self.request.GET:
    #         context['request'] = self.request.GET['title__icontains']
    #     return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        variant_searched, variant_type = None, None
        price_from, price_to = None, None
        products = Product.objects.all()
        if self.request.GET:
            print(self.request.GET)
            title_searched = self.request.GET.get('title')
            variant_searched = self.request.GET.get('variant')
            price_from = self.request.GET.get('price_from')
            price_to = self.request.GET.get('price_to')
            date = self.request.GET.get('date')

            if title_searched is not None:
                products = Product.objects.filter(title__icontains=title_searched)
            if date is not None or date != '':
                try:
                    date_object = datetime.strptime(date, "%Y-%m-%d")
                    products = products.filter(created_at__gte=date_object)
                except ValueError:
                    pass

        page_no = 1
        total_products = products.count()
        total_pages = total_products // 10 + 1

        data = []


        for product in products:
            product_data = {
                'id': product.id,
                'title': product.title,
                'description': product.description,
                'created_at':product.created_at,
                'variants': []
            }

            variants = ProductVariant.objects.filter(product=product)

            if variant_searched != None:
                try:
                    variant_type, variant_title = variant_searched.split('@@')
                    variants = variants.filter(product=product, variant_title=variant_title)
                except:
                    pass

            for variant in variants:
                if variant_type == 'Size':
                    variant_prices = ProductVariantPrice.objects.filter(product=product, product_variant_one=variant)
                elif variant_type == 'Color':
                    variant_prices = ProductVariantPrice.objects.filter(product=product, product_variant_two=variant)
                elif variant_type == 'Style':
                    variant_prices = ProductVariantPrice.objects.filter(product=product, product_variant_three=variant)
                else:
                    variant_prices = ProductVariantPrice.objects.filter(product=product, product_variant_one=variant)
                # print(f'"here {price_from}", "{price_to}"')
                if price_from is not None or price_from != '':
                    try:
                        variant_prices = variant_prices.filter(price__gte=float(price_from))
                    except:
                        pass
                if price_to is not None or price_from != '':
                    try:
                        variant_prices = variant_prices.filter(price__lte=float(price_to))
                    except:
                        pass


                for variant_price in variant_prices:
                    if variant_price == None:
                        continue
                    # varient_title = f'{variant_price.product_variant_one.variant_title} - ' \
                    #                 f'{variant_price.product_variant_two.variant_title} - ' \
                    #                 f'{variant_price.product_variant_three.variant_title}'
                    product_data['variants'].append({
                        # 'variant_title': variant.variant_title,
                        'variant_title': variant_price.return_combined_variant,
                        'price': variant_price.price,

                        'stock': variant_price.stock
                    })
            # if len(product_data.get('variants')) == 0:
            #     continue
            data.append(product_data)
        # pprint(data)

        no_of_data_sent = data.__len__()

        context['products'] = data
        context['page_no'] = page_no
        context['no_of_data_sent'] = no_of_data_sent
        context['total_products'] = total_products
        context['total_pages'] = range(1,total_pages+1)

        # variants = Variant.objects.filter(active=True).values('id', 'title')
        variants = Variant.objects.filter(active=True)

        all_variants_out = []
        for variant in variants:
            p_variants = ProductVariant.objects.filter(variant=variant).values('variant_title')
            p_variants = [i['variant_title'] for i in p_variants]
            tmp = {
                'varient_name': variant.title,
                'varients': set(p_variants)
            }
            all_variants_out.append(tmp)

        # context['variants'] = list(variants.all())
        context['variants'] = all_variants_out
        #     context['request'] = ''
        #     if self.request.GET:
        #         context['request'] = self.request.GET['title__icontains']
        return context


class EditProductView(generic.TemplateView):
    template_name = 'products/edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_id = self.request.GET.get('product_id')
        edit_product = Product.objects.get(id=product_id)

        context['product_name'] = edit_product.title
        context['product_sku'] = edit_product.sku
        context['product_description'] = edit_product.description

        price_variants = ProductVariantPrice.objects.filter(product__id=product_id)
        context['product_price_variants'] = list(price_variants)


        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context