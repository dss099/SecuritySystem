from fastapi import APIRouter, Query, status
from typing import List, Optional
from app.Region.schemas import RegionCreate, RegionUpdate, RegionResponse
from app.Region.services import RegionService

router = APIRouter(prefix="/regions", tags=["regions"])

# ============= 查询操作 =============

@router.get("/", response_model=List[RegionResponse])
async def list_regions(
    skip: int = Query(0, ge=0, description="跳过的记录数"),
    limit: int = Query(100, ge=1, le=1000, description="返回的记录数"),
    name: Optional[str] = Query(None, description="按名称筛选"),
    active_only: bool = Query(False, description="只返回未删除的记录")
):
    """获取区域列表"""
    return await RegionService.list_regions_with_filters(
        skip=skip,
        limit=limit,
        name=name,
        active_only=active_only
    )

@router.get("/search", response_model=List[RegionResponse])
async def search_regions(
    q: str = Query(..., min_length=1, description="搜索关键词"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100)
):
    """搜索区域"""
    return await RegionService.search_regions(q, skip, limit)

@router.get("/stats/count")
async def get_regions_statistics():
    """获取区域统计信息"""
    return await RegionService.get_regions_statistics()

@router.get("/{region_id}", response_model=RegionResponse)
async def get_region(region_id: int):
    """根据ID获取单个区域"""
    return await RegionService.get_region_by_id_or_404(region_id)

# ============= 创建操作 =============

@router.post("/", response_model=RegionResponse, status_code=status.HTTP_201_CREATED)
async def create_region(region_in: RegionCreate):
    """创建新区域"""
    return await RegionService.create_region_with_validation(region_in)

@router.post("/batch")
async def create_regions_batch(regions_in: List[RegionCreate]):
    """批量创建区域"""
    return await RegionService.create_regions_batch(regions_in)

# ============= 更新操作 =============

@router.put("/{region_id}", response_model=RegionResponse)
async def update_region(region_id: int, region_in: RegionUpdate):
    """更新区域"""
    return await RegionService.update_region_with_validation(region_id, region_in)

@router.patch("/{region_id}", response_model=RegionResponse)
async def partial_update_region(region_id: int, region_in: RegionUpdate):
    """部分更新区域"""
    return await RegionService.update_region_with_validation(region_id, region_in)

# ============= 删除操作 =============

@router.delete("/{region_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_region(region_id: int):
    """删除区域"""
    await RegionService.delete_region_with_checks(region_id)

@router.patch("/{region_id}/soft-delete")
async def soft_delete_region(region_id: int):
    """软删除区域"""
    return await RegionService.soft_delete_region(region_id)

@router.patch("/{region_id}/restore")
async def restore_region(region_id: int):
    """恢复软删除的区域"""
    return await RegionService.restore_region(region_id)