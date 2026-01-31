# run_test_tunehub.py
import types, sys, tempfile, os
# minimal mocks so api.py can import
sys.modules['xbmc'] = types.SimpleNamespace(translatePath=lambda p: p, LOGERROR=1)
sys.modules['xbmcaddon'] = types.SimpleNamespace(Addon=lambda: types.SimpleNamespace(getAddonInfo=lambda k: tempfile.gettempdir()))
sys.modules['xbmcplugin'] = types.SimpleNamespace(getSetting=lambda *a, **k: 'false')
sys.modules['xbmcvfs'] = types.SimpleNamespace(translatePath=lambda p: p)
# import the modified client
from api import NetEase
n = NetEase()
# 替换为你想测试的网易歌曲 id 与码率
print(n.tunehub_url(123456789, '320k'))