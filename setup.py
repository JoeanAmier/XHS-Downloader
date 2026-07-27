from importlib.metadata import distribution

from cx_Freeze import setup, Executable


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
    ],
    "include_files": [
        ("static", "static"),
        ("locale", "locale"),
        include_distribution_metadata("opentelemetry-api"),
    ],
}

executables = [
    Executable(
        script="main.py",
        icon="./static/XHS-Downloader",
        target_name="XHS-Downloader",
    )
]

setup(
    name="XHS-Downloader",
    options={"build_exe": build_exe_options},
    executables=executables,
)
