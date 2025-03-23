from pathlib import Path
from typing import TYPE_CHECKING

from ..translation import _
from .static import ERROR
from .tools import logging

if TYPE_CHECKING:
    from manager import Manager
    from recorder import MapRecorder


__all__ = ["Mapping"]


class Mapping:
    def __init__(
        self,
        manager: "Manager",
        mapping: "MapRecorder",
    ):
        self.root = manager.folder
        self.folder_mode = manager.folder_mode
        self.database = mapping
        self.switch = manager.author_archive

    async def update_cache(
        self,
        id_: str,
        alias: str,
        log=None,
    ):
        if not self.switch:
            return
        if (a := await self.has_mapping(id_)) and a != alias:
            self.__check_file(
                id_,
                alias,
                a,
                log,
            )
        await self.database.add(id_, alias)

    async def has_mapping(self, id_: str) -> str:
        return d[0] if (d := await self.database.select(id_)) else ""

    def __check_file(
        self,
        id_: str,
        alias: str,
        old_alias: str,
        log,
    ):
        if not (old_folder := self.root.joinpath(f"{id_}_{old_alias}")).is_dir():
            logging(
                log,
                _("{old_folder} 文件夹不存在，跳过处理").format(
                    old_folder=old_folder.name
                ),
            )
            return
        self.__rename_folder(
            old_folder,
            id_,
            alias,
            log,
        )
        self.__scan_file(
            id_,
            alias,
            old_alias,
            log,
        )

    def __rename_folder(
        self,
        old_folder: Path,
        id_: str,
        alias: str,
        log,
    ):
        new_folder = self.root.joinpath(f"{id_}_{alias}")
        self.__rename(
            old_folder,
            new_folder,
            _("文件夹"),
            log,
        )
        logging(
            log,
            _("文件夹 {old_folder} 已重命名为 {new_folder}").format(
                old_folder=old_folder.name, new_folder=new_folder.name
            ),
        )

    def __rename_works_folder(
        self,
        old_: Path,
        alias: str,
        old_alias: str,
        log,
    ) -> Path:
        if old_alias in old_.name:
            new_ = old_.parent / old_.name.replace(old_alias, alias, 1)
            self.__rename(
                old_,
                new_,
                _("文件夹"),
                log,
            )
            logging(
                log,
                _("文件夹 {old_} 重命名为 {new_}").format(
                    old_=old_.name, new_=new_.name
                ),
            )
            return new_
        return old_

    def __scan_file(
        self,
        id_: str,
        alias: str,
        old_alias: str,
        log,
    ):
        root = self.root.joinpath(f"{id_}_{alias}")
        item_list = root.iterdir()
        if self.folder_mode:
            for f in item_list:
                if f.is_dir():
                    f = self.__rename_works_folder(
                        f,
                        alias,
                        old_alias,
                        log,
                    )
                    files = f.iterdir()
                    self.__batch_rename(
                        f,
                        files,
                        alias,
                        old_alias,
                        log,
                    )
        else:
            self.__batch_rename(
                root,
                item_list,
                alias,
                old_alias,
                log,
            )

    def __batch_rename(
        self,
        root: Path,
        files,
        alias: str,
        old_alias: str,
        log,
    ):
        for old_file in files:
            if old_alias not in old_file.name:
                break
            self.__rename_file(
                root,
                old_file,
                alias,
                old_alias,
                log,
            )

    def __rename_file(
        self,
        root: Path,
        old_file: Path,
        alias: str,
        old_alias: str,
        log,
    ):
        new_file = root.joinpath(old_file.name.replace(old_alias, alias, 1))
        self.__rename(
            old_file,
            new_file,
            _("文件"),
            log,
        )
        logging(
            log,
            _("文件 {old_file} 重命名为 {new_file}").format(
                old_file=old_file.name, new_file=new_file.name
            ),
        )
        return True

    @staticmethod
    def __rename(
        old_: Path,
        new_: Path,
        type_=_("文件"),
        log=None,
    ) -> bool:
        try:
            old_.rename(new_)
            return True
        except PermissionError as e:
            logging(
                log,
                _("{type} {old}被占用，重命名失败: {error}").format(
                    type=type_, old=old_.name, error=e
                ),
                ERROR,
            )
            return False
        except FileExistsError as e:
            logging(
                log,
                _("{type} {new}名称重复，重命名失败: {error}").format(
                    type=type_, new=new_.name, error=e
                ),
                ERROR,
            )
            return False
        except OSError as e:
            logging(
                log,
                _("处理{type} {old}时发生预期之外的错误: {error}").format(
                    type=type_, old=old_.name, error=e
                ),
                ERROR,
            )
            return True
