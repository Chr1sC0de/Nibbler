# -*- coding: utf-8 -*-
"""
Created on Sat Apr  6 13:59:28 2019

@author: cmamon
"""
# import ta
# import inspect
# import unidecode

# def _script_generator(func,function_name,module):
#     code       = inspect.getsource(func)
#     class_name = code.splitlines()[1].replace(' ','').replace('"','').replace('/','')
#     class_name = unidecode.unidecode(class_name)
#     list_of_lines = [
#     'from .class_Indicator import Indicator\n',
#     'import ta\n',
#     'class {}(Indicator):\n'.format(class_name),
#     '    def __init__(self,*args,**kwargs):\n',
#     '        self.function = ta.{}.{}\n'.format(module,function_name),
#     '        super({},self).__init__(*args,**kwargs)'.format(class_name)
#     ]

#     filename =  'subclass_'+ class_name + '.py'
#     with open(filename,'w') as filehande:
#         filehande.writelines(list_of_lines)

# function_names = [func for func in dir(ta.others)\
#                   if all(['__' not in func,
#                           'math' not in func,
#                           'np' not in func,
#                           'pd' not in func,
#                           'dropna' not in func,
#                           ])]

# for function_name in function_names:
#     func = getattr(ta.others,function_name)
#     _script_generator(func,function_name, 'others')
import ta
import pathlib as pt
import unidecode
import inspect
ta_modules = ["momentum", "volume", "trend", "others"]

illegal_functions = [
    "ema", "get_min_max", "sma"
]

cwd = pt.Path(__file__).parent

for module in ta_modules:

    module_folder = cwd/module

    if not module_folder.exists():
        module_folder.mkdir()

    init_file = module_folder/"__init__.py"

    if init_file.exists():
        init_file.unlink()

    f = open(init_file, "w")

    function_names = [
        func for func in dir(getattr(ta, module))
            if all(
                [
                    '__'  not in func,
                    'math' not in func,
                    'np' not in func,
                    'pd' not in func,
                    'dropna' not in func
                ]
            )
    ]
    lines = ["import ta\n"]
    lines.extend(["from .. import Indicator\n"])


    for function_name in function_names:
        if (all([function_name != function for function in illegal_functions])):
            if ("sma" in function_name):
                a = 10
            try:
                if ("Mixin" not in function_name):
                    func = getattr(getattr(ta, module), function_name)
                    if not inspect.isclass(func):
                        inspection = inspect.getfullargspec(func)
                        n_kwargs = len(inspection.defaults)
                        kwargs = inspection.args[-n_kwargs:]
                        indicator_line = f"{function_name}=Indicator(ta.{module}.{function_name}"
                        for kwarg, val in zip(kwargs, inspection.defaults):
                            indicator_line+=(", "+kwarg+"="+str(val))
                        indicator_line += ")\n"
                        lines.extend(
                            [
                                indicator_line
                            ]
                        )
            except:
                pass
    f.writelines(lines)
    f.close()