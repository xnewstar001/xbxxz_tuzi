# 修真辅助（想不想修真）v8.5 逆向还原工程

## 如何运行（下载即可跑，无需安装任何依赖）

仓库自带完整运行时：`run/`（Qt 4.8.7 / PyQt4 / PyCrypto / protobuf / requests / 补丁版 game.pyd）
+ `tools/py27`（32 位 Python 2.7.18）。仅支持 Windows（32 位解释器可在 64 位系统上跑）。

```bat
git clone <本仓库>
cd fuzhu_project
copy run\config.ini.example run\config.ini
notepad run\config.ini        ; 填 [login] token= 与 gateway=（下面第 2 步）
run\启动辅助.bat               ; 或: cd run && ..\tools\py27\python.exe xbxxz_helper.py
; UI 里选渠道/区（随意）→ 点【开始挂机】
```

 **token 从哪来**：手机端登录《想不想修真》时抓包（fiddler/Charles），取完整渠道登录串
   （`appid=...&openid=...&timestamp=...&platform=...&server_id=N&access_token=...&sign=...`），
   一个账号×一个区一条。
