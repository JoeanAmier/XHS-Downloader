from source.expansion import Namespace
from .request import Html

__all__ = ['Image']


class Image:
    @classmethod
    def get_image_link(cls, data: Namespace, format_: str) -> list:
        images = data.safe_extract("imageList", [])
        token_list = [
            cls.__extract_image_token(
                Namespace.object_extract(
                    i, "urlDefault")) for i in images]
        match format_:
            case "png":
                return [Html.format_url(cls.__generate_png_link(i))
                        for i in token_list]
            case "webp":
                return [Html.format_url(cls.__generate_webp_link(i))
                        for i in token_list]
            case _:
                raise ValueError

    @staticmethod
    def __generate_webp_link(token: str) -> str:
        return f"https://sns-img-bd.xhscdn.com/{token}"

    @staticmethod
    def __generate_png_link(token: str) -> str:
        return f"https://ci.xiaohongshu.com/{token}?imageView2/2/w/format/png"

    @staticmethod
    def __extract_image_token(url: str) -> str:
        return "/".join(url.split("/")[5:]).split("!")[0]
