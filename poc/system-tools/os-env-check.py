import winreg
import os


def find_unavailable_path(value: str) -> list:
    unavailable_paths = []
    for item in remove_placeholders(value.split(';')):
        if len(item.strip()) == 0:
            continue
        else:
            if not os.path.exists(item):
                unavailable_paths.append(item)
    return unavailable_paths


def remove_placeholders(paths: list) -> list:
    checked_placeholder = {}
    for item in paths:
        item_str = str(item)
        if '%' in item_str:
            first_index = item_str.index('%')
            last_index = item_str.rindex('%')
            placeholder = str(item)[first_index + 1:last_index]
            # todo
    return []


if __name__ == '__main__':
    sys_env_reg_path = 'SYSTEM\CurrentControlSet\Control\Session Manager\Environment'
    sys_env_reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, sys_env_reg_path)
    sys_env_path_variables = winreg.QueryValueEx(sys_env_reg_key, 'Path')[0]
    # print(sys_env_path_variables)
    unavailable_paths = find_unavailable_path(sys_env_path_variables)
    print(unavailable_paths)

    # user_env_reg_path = 'Environment'
    # user_env_reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, user_env_reg_path)
    # user_env_path_variables = winreg.QueryValueEx(user_env_reg_key, 'Path')[0]
    # print(user_env_path_variables)