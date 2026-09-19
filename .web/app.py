#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" Visualization / app.py
    Flask 可视化模块:自动扫描指定目录下的 JSON DAG 文件,
    以表格列出,点击 DAG ID 查看图形化 DAG。
"""

import os
import json

from flask import Flask, render_template, request, abort, jsonify

# 界面输入框预填的默认路径,可用环境变量 DAG_SCAN_ROOT 覆盖
_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DEFAULT_ROOT = os.environ.get("DAG_SCAN_ROOT", os.path.join(_REPO_ROOT, "DAG_Model", "Data", "Idata"))

app = Flask(__name__)


def _numkey(_k):
    """ 尝试把节点键转成可排序的 (int, str) 元组,失败则按字符串排 """
    try:
        return (0, int(_k), _k)
    except (TypeError, ValueError):
        return (1, 0, str(_k))


def _iter_dag_entries(_obj):
    """ 递归找出一个 JSON 对象里所有形如 {G:{V,E}} 的 DAG 条目,产出 (id, 条目) """
    if isinstance(_obj, dict):
        if isinstance(_obj.get("G"), dict) and isinstance(_obj["G"].get("V"), dict):
            yield (_obj.get("ID"), _obj)
        for _k, _v in _obj.items():
            if _k == "G":
                continue
            yield from _iter_dag_entries(_v)


def _parse_dag_file(_file):
    """ 解析单个 JSON 文件,提取所有 |V|>=2 的 DAG,返回 (dag_list, is_error) """
    try:
        with open(_file, "r", encoding="utf-8") as _f:
            _td = json.load(_f)
    except (json.JSONDecodeError, UnicodeDecodeError, OSError):
        return [], True
    _dags = []
    for _id, _entry in _iter_dag_entries(_td):
        _v = _entry["G"]["V"]
        if len(_v) < 2:
            continue
        _e = _entry["G"].get("E", []) or []
        _dags.append({
            "id": str(_id) if _id is not None else os.path.splitext(os.path.basename(_file))[0],
            "V": len(_v),
            "E": len(_e),
            "T": _entry.get("T", ""),
            "D": _entry.get("D", ""),
        })
    return _dags, False


def _scan_dir(_root):
    """ 递归扫描目录下全部 .json 文件并汇总 DAG 列表 """
    _dags, _errors = [], 0
    for _dp, _dirs, _fs in os.walk(_root):
        _dirs.sort()
        for _f in sorted(_fs):
            if not _f.endswith(".json"):
                continue
            _file = os.path.join(_dp, _f)
            _file_dags, _is_error = _parse_dag_file(_file)
            _errors += 1 if _is_error else 0
            for _d in _file_dags:
                _d["file"] = os.path.relpath(_file, _root)
                _dags.append(_d)
    return _dags, _errors


def _scan_path(_addr):
    """ 界面提交的地址(目录或单个 .json 文件)检测 DAG,返回 (dags, errors, 目录) """
    _addr = os.path.abspath(os.path.expanduser(_addr))
    if os.path.isdir(_addr):
        _dags, _errors = _scan_dir(_addr)
        _base = _addr
    elif os.path.isfile(_addr) and _addr.lower().endswith(".json"):
        _file_dags, _is_error = _parse_dag_file(_addr)
        for _d in _file_dags:
            _d["file"] = os.path.basename(_addr)
        _dags, _errors = _file_dags, 1 if _is_error else 0
        _base = os.path.dirname(_addr)
    else:
        raise FileNotFoundError(f"路径不存在或不是 .json 文件:{_addr}")
    _dags.sort(key=lambda _d: (_d["file"], _numkey(_d["id"])))
    return _dags, _errors, _base


def _node_attr(_nd, *_keys):
    """ 兼容大写/小写键取值,如 W/w, B/b, O/o, A/a, P/p """
    for _k in _keys:
        for _c in (_k, _k.lower()):
            if _c in _nd:
                return _nd[_c]
    return None


def _fmt(_v):
    """ 嵌套 dict/list 值转成紧凑 JSON 字符串,便于前端展示 """
    if isinstance(_v, (dict, list)):
        return json.dumps(_v, ensure_ascii=False)
    return _v


def _load_dag(_file):
    """ 读取文件并归一化单个 DAG 为 Cytoscape 元素结构 """
    try:
        with open(_file, "r", encoding="utf-8") as _f:
            _td = json.load(_f)
    except (json.JSONDecodeError, UnicodeDecodeError, OSError) as _ex:
        abort(400, f"无法解析文件:{_ex}")
    for _id, _entry in _iter_dag_entries(_td):
        if len(_entry["G"]["V"]) < 2:
            continue
        _nodes, _edges = [], []
        for _k, _v in _entry["G"]["V"].items():
            _nodes.append({
                "id": str(_k),
                "label": str(_v.get("INDEX", _k)),
                "W": _fmt(_node_attr(_v, "W", "w")),
                "B": _fmt(_node_attr(_v, "B", "b")),
                "O": _node_attr(_v, "O", "o"),
                "A": _node_attr(_v, "A", "a"),
                "P": _node_attr(_v, "P", "p"),
            })
        _nodes.sort(key=lambda _n: _numkey(_n["id"]))
        for _s, _t in _entry["G"].get("E", []) or []:
            _edges.append({"source": str(_s), "target": str(_t)})
        return {
            "id": str(_id) if _id is not None else os.path.splitext(os.path.basename(_file))[0],
            "T": _entry.get("T", ""),
            "D": _entry.get("D", ""),
            "nodes": _nodes,
            "edges": _edges,
        }
    abort(404, "未在文件中找到 DAG")


@app.route("/")
def index():
    """ DAG 检测页:由界面提交扫描地址 """
    return render_template("index.html", default_root=DEFAULT_ROOT)


@app.post("/api/scan")
def api_scan():
    """ 界面提交地址 → 检测 DAG 列表 (JSON) """
    _data = request.get_json(silent=True) or {}
    _addr = (_data.get("root") or "").strip()
    if not _addr:
        return jsonify({"error": "请输入要扫描的路径"}), 400
    try:
        _dags, _errors, _base = _scan_path(_addr)
    except FileNotFoundError as _ex:
        return jsonify({"error": str(_ex)}), 400
    return jsonify({"root": _addr, "base": _base, "dags": _dags, "errors": _errors})


@app.route("/dag")
def dag():
    """ DAG 详情:图形化页 """
    _root_s = request.args.get("root", "").strip()
    _rel = request.args.get("path", "")
    if not _root_s:
        abort(400, "缺少 root 参数")
    _root = os.path.realpath(os.path.expanduser(_root_s))
    if not os.path.isdir(_root):
        abort(400, "非法目录")
    _abs = os.path.realpath(os.path.join(_root, _rel))
    if not _abs.startswith(_root + os.sep):
        abort(400, "非法路径")
    _data = _load_dag(_abs)
    _data["file"] = _rel
    _data["root"] = _root_s
    return render_template("dag.html", dag=_data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)