import ast
import astunparse

def is_recursive_call(node, function_name):
    # 检查是否存在函数自身的递归调用
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == function_name:
        return True
    for child in ast.iter_child_nodes(node):
        if is_recursive_call(child, function_name):
            return True
    return False

def is_dict_setitem(node):
    # 检查是否存在对字典的键值设定
    if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Subscript):
        return True
    for child in ast.iter_child_nodes(node):
        if is_dict_setitem(child):
            return True
    return False

def is_merge_like_function(node):
    # 检查是否存在递归调用和键值设定
    return is_recursive_call(node, node.name) and is_dict_setitem(node)

class MergeChecker(ast.NodeVisitor):
    def visit_FunctionDef(self, node):
        if is_merge_like_function(node):
            print(f"函数在代码行 {node.lineno} 可能有合并逻辑:\n")
            print(astunparse.unparse(node))
        self.generic_visit(node)

def check_for_merge_like(script):
    tree = ast.parse(script)
    checker = MergeChecker()
    checker.visit(tree)

# 输入的Python代码
code = """
def merge(src, dst):
    for k, v in src.items():
        if dst.get(k):
            if isinstance(v, dict):
                merge(v, dst.get(k))
            else:
                dst[k] = v
"""

check_for_merge_like(code)