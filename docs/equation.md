# class Var
name      |default| type
:---------|:------|:-----------  
`.var `   | `var` | sym.Symbol
`.val `   | `0`   | float
`.dig `   | `3`   | int
`.rm  `   | `''`  | str
`.array ` | `np.array([0])` | np.array
`.err   ` | `1`             | float
`.todiff` | `None`          | sym.Symbols of (pa_*func)/(pa_*.var)
`.diffed` | `None`          | diffed function of sym.Symbol by

function   | props
:----------|:------
`set_var`  | `(var=None, val=None, rm=None, dig=None):`
`set_array`| `(val):`
`df`       | `(df_name='', name=''):`
`latex`    | `(max=10, cp=True, nb=True):`

# class Eq
name       |default| type
:----------|:------|:-----------  
`.label`   | label  |
`.func`    | `None` |
`.todiff`  | `None` |
`.diffed`  | `None` |
`.subs_str`| `None` |
`.subs_val`| `None` |
`.subs_ans`| `None` |
`.syn_val` | `None` |
`.syn_ans` | `None` |
`.syn_rslt`| `None` |
`.eq`      | `sym.Eq(leq, req)` |
`.vars`    | `{}`   |
`.ans`     |` None` |
`.ans_val` | `0`    |
`.err_val` | `0`    |

function    | props
:-----------|:------
`latex`     | `(, cp=True, nb=True, rqs=[1]*5):`
`syn`       | `(, cp=True, nb=True, sub_val=True)`
`status`    | `()`
`set_tex`   | `(err=False)`
`ans_align` | `():`
`not_setting_obj` | `()`
