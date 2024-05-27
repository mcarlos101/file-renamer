# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['src\\file_renamer\\__main__.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('html\\license.html', '.'),
        ('html\\qt-for-python.html', '.'),
        ('html\\version.html', '.'),
        ('css\\bootstrap.min.css', '.'),
        ('js\\bootstrap.bundle.min.js', '.')
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='file-renamer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icons\\file-renamer.ico',
)
