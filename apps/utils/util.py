from datetime import datetime

# 记录最后编辑时间和最后编辑者
def save_time(request, obj, form, change):
    obj.last_editor = request.user.first_name
    obj.modified_date = datetime.now()
    obj.save()


def write_csv(writer: object, field_list, queryset):
    writer.writerow([queryset.model._meta.get_field(
        f).verbose_name.title() for f in field_list], )
    for obj in queryset:
        # 单行 的记录（各个字段的值）， 根据字段对象，从当前实例 (obj) 中获取字段值
        csv_line_values = []
        for field in field_list:
            field_object = queryset.model._meta.get_field(field)
            field_value = field_object.value_from_object(obj)
            csv_line_values.append(field_value)
        writer.writerow(csv_line_values)



