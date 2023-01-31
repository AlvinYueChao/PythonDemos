import winreg
import os


def find_unavailable_path(value: str) -> list:
    unavailable_paths = []
    for orig, curr in remove_placeholders(value.split(';')).items():
        if not os.path.exists(curr):
            unavailable_paths.append(orig)
    return unavailable_paths


def remove_placeholders(paths: list) -> dict:
    checked_placeholder = {}
    updated_paths_dict = {}
    for item in paths:
        item_str = str(item)
        if len(item_str.strip()) == 0:
            continue
        elif '%' in item_str:
            # todo %test1%\\%test2% case improvement
            first_index = item_str.index('%')
            last_index = item_str.rindex('%')
            placeholder = item_str[first_index + 1:last_index]
            if not placeholder in checked_placeholder:
                actual_path = os.getenv(placeholder)
                checked_placeholder[placeholder] = actual_path
            else:
                actual_path = checked_placeholder[placeholder]
            if actual_path:
                updated_paths_dict[item_str] = item_str.replace('%' + placeholder + '%', actual_path)
            else:
                updated_paths_dict[item_str] = item_str
        else:
            updated_paths_dict[item_str] = item_str
    return updated_paths_dict


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
    # unavailable_paths = find_unavailable_path(user_env_path_variables)
    # print(unavailable_paths)