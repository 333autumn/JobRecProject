import csv
import json
import glob
from collections import defaultdict, Counter

def filter_student_job_info(input_pattern, output_file, target_byqxmc_values):
    """
    筛选出BYQXMC字段等于特定值的数据，并将结果保存到新的JSON文件中。

    :param input_pattern: 输入JSON文件路径的模式（例如：'path/to/student_job_info_page_*.json'）
    :param output_file: 输出的JSON文件路径（例如：'path/to/filtered_student_job_info.json'）
    :param target_byqxmc_values: 目标BYQXMC值的集合（例如：{"签就业协议形式就业", "其他录用证明就业", "签劳动合同就业", "签约中"}）
    """
    # 初始化一个列表来存储符合条件的数据
    filtered_data = []

    # 获取所有JSON文件路径
    file_paths = glob.glob(input_pattern)

    # 逐个读取文件并筛选数据
    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            # 筛选BYQXMC字段值符合条件的记录
            for entry in data:
                    filtered_data.append(entry)

    # 将筛选后的数据写入新的JSON文件
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(filtered_data, file, ensure_ascii=False, indent=4)

    print(f"Filtered data has been saved to {output_file}")

def remove_empty_fields(data, fields, invalid_values=None):
    """
    去除指定字段为空或为无效值的记录。

    :param data: 输入数据列表
    :param fields: 要检查的字段列表
    :param invalid_values: 要去除的无效值列表（例如：["无"]），默认为None
    :return: 去除指定字段为空或为无效值的记录后的数据列表
    """
    if invalid_values is None:
        invalid_values = []

    def is_valid(entry):
        for field in fields:
            value = entry.get(field)
            if not value or value in invalid_values:
                return False
        return True

    return [entry for entry in data if is_valid(entry)]

def extract_fields_from_json(input_pattern, output_file, fields_to_extract):
    """
    从JSON文件中提取指定字段并保存到新的JSON文件。

    :param input_pattern: 输入JSON文件路径的模式（例如：'path/to/student_job_info_page_*.json'）
    :param output_file: 输出的JSON文件路径（例如：'path/to/extracted_fields.json'）
    :param fields_to_extract: 要提取的字段列表（例如：['REALNAME', 'DEPARTMENT', 'BYQXMC']）
    """
    # 初始化一个列表来存储提取后的数据
    extracted_data = []

    # 获取所有JSON文件路径
    file_paths = glob.glob(input_pattern)

    # 逐个读取文件并提取数据
    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            # 提取指定字段
            for entry in data:
                extracted_entry = {field: entry.get(field) for field in fields_to_extract}
                extracted_data.append(extracted_entry)

    # 将提取后的数据写入新的JSON文件
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(extracted_data, file, ensure_ascii=False, indent=4)

    print(f"Extracted data has been saved to {output_file}")

def find_and_deduplicate_by_dwzzjgdm(input_pattern, output_file):
    """
    去重DWZZJGDM字段，并统计每个字段的不同值，选择出现次数最多的那个进行保存。

    :param input_pattern: 输入JSON文件路径的模式（例如：'path/to/student_job_info_page_*.json'）
    :param output_file: 输出的JSON文件路径（例如：'path/to/deduplicated_data.json'）
    """
    # 要处理的字段
    fields_to_process = ['DWZZJGDM', 'SJDWMC', 'DWXZMC', 'DWHYMC', 'GZZWLBMC', 'DWSZDDM']

    # 初始化一个字典来存储去重后的数据
    deduplicated_data = defaultdict(lambda: defaultdict(Counter))

    # 获取所有JSON文件路径
    file_paths = glob.glob(input_pattern)

    # 逐个读取文件并处理数据
    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            for entry in data:
                dwzzjgdm = entry.get('DWZZJGDM')
                if dwzzjgdm:
                    for field in fields_to_process:
                        value = entry.get(field)
                        if value is not None:
                            value = value.strip()
                            if value:
                                deduplicated_data[dwzzjgdm][field][value] += 1

    # 构建去重后的数据列表
    deduplicated_list = []
    for dwzzjgdm, field_counters in deduplicated_data.items():
        deduplicated_entry = {'DWZZJGDM': dwzzjgdm}
        for field, counter in field_counters.items():
            most_common_value, _ = counter.most_common(1)[0]
            deduplicated_entry[field] = most_common_value
        deduplicated_list.append(deduplicated_entry)

    # 将去重后的数据写入新的JSON文件
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(deduplicated_list, file, ensure_ascii=False, indent=4)

    print(f"Deduplicated data has been saved to {output_file}")

def extract_sid_and_dwzzjgdm(input_pattern, output_file):
    """
    提取每条数据的SID和DWZZJGDM，并增加一个字段satisfied（值全1），保存到新的JSON文件中。

    :param input_pattern: 输入JSON文件路径的模式（例如：'path/to/student_job_info_page_*.json'）
    :param output_file: 输出的JSON文件路径（例如：'path/to/extracted_data.json'）
    """
    # 初始化一个列表来存储提取后的数据
    extracted_data = []

    # 获取所有JSON文件路径
    file_paths = glob.glob(input_pattern)

    # 逐个读取文件并提取数据
    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            for entry in data:
                sid = entry.get('SID')
                dwzzjgdm = entry.get('DWZZJGDM')
                if sid and dwzzjgdm:
                    extracted_entry = {
                        'SID': sid,
                        'DWZZJGDM': dwzzjgdm,
                        'satisfied': 1
                    }
                    extracted_data.append(extracted_entry)

    # 将提取后的数据写入新的JSON文件
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(extracted_data, file, ensure_ascii=False, indent=4)

    print(f"Extracted data has been saved to {output_file}")

def check_dwzzjgdm_correspondence(user_file, job_file):
    """
    检查user_file中的DWZZJGDM是否都能在job_file中的DWZZJGDM找到对应值。

    :param user_file: 用户数据的JSON文件路径（例如：'path/to/xdu_dataset_user.json'）
    :param job_file: 工作数据的JSON文件路径（例如：'path/to/xdu_dataset_job_v2.json'）
    """
    # 读取用户数据文件
    with open(user_file, 'r', encoding='utf-8') as file:
        user_data = json.load(file)

    # 读取工作数据文件
    with open(job_file, 'r', encoding='utf-8') as file:
        job_data = json.load(file)

    # 提取工作数据中的DWZZJGDM
    job_dwzzjgdm_set = {entry.get('DWZZJGDM') for entry in job_data if entry.get('DWZZJGDM')}

    # 检查用户数据中的DWZZJGDM是否在工作数据中存在
    missing_dwzzjgdm = []
    for entry in user_data:
        dwzzjgdm = entry.get('DWZZJGDM')
        if dwzzjgdm and dwzzjgdm not in job_dwzzjgdm_set:
            missing_dwzzjgdm.append(dwzzjgdm)

    if missing_dwzzjgdm:
        print(f"Missing DWZZJGDM in job dataset: {missing_dwzzjgdm}")
    else:
        print("All DWZZJGDM values in user dataset are present in job dataset.")

def json_to_csv(json_file, csv_file):
    """
    将JSON文件转换为CSV文件。

    :param json_file: 输入的JSON文件路径
    :param csv_file: 输出的CSV文件路径
    """
    # 读取JSON文件
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # 获取字段名称（假设所有记录都有相同的字段）
    fieldnames = data[0].keys()

    # 写入CSV文件
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for entry in data:
            writer.writerow(entry)

    print(f"Data has been converted to {csv_file}")

# 示例调用
input_pattern = 'D:/xd_dataset/utf-8/student_job_info_page_*_utf-8.json'
output_file = 'D:/xd_dataset/filtered_student_job_info.json'
output_file_v2 = 'D:/xd_dataset/filtered_student_job_info_v2.json'
target_byqxmc_values = {"签就业协议形式就业", "其他录用证明就业", "签劳动合同就业", "签约中"}

'''1、筛选出BYQXMC字段等于特定值的数据，并将结果保存到新的JSON文件中'''
# filter_student_job_info(input_pattern, output_file, target_byqxmc_values)

'''2、去除DWZZJGDM和SJDWMC字段为空的记录'''
# # 读取筛选后的临时数据
# with open(output_file, 'r', encoding='utf-8') as file:
#     temp_data = json.load(file)
#
# invalid_values = ["无"]
#
# # 去除DWZZJGDM和SJDWMC字段为空的记录
# final_filtered_data = remove_empty_fields(temp_data, ['DWZZJGDM', 'SJDWMC'],invalid_values)
#
# # 将最终筛选后的数据写入最终的输出文件
# with open(output_file_v2, 'w', encoding='utf-8') as file:
#     json.dump(final_filtered_data, file, ensure_ascii=False, indent=4)

'''3、提取用户表、工作表、交互表'''
# 3.1 提取用户表
# fields_to_extract_user = ['SID', 'REALNAME', 'GRADE','DEPARTMENT','MAJOR','ZYFX','XBMC',
#                           'ZXWYYZMC','BIRTHDAY','XLMC','XXXSMC','JTDZ','GZZWLBMC']
# output_file_user = 'D:/xd_dataset/xdu_dataset_user.json'
# extract_fields_from_json(output_file_v2, output_file_user, fields_to_extract_user)

# 3.2.1 提取工作表
# fields_to_extract_job = ['DWZZJGDM', 'SJDWMC', 'DWXZMC', 'DWHYMC','GZZWLBMC','DWSZDDM']
# output_file_job = 'D:/xd_dataset/xdu_dataset_job.json'
# extract_fields_from_json(output_file_v2, output_file_job, fields_to_extract_job)

# 3.2.2 对同一ID对应不同公司的数据进行处理（取出现频率最高的公司名进行替换）
# fields_to_extract_job_v2 = ['DWZZJGDM', 'SJDWMC', 'DWXZMC', 'DWHYMC','GZZWLBMC','DWSZDDM']
# output_file_job_v2 = 'D:/xd_dataset/xdu_dataset_job_v2.json'
# find_and_deduplicate_by_dwzzjgdm(output_file_v2, output_file_job_v2)

# 3.3 提取交互表
# output_file_action = 'D:/xd_dataset/xdu_dataset_action.json'
# extract_sid_and_dwzzjgdm(output_file_v2, output_file_action)

# check_dwzzjgdm_correspondence(output_file_action, output_file_job_v2)

'''4、转换成csv文件'''
json_user = 'D:/xd_dataset/xdu_dataset_user.json'
json_job = 'D:/xd_dataset/xdu_dataset_job_v2.json'
json_action = 'D:/xd_dataset/xdu_dataset_action.json'

csv_user = 'D:/xd_dataset/xdu_dataset_user.csv'
csv_job = 'D:/xd_dataset/xdu_dataset_job.csv'
csv_action = 'D:/xd_dataset/xdu_dataset_action.csv'

# json_to_csv(json_user, csv_user)
json_to_csv(json_job, csv_job)
json_to_csv(json_action, csv_action)