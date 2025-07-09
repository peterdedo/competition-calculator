AttributeError: 'PandasThen' object has no attribute '_evaluate_output_names'
Traceback:

File "/Users/administrator/Documents/Cursor/4ct_project/.venv/lib/python3.9/site-packages/streamlit/runtime/scriptrunner/exec_code.py", line 128, in exec_func_with_error_handling
    result = func()
File "/Users/administrator/Documents/Cursor/4ct_project/.venv/lib/python3.9/site-packages/streamlit/runtime/scriptrunner/script_runner.py", line 669, in code_to_exec
    exec(code, module.__dict__)  # noqa: S102
File "/Users/administrator/Documents/Cursor/4ct_project/app.py", line 578, in <module>
    fig_sunburst = px.sunburst(
File "/Users/administrator/Documents/Cursor/4ct_project/.venv/lib/python3.9/site-packages/plotly/express/_chart_types.py", line 1761, in sunburst
    return make_figure(
File "/Users/administrator/Documents/Cursor/4ct_project/.venv/lib/python3.9/site-packages/plotly/express/_core.py", line 2493, in make_figure
    args = process_dataframe_hierarchy(args)
File "/Users/administrator/Documents/Cursor/4ct_project/.venv/lib/python3.9/site-packages/plotly/express/_core.py", line 2051, in process_dataframe_hierarchy
    df.group_by(path[i:], drop_null_keys=True)
File "/Users/administrator/Documents/Cursor/4ct_project/.venv/lib/python3.9/site-packages/narwhals/dataframe.py", line 2388, in pipe
    return super().pipe(function, *args, **kwargs)
File "/Users/administrator/Documents/Cursor/4ct_project/.venv/lib/python3.9/site-packages/narwhals/dataframe.py", line 134, in pipe
    return function(self, *args, **kwargs)
File "/Users/administrator/Documents/Cursor/4ct_project/.venv/lib/python3.9/site-packages/plotly/express/_core.py", line 2036, in post_agg
    return dframe.with_columns(
File "/Users/administrator/Documents/Cursor/4ct_project/.venv/lib/python3.9/site-packages/narwhals/dataframe.py", line 2560, in with_columns
    return super().with_columns(*exprs, **named_exprs)
File "/Users/administrator/Documents/Cursor/4ct_project/.venv/lib/python3.9/site-packages/narwhals/dataframe.py", line 152, in with_columns
    return self._with_compliant(self._compliant_frame.with_columns(*compliant_exprs))
File "/Users/administrator/Documents/Cursor/4ct_project/.venv/lib/python3.9/site-packages/narwhals/_pandas_like/dataframe.py", line 441, in with_columns
    columns = self._evaluate_into_exprs(*exprs)
File "/Users/administrator/Documents/Cursor/4ct_project/.venv/lib/python3.9/site-packages/narwhals/_compliant/dataframe.py", line 420, in _evaluate_into_exprs
    return list(chain.from_iterable(self._evaluate_into_expr(expr) for expr in exprs))  # pyright: ignore[reportArgumentType]
File "/Users/administrator/Documents/Cursor/4ct_project/.venv/lib/python3.9/site-packages/narwhals/_compliant/dataframe.py", line 420, in <genexpr>
    return list(chain.from_iterable(self._evaluate_into_expr(expr) for expr in exprs))  # pyright: ignore[reportArgumentType]
File "/Users/administrator/Documents/Cursor/4ct_project/.venv/lib/python3.9/site-packages/narwhals/_compliant/dataframe.py", line 432, in _evaluate_into_expr
    aliases = expr._evaluate_aliases(self)
File "/Users/administrator/Documents/Cursor/4ct_project/.venv/lib/python3.9/site-packages/narwhals/_compliant/expr.py", line 254, in _evaluate_aliases
    names = self._evaluate_output_names(frame)
