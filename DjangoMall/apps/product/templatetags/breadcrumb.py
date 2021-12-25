from django import template
from django.utils.html import format_html
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def get_breadcrumb(request, cate=None):
    breadcrumb = None

    if request.path_info == '/product/category_list/':
        h = '''
            <li><a href="/product/category_list/"><span>全部分类</span></a></li>
        '''
        breadcrumb = format_html(h)
    elif cate.parent:
        h = '''
            <li><a href="/product/category/{}/"><span>{}</span></a></li>
            <li><a href="/product/category/{}/"><span>{}</span></a></li>
        '''
        breadcrumb = format_html(h, cate.parent.id, cate.parent.name, cate.id, cate.name)
    elif cate.parent == 'None':
        h = '''
            <li><a href="/product/category/{}/"><span>{}</span></a></li>
        '''
        breadcrumb = format_html(h, cate.id, cate.name)
    return breadcrumb
        