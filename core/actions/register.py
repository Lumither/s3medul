from core.utils import ensure_list


def copy(from_r: str, to_r: str):
    def func(wf_msg):
        wf_msg["registers"][to_r] = wf_msg["registers"][from_r]
        return wf_msg

    return func


def append(from_r: str, to_r: str):
    def func(wf_msg: dict):
        tmp = ensure_list(wf_msg["registers"][from_r])
        if to_r not in wf_msg['registers']:
            wf_msg['registers'][to_r] = tmp
        else:
            wf_msg["registers"][to_r] = ensure_list(wf_msg["registers"][to_r]) + tmp
        return wf_msg

    return func


def swap(from_r: str, to_r: str):
    def func(wf_msg):
        tmp = wf_msg["registers"][to_r]
        wf_msg["registers"][to_r] = wf_msg["registers"][from_r]
        wf_msg["registers"][from_r] = tmp
        return wf_msg

    return func


def move(from_r: str, to_r: str):
    def func(wf_msg):
        wf_msg["registers"][to_r] = wf_msg["registers"][from_r]
        wf_msg["registers"][from_r] = None
        return wf_msg

    return func


def func_reg_name(func, name=None) -> str:
    if name is None:
        return f"{func.__module__}.{func.__name__}"
    return f"{func.__module__}.{func.__name__}.{name}"


def get_reg(wf_msg, func, name, init_val=None):
    reg_list = wf_msg["registers"]
    reg_name = f"{func_reg_name(func)}.{name}"
    if reg_name not in reg_list:
        reg_list[reg_name] = init_val
    return reg_list[reg_name]
