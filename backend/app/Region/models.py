from tortoise import fields
from app.Core.models import CommonFieldsModel

class Region(CommonFieldsModel):
    """
    区域／片区
    """
    # ─────── 属性字段 ───────
    name = fields.CharField(max_length=60, description="区域名称", unique=True)
    note = fields.TextField(null=True, description="备注")

    class Meta:
        table             = "region"
        table_description = "片区"
        ordering          = ["name"]          # 按名称升序，唯一字段自动带索引

    def __str__(self):
        return self.name