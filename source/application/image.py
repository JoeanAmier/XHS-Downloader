from source.expansion import Namespace

from .request import Html

__all__ = ["Image"]


class Image:
    @classmethod
    def get_image_link(cls, data: Namespace, format_: str) -> [list, list]:
        images = data.safe_extract("imageList", [])
        live_link = cls.__get_live_link(images)
        token_list = [
            cls.__extract_image_token(Namespace.object_extract(i, "urlDefault"))
            for i in images
        ]
        match format_:
            case "png" | "webp" | "jpeg" | "heic" | "avif":
                return [
                    Html.format_url(
                        cls.__generate_fixed_link(
                            i,
                            format_,
                        )
                    )
                    for i in token_list
                ], live_link
            case "auto":
                return [
                    Html.format_url(cls.__generate_auto_link(i)) for i in token_list
                ], live_link
            case _:
                raise ValueError

    @staticmethod
    def __generate_auto_link(token: str) -> str:
        return f"https://sns-img-bd.xhscdn.com/{token}"

    @staticmethod
    def __generate_fixed_link(
        token: str,
        format_: str,
    ) -> str:
        return f"https://ci.xiaohongshu.com/{token}?imageView2/format/{format_}"

    @staticmethod
    def __extract_image_token(url: str) -> str:
        return "/".join(url.split("/")[5:]).split("!")[0]

    @staticmethod
    def __get_live_link(items: list) -> list:
        return [
            (
                Html.format_url(
                    Namespace.object_extract(item, "stream.h264[0].masterUrl")
                )
                or None
            )
            for item in items
        ]
