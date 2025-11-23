import json
from typing import Any, Dict, List


def build_tree(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """构建树形结构"""
    # 创建id到item的映射
    item_map = {item["id"]: item for item in items}

    # 构建树
    tree = []
    for item in items:
        if item["pId"] == 0:
            tree.append(item)
            item["children"] = []
        else:
            parent = item_map.get(item["pId"])
            if parent:
                if "children" not in parent:
                    parent["children"] = []
                parent["children"].append(item)

    return tree


def convert_to_js_format(item: Dict[str, Any]) -> Dict[str, Any]:
    """转换为JS格式的数据结构"""
    js_item = {
        "id": item["id"],
        "name": item["name"],
        "pId": item["pId"],
        "status": item["status"],
        "uri": item["uri"],
        "children": [],
    }

    # 添加可选字段
    if item["isExpand"]:
        js_item["isExpand"] = item["isExpand"]
    if item["desc"]:
        js_item["desc"] = item["desc"]
    if item["favicon"]:
        js_item["favicon"] = item["favicon"]
    if item["orderNum"]:
        js_item["orderNum"] = item["orderNum"]

    return js_item


def process_tree(tree: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """处理树形结构，转换为JS格式"""
    result = []
    for item in tree:
        js_item = convert_to_js_format(item)
        if "children" in item and item["children"]:
            js_item["children"] = process_tree(item["children"])
        result.append(js_item)
    return result


def generate_js_file(category: str, items: List[Dict[str, Any]], output_file: str):
    """生成JS文件"""

    # 构建树
    tree = build_tree(items)

    # 转换为JS格式
    js_data = process_tree(tree)

    # 生成JS文件内容
    js_content = f"const {category}_site_list = " f"{json.dumps(js_data, ensure_ascii=False, indent=4)}"

    # 写入文件
    with open(output_file, "w", encoding="utf-8-sig") as f:
        f.write(js_content)


def main():
    """主函数"""
    # 获取数据
    index_items = []  # get_nav_items('index')
    # 生成index.js
    generate_js_file(index_items, "index", "index.js")
    # 生成others.js
    other_items = []  # get_nav_items('other')
    generate_js_file(other_items, "other", "others.js")


if __name__ == "__main__":
    main()
