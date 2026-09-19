# AGENTS.md

独立的 Flask 应用:扫描 JSON DAG 文件并用 Cytoscape 渲染图(中文注释/UI)。本目录是**独立的 git 仓库(尚无提交)**,嵌套在更大的 `dag-scheduler` 仓库里,后者根目录的 `../AGENTS.md` 覆盖整个项目 —— 需要了解数据格式上下文时请先读它。

## 运行

```bash
pip install flask        # 唯一依赖,见 requirements.txt
python3 app.py           # http://0.0.0.0:5000
```

- 默认扫描根目录 = `../DAG_Model/Data/Idata`(父仓库,相对于本仓库根目录);用环境变量 `DAG_SCAN_ROOT` 覆盖。脱离父仓库/移动到别处运行时找不到该路径。
- 无测试、无 lint、无 CI。验证方式:运行服务或直接 import `app.py` 里的函数。

## 架构

- `app.py` —— 全部逻辑。路由:
  - `GET /` → `templates/index.html`,扫描表单页
  - `POST /api/scan` —— body `{"root": <目录或.json>}` → DAG 列表 JSON
  - `GET /dag?root=<目录>&path=<相对路径>` —— 渲染 `templates/dag.html`;要求 `root` 为目录,并通过 `realpath(root + "/" + path)` 必须落在 `root` 之下的路径穿越检查 —— 改动路由时务必保留此检查。
- `templates/dag.html` 从 unpkg CDN 加载 Cytoscape(**需要联网**);dagre 布局、LR 方向,节点颜色由 `A`(核心/分配)取模调色板得出。

## DAG JSON 格式(`_parse_dag_file` / `_load_dag` 的解析假设)

- 一个 DAG 条目是任意含 `G: {V: {...}, E: [[src,dst],...]}` 结构的 dict;递归查找嵌套条目;没有 `ID` 的条目用文件名作 id。`|V|<2` 的 DAG 会被丢弃;无法解析的文件会被跳过并计入 `errors` 字段 —— 测试时不要把这两种情况当 bug。
- 节点属性 `W/B/O/A/P` 大小写不敏感读取(`_node_attr` 同时查小写 —— `NTask`/`NSystem` 文件用小写 `w,b,o,a,p`)。`W`/`B` 为 dict/list 值时 JSON 字符串化后展示(`_fmt`)。
- 节点 `label` 取 `V[k].INDEX`,否则取节点键。

## 约定

- 保持中文注释/docstring/UI 文案。
- 辅助函数用 `_` 前缀(如 `_numkey`、`_scan_dir`、`_fmt`)。