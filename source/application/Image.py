from source.expansion import Namespace
from .Html import Html

__all__ = ['Image']


class Image:
    @classmethod
    def get_image_link(cls, data: Namespace, format_: str) -> list:
        images = data.safe_extract("imageList", [])
        match format_:
            case "png":
                return [
                    Html.format_url(
                        cls.__generate_png_link(
                            cls.__extract_png_token(Namespace.object_extract(
                                i,
                                "urlDefault")))) for i in images]
            case "webp":
                return [
                    Html.format_url(
                        cls.__generate_webp_link(
                            cls.__extract_webp_token(Namespace.object_extract(
                                i,
                                "urlDefault")))) for i in images]
        raise ValueError

    @staticmethod
    def __generate_webp_link(token: str) -> str:
        return f"https://sns-img-bd.xhscdn.com/{token}"

    @staticmethod
    def __generate_png_link(token: str) -> str:
        return f"https://ci.xiaohongshu.com/{token}?imageView2/2/w/format/png"

    @staticmethod
    def __extract_webp_token(url: str) -> str:
        return "/".join(url.split("/")[5:]).split("!")[0]

    @staticmethod
    def __extract_png_token(url: str) -> str:
        return url.split("/")[-1].split("!")[0]
