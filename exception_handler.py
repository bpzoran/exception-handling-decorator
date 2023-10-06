from typing import List, Callable, Type, Tuple


class ExceptionHandler:

    def __init__(self, exception=Exception, handling_func=None,
                 reraise=True):
        self.handling_func = handling_func
        self.exceptions = exception
        self.reraise = reraise
        self.check_types()


    def __call__(self, func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except self.exceptions as ex:
                handling_func, reraise = self.get_handling_func_reraise(ex)
                if handling_func:
                    handling_func(ex)
                if reraise:
                    raise
        return wrapper

    def check_exception_types(self):
        if self.exceptions is None:
            self.exceptions = Exception
            return
        if isinstance(self.exceptions, type) and issubclass(self.exceptions, Exception):
            return
        if not isinstance(self.exceptions, tuple):
            self.set_all_to_default()
            return
        for ex in self.exceptions:
            if not (isinstance(ex, type) and issubclass(ex, Exception)):
                self.set_all_to_default()
                return
            
    def check_types(self):
        self.check_exception_types()
        self.check_type(self.handling_func, Callable)
        self.check_type(self.reraise, bool)
            
    def check_type(self, var_to_check, checking_type):
        if var_to_check is None or isinstance(var_to_check, checking_type):
            return
        if not isinstance(var_to_check, tuple):
            self.set_all_to_default()
            return
        for v in var_to_check:
            if not isinstance(v, checking_type):
                self.set_all_to_default()
                return

    def set_all_to_default(self):
        self.exceptions = Exception
        self.handling_func = None
        self.reraise = True


    def get_handling_func_reraise(self, ex: Exception) -> Tuple[Callable, bool]:
        handling_func = None
        reraise = True
        exception_index = -1
        if isinstance(self.exceptions, type(Exception)):
            exception_index = 0
        elif self.exceptions and ex:
            exception_index = self.exceptions.index(type(ex))
        if self.handling_func:
            if not isinstance(self.handling_func, tuple):
                handling_func = self.handling_func
            elif (not self.exceptions) or (exception_index >= 0 and len(self.handling_func) <= exception_index):
                handling_func = self.handling_func[-1]
            else:
                handling_func = self.handling_func[exception_index]
        if isinstance(self.reraise, bool):
            reraise = self.reraise
        elif isinstance(self.reraise, tuple):
            if (not self.exceptions) or (exception_index >= 0 and len(self.reraise) <= exception_index):
                reraise = self.reraise[-1]
            else:
                reraise = self.reraise[exception_index]
        return handling_func, reraise
