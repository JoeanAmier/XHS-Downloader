from importlib.metadata import distribution
from sys import platform

from cx_Freeze import Executable, setup


def include_distribution_metadata(distribution_name):
    dist = distribution(distribution_name)
    metadata_path = dist._path

    if metadata_path.name.endswith((".dist-info", ".egg-info")):
        return str(metadata_path), f"lib/{metadata_path.name}"

    raise RuntimeError(f"Cannot locate metadata for {distribution_name!r}")


build_exe_options = {
    "packages": [
        "rich",
        "opentelemetry",
        "uvicorn",
    ],
    "include_files": [
        ("static", "static"),
        ("locale", "locale"),
        include_distribution_metadata("opentelemetry-api"),
    ],
    "include_msvcr": True,
}

executables = [
    Executable(
        script="main.py",
        icon="./static/XHS-Downloader",
        target_name="XHS-Downloader",
    )
]

if platform == "win32":
    executables.append(
        Executable(
            script="main.py",
            base="gui",
            icon="./static/XHS-Downloader",
            target_name="XHS-Downloader-GUI",
        )
    )

setup(
    name="XHS-Downloader",
    options={"build_exe": build_exe_options},
    executables=executables,
)
