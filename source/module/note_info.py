from datetime import datetime
from typing import TYPE_CHECKING
from aiofiles import open

if TYPE_CHECKING:
    from pathlib import Path


class NoteGenerator:
    def __init__(self, note_format: str) -> None:
        self.note_format = note_format

    @classmethod
    def generate_txt(cls, data: dict) -> str:
        """生成纯文本格式的作品信息"""
        desc = data["作品描述"].replace("\n", "\n    ")
        save_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        lines = [
            "[作品信息]",
            f"作品ID: {data['作品ID']}",
            f"作品类型: {data['作品类型']}",
            f"发布时间: {data['发布时间']}",
            f"最后更新时间: {data['最后更新时间']}",
            "",
            "[作品内容]",
            f"作品标题: {data['作品标题']}",
            f"作品描述: {desc}",
            f"作品标签: {data['作品标签']}",
            "",
            "[互动数据]",
            f"点赞数量: {data['点赞数量']}",
            f"收藏数量: {data['收藏数量']}",
            f"评论数量: {data['评论数量']}",
            f"分享数量: {data['分享数量']}",
            "",
            "[作者信息]",
            f"作者昵称: {data['作者昵称']}",
            f"作者ID: {data['作者ID']}",
            f"作者链接: {data['作者链接']}",
            "",
            f"保存时间: {save_time}",
            "",
            "*" * 50,
            "",
        ]
        return "\n".join(lines) + "\n"

    @classmethod
    def generate_md(cls, data: dict) -> str:
        """生成 Markdown 格式的作品信息"""
        # 处理多行描述：每行添加 2 空格 + > 引用符号，行末添加 2 空格强制换行
        desc_lines = data["作品描述"].split("\n")
        formatted_desc = "\n".join(f"  > {line}  " for line in desc_lines)
        save_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        lines = [
            "## 📝 作品信息",
            f"- **作品ID**：`{data['作品ID']}`",
            f"- **作品类型**：{data['作品类型']}",
            f"- **发布时间**：{data['发布时间']}",
            f"- **最后更新时间**：{data['最后更新时间']}",
            "",
            "---",
            "",
            "## 💬 作品内容",
            f"- **作品标题**：{data['作品标题']}",
            "- **作品描述**：",
            formatted_desc,
            f"- **作品标签**：{data['作品标签']}",
            "",
            "---",
            "",
            "## 📊 互动数据统计",
            f"- ❤️ **点赞数量**：{data['点赞数量']}",
            f"- ⭐ **收藏数量**：{data['收藏数量']}",
            f"- 💬 **评论数量**：{data['评论数量']}",
            f"- 🔗 **分享数量**：{data['分享数量']}",
            "",
            "---",
            "",
            "## 👤 作者信息",
            f"- **作者昵称**：{data['作者昵称']}",
            f"- **作者ID**：`{data['作者ID']}`",
            f"- **作者链接**：{data['作者链接']}",
            "",
            f"***保存时间：{save_time}***",
            "",
            "---",
            "",
        ]
        return "\n".join(lines) + "\n"

    @staticmethod
    async def write_note_info(content: str, file_path: "Path") -> None:
        """将内容追加写入到指定文件"""
        async with open(file_path, "a", encoding="utf-8") as f:
            await f.write(content)

    async def save_note_info(self, data: dict, path: "Path", name: str) -> None:
        if not self.note_format:
            return
        formats = ["md", "txt"] if self.note_format == "all" else [self.note_format]
        for fmt in formats:
            content = self.generate_md(data) if fmt == "md" else self.generate_txt(data)
            await self.write_note_info(content, path / f"{name}.{fmt}")
