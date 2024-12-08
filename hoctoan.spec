# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:\\Users\\realklix3k\\Desktop\\this\\hoctoan.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\Users\\realklix3k\\Desktop\\this\\AI', 'AI/'), ('C:\\Users\\realklix3k\\Desktop\\this\\AI\\functions', 'functions/'), ('C:\\Users\\realklix3k\\Desktop\\this\\AI\\question_folder', 'question_folder/'), ('C:\\Users\\realklix3k\\Desktop\\this\\baigiang', 'baigiang/'), ('C:\\Users\\realklix3k\\Desktop\\this\\config', 'config/'), ('C:\\Users\\realklix3k\\Desktop\\this\\data', 'data/'), ('C:\\Users\\realklix3k\\Desktop\\this\\functions', 'functions/'), ('C:\\Users\\realklix3k\\Desktop\\this\\functions\\get_lesson_from_server', 'get_lesson_from_server/'), ('C:\\Users\\realklix3k\\Desktop\\this\\functions\\keyboard', 'keyboard/'), ('C:\\Users\\realklix3k\\Desktop\\this\\functions\\login_register', 'login_register/'), ('C:\\Users\\realklix3k\\Desktop\\this\\functions\\maths', 'maths/'), ('C:\\Users\\realklix3k\\Desktop\\this\\functions\\microphone', 'microphone/'), ('C:\\Users\\realklix3k\\Desktop\\this\\main_frontend', 'main_frontend/'), ('C:\\Users\\realklix3k\\Desktop\\this\\stuff', 'stuff/'), ('C:\\Users\\realklix3k\\Desktop\\this\\temp', 'temp/'), ('C:\\Users\\realklix3k\\Desktop\\this\\tts', 'tts/')],
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
    [],
    exclude_binaries=True,
    name='hoctoan',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='hoctoan',
)
