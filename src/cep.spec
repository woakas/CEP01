# -*- mode: python -*-
from kivy.tools.packaging.pyinstaller_hooks import install_hooks
import os
install_hooks(globals())


PROJECT_DIR = os.path.join(os.path.dirname(__file__))

a = Analysis(['main.py'],
             pathex=[PROJECT_DIR],
             hiddenimports=[],
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='cep01.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True )
coll = COLLECT(exe,
               Tree(PROJECT_DIR),
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name='cep')
