from source.expansion import Namespace

from .request import Html

__all__ = ["Image"]


class Image:
    @classmethod
    def get_image_link(cls, data: Namespace, format_: str) -> tuple[list, list]:
        images = data.safe_extract("imageList", [])
        live_link = cls._get_live_link(images)
        for extractor in (
            lambda i: Namespace.object_extract(i, "fileId"),
            lambda i: cls._extract_image_token(
                Namespace.object_extract(i, "urlDefault")
            ),
            lambda i: cls._extract_image_token(Namespace.object_extract(i, "urlPre")),
        ):
            token_list = [extractor(i) for i in images]
            if any(token_list):
                break
        else:
            return [], []
        match format_:
            case "png" | "webp" | "jpeg" | "heic" | "avif":
                return [
                    Html.format_url(
                        cls._generate_fixed_link(
                            i,
                            format_,
                        )
                    )
                    for i in token_list
                ], live_link
            case "auto":
                return [
                    Html.format_url(cls._generate_auto_link(i)) for i in token_list
                ], live_link
            case _:
                raise ValueError

    @staticmethod
    def _generate_auto_link(token: str) -> str:
        return f"https://sns-img-bd.xhscdn.com/{token}"

    @staticmethod
    def _generate_fixed_link(
        token: str,
        format_: str,
    ) -> str:
        return f"https://ci.xiaohongshu.com/{token}?imageView2/format/{format_}"

    @staticmethod
    def _extract_image_token(url: str) -> str:
        return "/".join(url.split("/")[5:]).split("!")[0]

    @staticmethod
    def _get_live_link(items: list) -> list:
        result = []
        for item in items:
            url = None
            stream = Namespace.object_extract(item, "stream", {})
            for key in vars(stream):
                url = Namespace.object_extract(
                    stream, f"{key}[0].backupUrls[0]"
                ) or Namespace.object_extract(stream, f"{key}[0].masterUrl")
                if url := Html.format_url(url):
                    break
            result.append(url)
        return result
