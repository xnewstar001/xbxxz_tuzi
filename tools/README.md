# tools/ — 逆向与校验工具

本目录包含把 `修真辅助v8.5.exe` 还原为源码工程的全部工具脚本，以及校验脚本。

## 复现流程

```powershell
# 0. 准备
#   - Python 3.x（装 xdis + uncompyle6；本项目针对 uncompyle6 3.9.3 / xdis 6.1.7 做了两处补丁，见 docs/01-逆向还原报告.md）
#   - Python 2.7.18（tools/py27/，用 msiexec /a 解包 python-2.7.18.msi 获得，仅用于校验）

# 1. 解出 PyInstaller CArchive 全部条目（含主脚本字节码、game.pyd、PYZ）
python tools/extract_carchive.py "fuzhu/修真辅助v8.5.exe" build/extracted

# 2. 提取 PYZ 里的应用模块并补 py2.7 pyc 头
python tools/extract_pyz.py build/extracted/PYZ-00.pyz build/pyc_ready

# 3. 反编译全部模块
uncompyle6 -o build/decompiled build/pyc_ready/xbxxz_helper.pyc
# ... op / qt_main / browser / icon / xbxxz_pb2 同理；Pic_rc 无法反编译，保留 .pyc

# 4. 修复 + 落入 src/
python tools/fix_decompiled.py build/decompiled src

# 5. 校验（必须全绿，见 docs/01 第 4 节）
tools/py27/python.exe -m compileall -q -f src          # 语法/字节码校验
tools/py27/python.exe tools/verify_op_py27.py           # op.py 全变量值比对（期望 different: 0）
python tools/verify_const_coverage.py                   # 各模块 CJK 常量覆盖（期望 missing: 0）
```

## 文件说明

| 文件 | 作用 |
|---|---|
| extract_carchive.py | 解析 PyInstaller CArchive（尾部 cookie `MEI\x0c\x0b\x0a\x0b\x0e` + TOC），解出全部条目 |
| extract_pyz.py | 解析 PYZ-00.pyz（PYZ 魔数 + marshal TOC），提取模块并补 py2.7 pyc 头 |
| fix_decompiled.py | 修复 `\u0x` 转义损坏、补编码声明、去模块级 `return` |
| build_runtime.py | 从原 exe + src/ + resources/ 合成可直接运行的 run/（含 Qt DLL、PYZ 第三方包、配置模板） |
| **apply_offline.py** | **脱离作者服务器改造固化（幂等）**：xbxxz_helper.py 两处锚点 + run/game.pyd RSA 补丁 + 同步 src→run。流水线 = build_runtime → apply_offline（见 docs/07） |
| patch_game_pyd.py | game.pyd 内嵌 RSA 公钥等长替换（分析目录工作版；apply_offline 内置同款逻辑） |
| make_rsa_key.py | 生成本地 RSA 密钥对（mykey.json/priv/pub_spki.b64） |
| verify_op_py27.py | 用 py2.7 真实执行还原的 op.py，与原始 pyc 逐变量对比值 |
| verify_const_coverage.py | 检查全部 CJK unicode 常量在还原源码中的覆盖情况 |
| probe_game.py / probe_stage2~40.py | game.pyd 动态逆向探针系列（requests/socket 钩子 + 异常即路标）。关键节点：stage5（AES key）、stage19（应答格式）、stage30（tempid 闸）、stage35~37（旧发包实验，S->C=0 假会话）、**stage38（端到端验收：LIVE SESSION）**、stage40（长保活看门狗检查）。**probe_stage2~37.py 含本地抓包样本/账号数据，仅本地留档不入库（结论已固化在 docs/06）；入库的 stage38/40 及其他探针均从 run/config.ini 读 token/gateway** |
| probe_charge.py / probe_int_parse.py / probe_mso.py | 授权工具面黑盒探测（make_int*/get_int* 的 protobuf 文本格式、make_self_obj 输入变体） |
| probe_trace_auth.py | **授权数据流全追踪**：包装 game 模块 get_int*/make_int*/get_delta/make_self_obj 等，跑真实登录链打印每次调用（定位"辅助到期"功能闸的决策数据） |
| probe_capture_ep.py | **作者服务器端点全捕捉**：包装 local_auth._handle_author，真实会话记录全部请求（URL/请求体/AES解密/响应）→ analysis/endpoint_capture.log（docs/08 数据源） |
| （analysis/）endpoint_xrefs.py 等 | 静态分析：17 端点 URL 槽位→代码引用→capstone 上下文 → analysis/endpoint_xrefs.txt、endpoint_deep*.txt（docs/08 数据源；analysis/ 为本地工作目录，不入库） |
| find_aint_setters.py / dump_aint_setter.py / dump_fixed.py / dump_setter_callsites.py / find_fn_and_tuple.py / xref_int_fns.py / find_expiry_msg_refs.py | capstone 静态分析脚本（字符串表槽引用/PyMethodDef 定位/函数 dump；dump_fixed.py 含偏移 bug 修正说明） |
| probe_gw_raw.py | 前置登录服裸协议探针（0201/0202 → 打印 0204 完整载荷；实测 331B） |
| probe_stageNN.py 运行方式 | `cd run` 后 `..\tools\py27\python.exe ..\tools\probe_stageNN.py`；探针自带看门狗自杀 |
| patches/xbxxz_helper.pre_offline.py | xbxxz_helper.py 改造前基线备份（docs/07 §8 回退用） |
| keys/pub_spki.b64 | 本项目 RSA 公钥（apply_offline.py 等长替换 game.pyd 内嵌公钥用）。私钥不入库也不需要——运行/补丁只用公钥；要重生成密钥对用 make_rsa_key.py（生成后需重跑 apply_offline.py 重打补丁） |
| py27/ | 本地解包的 Python 2.7.18（msiexec /a python-2.7.18.msi 提取，非系统安装），用于编译、执行校验与运行 run/（已入库，开箱即用） |
| python-2.7.18.msi | py27 的来源安装包 |

## 运行 run/ 的要点

- 必须用 32 位 py2.7（tools/py27）；`QT_PLUGIN_PATH` 指向 run/qt4_plugins（启动辅助.bat 已处理）；
- PYZ 提取白名单里的第三方包以 .pyc 落盘（requests/urllib3/Crypto/google.protobuf/chardet/certifi/idna/six/backports/configparser/netbios/PyQt4.__init__）；
- six 若缺失会导致 `google.protobuf.descriptor` 导入失败（protobuf 3.x 依赖）。
