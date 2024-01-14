print("版本1.1")
#================导入运行方法库==================
import time
import winreg
import json
import os
import easygui
import vdf
# print("运行库导入完毕")

#================方法库==================
#读取json
def jsonfile():
    with open("config.json", 'r', encoding='utf-8') as file:
        return file.read()

json_data = jsonfile()
json_data1 = json.loads(json_data)

#修改注册表
def modify_registry_key(user):
    # 定义注册表路径
    key_path = r"Software\Valve\Steam"
    key_name = "AutoLoginUser"

    try:
        # 打开或创建注册表项
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)

        # 获取用户输入的值
        value_data = user

        # 设置注册表项的值
        winreg.SetValueEx(key, key_name, 0, winreg.REG_SZ, value_data)

        # print(f"已成功将注册表项 {key_path}\\{key_name} 的值设置为 {value_data}")

        # 关闭注册表项
        winreg.CloseKey(key)

    except Exception as e:
        print(f"发生错误: {e}")

#修改VDF
def vdf_to_json(vdf_content):
    vdf_data = vdf.loads(vdf_content)
    json_data = json.dumps(vdf_data, indent=2)
    return json_data

def json_to_vdf(json_data):
    data_dict = json.loads(json_data)
    vdf_content = vdf.dumps(data_dict)
    return vdf_content

def update_values(vdf_file_path, account_name, offline_mode_value):
    try:
        with open(vdf_file_path, "r", encoding="utf-8") as file:
            vdf_content = file.read()
    except FileNotFoundError:
        print(f"未找到指定的文件: {vdf_file_path}")
        return None

    json_data = vdf_to_json(vdf_content)

    data_dict = json.loads(json_data)
    for user_id, user_data in data_dict.get("users", {}).items():
        if "AccountName" in user_data and user_data["AccountName"] == account_name:
            user_data["MostRecent"] = 1
            user_data["WantsOfflineMode"] = offline_mode_value
            user_data["AllowAutoLogin"] = 1

    updated_vdf_content = vdf.dumps(data_dict)

    try:
        with open(vdf_file_path, "w", encoding="utf-8") as file:
            file.write(updated_vdf_content)
        # print(f"成功将更新后的VDF内容覆盖回文件: {vdf_file_path}")
    except FileNotFoundError:
        print(f"无法写入文件，未找到指定的文件: {vdf_file_path}")

#展示所有账号下拉框
def display_values(json_data):
    data = json.loads(json_data)
    user_dict = data.get("userName", {})
    values = list(user_dict.values())

    # 使用 easygui.choicebox 展示下拉框
    selected_value = easygui.choicebox("请选择您要登陆的steam账号", "选择框", choices=values)

    if selected_value:
        # 获取选中值对应的键
        selected_key = next((k for k, v in user_dict.items() if v == selected_value), None)
        if selected_key:
            return selected_key
        else:
            easygui.msgbox("您没有选择账号", "结果")

# print("方法库定义完毕")
#===================环境初始化===================
#读取vdf路径
vdf_file_path = json_data1['vdfPath']
#读取steam运行路径
exe_path = json_data1['runPath']

print("环境初始化完毕")
#==================主程序====================
# username = input("请输入你要登陆的用户账号")
username = display_values(json_data)
offline_mode_value = input("是否使用离线登陆(“0”代表“否”|“1”代表“是”)")
modify_registry_key(username)
print("steam登陆注册表修改完毕")
# 要匹配的AccountName值
account_name_to_match = username

# 要设置的 WantsOfflineMode 值
offline_mode_value = offline_mode_value

# 更新匹配的 AccountName 的 MostRecent 和 WantsOfflineMode 值
update_values(vdf_file_path, account_name_to_match, offline_mode_value)
print("steam登陆文件修改完毕")
print("即将启动steam.exe，请稍后...")
#延迟函数
time.sleep(3)
#执行启动steam
os.startfile(exe_path)
