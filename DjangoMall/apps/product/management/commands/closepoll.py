from django.core.management.base import BaseCommand, CommandError
from product.models import DJMallProductCategory as Product


class Command(BaseCommand):
    help = "导入测试数据"

    def add_arguments(self, parser) -> None:

        parser.add_argument('cate_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        for cate_id in options['cate_ids']:
            try:
                cate = Product.objects.get(pk=cate_id)
            except Product.DoesNotExist:
                raise CommandError('Product "%s" does not exist' % cate_id)

            cate.is_nav = True
            cate.save()

            self.stdout.write(self.style.SUCCESS('Successfully closed product "%s"' % cate_id))
