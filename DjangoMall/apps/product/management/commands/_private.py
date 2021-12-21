from product.models import DJMallProductCategory

def create_category(category_data):
    for data_dict in category_data:
        cate_obj = DJMallProductCategory()
        cate_obj.id = data_dict.get('id')
        cate_obj.name = data_dict.get('name')
        cate_obj.desc = data_dict.get('desc')
        cate_obj.pc_img = data_dict.get('pc_img')
        cate_obj.is_nav = data_dict.get('is_nav')
        cate_obj.save()

        for sub_cate in data_dict['sub_category']:
            sub_cate_obj = DJMallProductCategory()
            sub_cate_obj.id = sub_cate.get('id')
            sub_cate_obj.name = sub_cate.get('name')
            sub_cate_obj.is_nav = sub_cate.get('is_nav')
            sub_cate_obj.icon = sub_cate.get('icon')
            sub_cate_obj.parent = cate_obj
            sub_cate_obj.save()