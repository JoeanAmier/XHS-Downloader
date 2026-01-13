# route.py
from typing import Optional

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from source.module import Manager, logging

from .generate_js import generate_js_file
from .model import SiteItemUpdate
from .module import SiteItem

router = APIRouter(prefix="/sites", tags=["Site Nav"])


class SiteNavRoute:
    def __init__(self, manager: Manager, db_obj: SiteItem):
        self.db_obj = db_obj
        self.manager = manager

    def setup_routes(self):
        @router.get(
            "",
            summary="Get Site Items",
            description="获取所有网站",
            response_class=JSONResponse,
        )
        async def get_sites(category: str = "index"):
            logging(None, f"start get sites for category: {category}")
            return await self.db_obj.all(category)

        def _build_site_tree(flat_sites):
            """将扁平的站点数据转换为树形结构"""
            # 创建一个字典，以站点id为键，站点对象为值
            site_map = {site["id"]: {**site, "children": []} for site in flat_sites}
            
            # 根节点列表
            root_nodes = []
            
            # 遍历每个站点，建立父子关系
            for site in flat_sites:
                site_id = site["id"]
                pid = site.get("pId")
                
                # 如果没有父节点或父节点不存在，则为根节点
                if not pid or pid not in site_map:
                    root_nodes.append(site_map[site_id])
                else:
                    # 将当前节点添加到其父节点的children列表中
                    site_map[pid]["children"].append(site_map[site_id])
            
            return root_nodes

        @router.get(
            "/tree",
            summary="Get Sites Tree",
            description="获取网站树形结构数据",
            response_class=JSONResponse,
        )
        async def get_sites_tree(category: str = "index"):
            logging(None, f"start get sites tree for category: {category}")
            flat_sites = await self.db_obj.all(category)
            tree_sites = _build_site_tree(flat_sites)
            return tree_sites

        @router.post(
            "",
            summary="Save Site Item",
            description="保存网站",
            response_class=JSONResponse,
        )
        async def save_site_item(site_item: SiteItemUpdate, id: Optional[str] = None):
            if id:
                exist_item = await self.db_obj.select(id)
                if exist_item:
                    await self.db_obj.update(id, **site_item.model_dump(exclude_unset=True))
                else:
                    return {"code": 1001, "message": "Site item not found"}
            else:
                # If no id and has uri but no desc, fetch metadata from url
                if site_item.uri and not site_item.desc:
                    from .site_metadata import fetch_metadata_from_url
                    metadata = await fetch_metadata_from_url(site_item.uri)
                    # Update site_item with fetched metadata
                    if metadata.get("title"):
                        site_item.name = metadata["title"]
                    if metadata.get("description"):
                        site_item.desc = metadata["description"]
                    if metadata.get("favicon"):
                        site_item.favicon = metadata["favicon"]
                await self.db_obj.add(**site_item.model_dump())

            return {"code": 200, "message": "Site item saved successfully"}

        @router.delete(
            "/{id_}",
            summary="Delete Site Item",
            description="删除指定ID的网站",
            tags=["Site Nav"],
            response_class=JSONResponse,
        )
        async def delete_site_item(id_: str):
            await self.db_obj.delete(id_)
            return {"code": 200, "message": "Site item deleted successfully"}

        @router.get(
            "/generate",
            summary="Generate Sites JS File",
            description="生成网站js文件",
            response_class=JSONResponse,
        )
        async def generate_sites(category: str = "index"):
            import os

            dict_items = await self.db_obj.all(category)

            # 生成 JS 文件
            download_folder = self.manager.folder
            output_file = os.path.join(download_folder, category + ".js")
            generate_js_file(category, dict_items, output_file)
            return {"code": 200, "data": [category + ".js"]}

        @router.get(
            "/fetch_metadata",
            summary="Fetch Metadata from URL",
            description="Fetches title, description, and logo from the given URL",
            tags=["Site Nav"],
            response_class=JSONResponse,
        )
        async def fetch_metadata(url: str):
            from .site_metadata import fetch_metadata_from_url

            return {"code": 200, "data": await fetch_metadata_from_url(url)}

        @router.post(
            "/update_metadata_batch",
            summary="Batch Update Metadata",
            description="批量更新指定分类下缺失favicon的站点元数据",
            response_class=JSONResponse,
        )
        async def batch_update_metadata(category: str):
            logging(None, f"start batch update metadata for category: {category}")

            # 查询符合条件的站点
            query = "SELECT * FROM site_item WHERE LOWER(category) = LOWER(?) AND uri IS NOT NULL AND uri != '' AND (favicon IS NULL OR favicon = '')"
            await self.db_obj.cursor.execute(query, (category,))
            rows = await self.db_obj.cursor.fetchall()

            columns = [col[0] for col in self.db_obj.DATA_TABLE]
            sites = [dict(zip(columns, item)) for item in rows]

            updated_count = 0
            from .site_metadata import fetch_metadata_from_url

            for site in sites:
                url = site["uri"]
                try:
                    metadata = await fetch_metadata_from_url(url)
                    if "error" not in metadata:
                        update_data = {}
                        if metadata.get("favicon"):
                            update_data["favicon"] = metadata["favicon"]
                        if metadata.get("description"):
                            update_data["desc"] = metadata["description"]

                        if update_data:
                            await self.db_obj.update(site["id"], **update_data)
                            updated_count += 1
                except Exception as e:
                    logging(None, f"Error updating metadata for {url}: {e}")

            return {
                "code": 200,
                "message": f"Updated {updated_count} sites",
                "total_candidates": len(sites),
            }

        return router