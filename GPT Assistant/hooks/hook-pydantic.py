from PyInstaller.utils.hooks import collect_submodules, copy_metadata

hiddenimports = collect_submodules('pydantic')
datas = copy_metadata('pydantic')