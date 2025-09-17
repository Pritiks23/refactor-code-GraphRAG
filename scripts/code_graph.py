#!/usr/bin/env python3
import os, re, ast, glob, hashlib
from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple, Optional
from graphviz import Digraph

# -------- config --------
EXCLUDE_DIRS = {".git", ".venv", "venv", "site-packages", "build", "dist", "__pycache__", ".mypy_cache", ".ruff_cache", ".pytest_cache", "node_modules"}
DIAGRAM_DIR = os.path.join("diagrams")
os.makedirs(DIAGRAM_DIR, exist_ok=True)

# -------- utils --------
def is_excluded(path: str) -> bool:
    parts = set(path.split(os.sep))
    return bool(EXCLUDE_DIRS & parts)

def discover_py_files(root: str) -> List[str]:
    files = []
    for p in glob.glob(os.path.join(root, "**/*.py"), recursive=True):
        if p.endswith(".py") and not is_excluded(p):
            files.append(os.path.abspath(p))
    return files

def module_name_from_path(root: str, file_path: str) -> str:
    rel = os.path.relpath(file_path, root)
    parts = rel.split(os.sep)
    if parts[-1] == "__init__.py":
        parts = parts[:-1]
    else:
        parts[-1] = parts[-1].replace(".py", "")
    # stop at non-package boundary if __init__.py absent
    # but for simplicity, join all
    mod = ".".join([p for p in parts if p])
    return mod

# -------- AST collection --------
@dataclass
class Func:
    name: str
    qualname: str
    file: str
    lineno: int
    calls: Set[str] = field(default_factory=set)

@dataclass
class ModuleInfo:
    path: str
    module: str
    imports: Set[str] = field(default_factory=set)
    funcs: List[Func] = field(default_factory=list)

class Walker(ast.NodeVisitor):
    def __init__(self, file: str, module: str):
        self.file = file
        self.module = module
        self.stack: List[str] = []
        self.funcs: List[Func] = []
        self.imports: Set[str] = set()
        self.current: Optional[Func] = None

    def visit_Import(self, node):
        for n in node.names:
            self.imports.add(n.name.split(".")[0])

    def visit_ImportFrom(self, node):
        if node.module:
            self.imports.add(node.module.split(".")[0])

    def visit_FunctionDef(self, node):
        qual = ".".join(self.stack + [node.name]) if self.stack else node.name
        f = Func(name=node.name, qualname=f"{self.module}.{qual}", file=self.file, lineno=node.lineno)
        self.funcs.append(f)
        prev = self.current
        self.stack.append(node.name)
        self.current = f
        self.generic_visit(node)
        self.stack.pop()
        self.current = prev

    def visit_AsyncFunctionDef(self, node):
        self.visit_FunctionDef(node)

    def visit_ClassDef(self, node):
        self.stack.append(node.name)
        self.generic_visit(node)
        self.stack.pop()

    def visit_Call(self, node):
        if self.current is not None:
            callee = None
            if isinstance(node.func, ast.Name):
                callee = node.func.id
            elif isinstance(node.func, ast.Attribute):
                callee = node.func.attr
            if callee:
                self.current.calls.add(callee)
        self.generic_visit(node)

def collect(root: str) -> Dict[str, ModuleInfo]:
    out: Dict[str, ModuleInfo] = {}
    for f in discover_py_files(root):
        try:
            src = open(f, "r", encoding="utf-8").read()
            tree = ast.parse(src)
        except Exception:
            continue
        mod = module_name_from_path(root, f)
        w = Walker(f, mod); w.visit(tree)
        out[mod] = ModuleInfo(path=f, module=mod, imports=w.imports, funcs=w.funcs)
    return out

# -------- Graph rendering --------
def render_module_graph(mods: Dict[str, ModuleInfo], out_path: str):
    g = Digraph("modules", format="svg")
    g.attr(rankdir="LR", concentrate="true", splines="spline", nodesep="0.3", ranksep="0.7")
    g.attr("node", shape="box", style="rounded,filled", fillcolor="#f6f8fa", color="#d0d7de", fontname="Inter,Helvetica,Arial", fontsize="10")

    for m in mods:
        g.node(m)

    edges: Set[Tuple[str, str]] = set()
    for m, info in mods.items():
        for imp in info.imports:
            if imp in mods and imp != m:
                edges.add((m, imp))
    for a, b in sorted(edges):
        g.edge(a, b, color="#6e7781", arrowsize="0.6")

    g.render(out_path, cleanup=True)

def render_call_graph(mods: Dict[str, ModuleInfo], out_path: str):
    # Build a cross-file call graph by name matching (best-effort)
    func_index: Dict[str, Set[str]] = {}  # simple name -> fully qualified names
    for m, info in mods.items():
        for f in info.funcs:
            func_index.setdefault(f.name, set()).add(f.qualname)

    g = Digraph("calls", format="svg")
    g.attr(rankdir="LR", concentrate="true", splines="spline", nodesep="0.2", ranksep="0.7")
    g.attr("node", shape="ellipse", style="filled", fillcolor="#eef2ff", color="#c7d2fe", fontname="Inter,Helvetica,Arial", fontsize="9")

    # Only include functions that call or are called cross-file
    nodes: Set[str] = set()
    edges: Set[Tuple[str, str]] = set()

    for m, info in mods.items():
        for f in info.funcs:
            for cname in f.calls:
                targets = func_index.get(cname, set())
                for t in targets:
                    if t.split(".")[0] != m.split(".")[0]:  # heuristic cross-module
                        nodes.add(f.qualname)
                        nodes.add(t)
                        edges.add((f.qualname, t))

    for n in sorted(nodes):
        label = n
        g.node(n, label=label)

    for a, b in sorted(edges):
        g.edge(a, b, color="#64748b", arrowsize="0.5")

    g.render(out_path, cleanup=True)

def main():
    root = os.getcwd()
    mods = collect(root)
    render_module_graph(mods, os.path.join(DIAGRAM_DIR, "code_graph_modules"))
    render_call_graph(mods, os.path.join(DIAGRAM_DIR, "code_graph_calls"))
    print("Generated diagrams in:", DIAGRAM_DIR)

if __name__ == "__main__":
    main()
