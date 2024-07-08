import json
import glob

def remove_entries_with_field_value(input_pattern, output_file, target_field, target_value):
    """
    删除指定字段具有特定值的记录，并将结果保存到新的JSON文件中。

    :param input_pattern: 输入JSON文件路径的模式（例如：'path/to/student_job_info_page_*.json'）
    :param output_file: 输出的JSON文件路径（例如：'path/to/filtered_data.json'）
    :param target_field: 要检查的目标字段（例如：'DWZZJGDM'）
    :param target_value: 要删除的目标值（例如：'916100009205248781'）
    """
    # 初始化一个列表来存储过滤后的数据
    filtered_data = []

    # 获取所有JSON文件路径
    file_paths = glob.glob(input_pattern)

    # 逐个读取文件并过滤数据
    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            # 过滤掉指定字段具有特定值的记录
            for entry in data:
                if entry.get(target_field) != target_value:
                    filtered_data.append(entry)

    # 将过滤后的数据写入新的JSON文件
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(filtered_data, file, ensure_ascii=False, indent=4)

    print(f"Filtered data has been saved to {output_file}")

# 示例调用
input_pattern = r'D:\xd_dataset\filtered_student_job_info_v2.json'
output_file = r'D:\xd_dataset\filtered_student_job_info_v2.json'
target_field = 'DWZZJGDM'
# 435230729、458398460、000000000、MA2GMU1A5、11654323010515673H
target_value = '11654323010515673H'

remove_entries_with_field_value(input_pattern, output_file, target_field, target_value)
