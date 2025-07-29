from app.Region.models import Region

# ============= 基础CRUD操作 =============

async def create_region(**kwargs):
    return await Region.create(**kwargs)

async def get_region_by_id(region_id: int):
    return await Region.get_or_none(pk_id=region_id)

async def get_region_by_name(name: str):
    return await Region.get_or_none(name=name)

async def list_regions():
    return await Region.all()

async def list_regions_paginated(skip: int = 0, limit: int = 100):
    return await Region.all().offset(skip).limit(limit)

async def update_region(region_id: int, **kwargs):
    region = await Region.get_or_none(pk_id=region_id)
    if region:
        for k, v in kwargs.items():
            setattr(region, k, v)
        await region.save()
    return region

async def delete_region(region_id: int):
    region = await Region.get_or_none(pk_id=region_id)
    if region:
        await region.delete()
    return region

# ============= 查询和过滤 =============

async def get_regions_by_name_filter(name_filter: str):
    return await Region.filter(name__icontains=name_filter)

async def get_active_regions():
    return await Region.filter(is_deleted=False)

async def search_regions(keyword: str):
    return await Region.filter(
        Region.name.icontains(keyword) |
        Region.note.icontains(keyword)
    )

# ============= 统计功能 =============

async def count_regions():
    return await Region.all().count()

async def count_active_regions():
    return await Region.filter(is_deleted=False).count()

async def count_deleted_regions():
    return await Region.filter(is_deleted=True).count()

# ============= 验证功能 =============

async def check_region_name_exists(name: str, exclude_id: int = None):
    query = Region.filter(name=name, is_deleted=False)
    if exclude_id:
        query = query.exclude(pk_id=exclude_id)
    return await query.exists()

# ============= 批量操作 =============

async def bulk_create_regions(regions_data: list):
    return await Region.bulk_create([Region(**data) for data in regions_data])

async def bulk_delete_regions(region_ids: list):
    return await Region.filter(pk_id__in=region_ids).delete()