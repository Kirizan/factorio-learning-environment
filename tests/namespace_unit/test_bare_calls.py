"""Bare call statements in agent code (no Factorio server needed)."""

import ast

from fle.env.namespace import FactorioNamespace


def run(code: str) -> list[str]:
    logged: list[str] = []

    class FakeNamespace:
        capture_whole_output = False
        line_value = 0

        def log(self, value):
            logged.append(str(value))

    ns = FakeNamespace()
    eval_dict = {"__builtins__": __builtins__}
    for node in ast.parse(code).body:
        FactorioNamespace.execute_node(ns, node, eval_dict)
    return logged


def test_undefined_bare_call_raises():
    try:
        run("not_a_tool()")
    except NameError as e:
        assert "not_a_tool" in str(e)
    else:
        raise AssertionError("undefined bare call was silently skipped")


def test_builtin_bare_call_works():
    run("sorted([3, 1, 2])")
