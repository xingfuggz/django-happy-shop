from django import template
from django.utils.html import format_html
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def get_breadcrumb(request, cate=None, product=None):
    # 面包屑
    breadcrumb = None

    if request.path_info == '/product/category_list/':
        h = '''
            <li><a href="/product/category_list/"><span>全部分类</span></a></li>
        '''
        breadcrumb = format_html(h)
    elif cate is not None and cate.parent:
        h = '''
            <li><a href="/product/category/{}/"><span>{}</span></a></li>
            <li><a href="/product/category/{}/"><span>{}</span></a></li>
        '''
        if product is not None and product.id:
            h += '<li class="is-active"><a href="/product/goods/{}/detail/"><span>{}</span></a></li>'
            breadcrumb = format_html(
                h, cate.parent.id, cate.parent.name, cate.id, 
                cate.name, product.id, product.title
            )
        else:
            breadcrumb = format_html(h, cate.parent.id, cate.parent.name, cate.id, cate.name)
    elif cate is not None and not cate.parent:
        h = '''
            <li class="is-active"><a href="/product/category/{}/"><span>{}</span></a></li>
        '''
        breadcrumb = format_html(h, cate.id, cate.name)
    elif '/personal/' in request.path_info:
        h = '''
            <li><a href="/personal/home/"><span>个人中心</span></a></li>
        '''
        breadcrumb = format_html(h)
    return breadcrumb
        