from django.core.management.base import BaseCommand, CommandError
from ._private import create_category
from db.data.product_category_data import category_data


class Command(BaseCommand):
    help = "向数据库导入默认测试数据！"

    def add_arguments(self, parser) -> None:

        parser.add_argument(
            '-cate',
            '--category',
            action='store_true',
            help='仅导入商品分类数据！',
        )
    
    def handle(self, *args, **options):
        if options['category']:
            create_category(category_data)
            self.stdout.write(self.style.SUCCESS('只导入分类数据成功！'))