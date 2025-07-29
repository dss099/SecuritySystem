from fastapi import HTTPException, status
from typing import List, Optional
from datetime import datetime
from app.Region import crud
from app.Region.schemas import RegionCreate, RegionUpdate, RegionResponse


class RegionService:

    # ============= 查询业务逻辑 =============

    @staticmethod
    async def get_region_by_id_or_404(region_id: int) -> RegionResponse:
        """获取区域，不存在则抛出404异常"""
        region = await crud.get_region_by_id(region_id)
        if not region:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Region with id {region_id} not found"
            )
        return region

    @staticmethod
    async def list_regions_with_filters(
            skip: int = 0,
            limit: int = 100,
            name: Optional[str] = None,
            active_only: bool = False
    ) -> List[RegionResponse]:
        """带过滤条件的区域列表查询"""
        if name:
            regions = await crud.get_regions_by_name_filter(name)
        elif active_only:
            regions = await crud.get_active_regions()
        else:
            regions = await crud.list_regions()

        # 应用分页
        return regions[skip:skip + limit]

    @staticmethod
    async def search_regions(
            keyword: str,
            skip: int = 0,
            limit: int = 50
    ) -> List[RegionResponse]:
        """搜索区域"""
        regions = await crud.search_regions(keyword)
        return regions[skip:skip + limit]

    # ============= 创建业务逻辑 =============

    @staticmethod
    async def create_region_with_validation(region_data: RegionCreate) -> RegionResponse:
        """创建区域，包含业务验证"""
        # 规范化名称
        normalized_name = region_data.name.strip().title()

        # 检查名称是否已存在
        if await crud.check_region_name_exists(normalized_name):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Region name '{normalized_name}' already exists"
            )

        # 创建区域
        create_data = region_data.dict()
        create_data['name'] = normalized_name

        try:
            return await crud.create_region(**create_data)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create region"
            )

    # ============= 更新业务逻辑 =============

    @staticmethod
    async def update_region_with_validation(
            region_id: int,
            region_data: RegionUpdate
    ) -> RegionResponse:
        """更新区域，包含业务验证"""
        # 检查区域是否存在
        await RegionService.get_region_by_id_or_404(region_id)

        update_data = region_data.dict(exclude_unset=True)
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields provided for update"
            )

        # 如果更新名称，检查重复
        if 'name' in update_data:
            new_name = update_data['name'].strip().title()
            if await crud.check_region_name_exists(new_name, exclude_id=region_id):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Region name '{new_name}' already exists"
                )
            update_data['name'] = new_name

        return await crud.update_region(region_id, **update_data)

    # ============= 删除业务逻辑 =============

    @staticmethod
    async def delete_region_with_checks(region_id: int) -> None:
        """删除区域，包含业务检查"""
        await RegionService.get_region_by_id_or_404(region_id)
        await crud.delete_region(region_id)

    @staticmethod
    async def soft_delete_region(region_id: int) -> dict:
        """软删除区域"""
        await RegionService.get_region_by_id_or_404(region_id)
        await crud.update_region(region_id, is_deleted=True)
        return {"message": "Region soft deleted successfully"}

    @staticmethod
    async def restore_region(region_id: int) -> dict:
        """恢复软删除的区域"""
        region = await RegionService.get_region_by_id_or_404(region_id)
        if not region.is_deleted:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Region is not deleted"
            )

        await crud.update_region(region_id, is_deleted=False)
        return {"message": "Region restored successfully"}

    # ============= 批量操作业务逻辑 =============

    @staticmethod
    async def create_regions_batch(regions_data: List[RegionCreate]) -> dict:
        """批量创建区域"""
        if len(regions_data) > 100:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Batch size cannot exceed 100"
            )

        created_regions = []
        failed_regions = []

        for i, region_data in enumerate(regions_data):
            try:
                region = await RegionService.create_region_with_validation(region_data)
                created_regions.append(region)
            except HTTPException as e:
                failed_regions.append({
                    "index": i,
                    "name": region_data.name,
                    "error": e.detail
                })

        return {
            "created_count": len(created_regions),
            "failed_count": len(failed_regions),
            "created_regions": created_regions,
            "failed_regions": failed_regions
        }

    # ============= 统计业务逻辑 =============

    @staticmethod
    async def get_regions_statistics() -> dict:
        """获取区域统计信息"""
        total = await crud.count_regions()
        active = await crud.count_active_regions()
        deleted = await crud.count_deleted_regions()

        return {
            "total": total,
            "active": active,
            "deleted": deleted,
            "active_percentage": round((active / total * 100) if total > 0 else 0, 2)
        }