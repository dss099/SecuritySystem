from tortoise import fields
from tortoise.models import Model

class CommonFieldsModel(Model):
    pk_id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    created_by = fields.IntField(null=True)
    last_modified_at = fields.DatetimeField(auto_now=True)
    last_modified_by = fields.IntField(null=True)
    is_deleted = fields.BooleanField(default=False, db_index=True)

    class Meta:
        abstract = True

    @classmethod
    def active(cls):
        return cls.filter(is_deleted=False)

    async def delete(self, *, using_db=None, force=False):
        if force:
            await super().delete(using_db=using_db)
        else:
            self.is_deleted = True
            await self.save(update_fields=["is_deleted"], using_db=using_db)