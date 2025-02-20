import subprocess

# 定义年份范围
years = range(2000, 2024)  # 2021年到2024年

# 基础路径
input_base_path = "./data/input/ERA5/ERA5_{}.csv"
output_base_path = "./data/input/ERA5/ERA5_{}.nc"
static_path = "./data/static/KQGR.nc"

# 遍历每一年
for year in years:
    # 动态生成输入文件路径
    input_file = input_base_path.format(year)
    output_file = output_base_path.format(year)
    
    # 动态设置开始日期和结束日期
    start_date = f"{year}0101"  # 每年的1月1日
    end_date = f"{year+1}0102"    # 每年的12月31日
    
    # 构建命令
    command = [
        "python", "-m", "cosipy.utilities.aws2cosipy.aws2cosipy",
        "-i", input_file,
        "-o", output_file,
        "-s", static_path,
        "-b", start_date,
        "-e", end_date
    ]
    
    # 打印命令（可选，用于调试）
    print("Executing command for {}:".format(year))
    
    # 执行命令
    result = subprocess.run(command, capture_output=True, text=True)
    
    # 检查命令执行结果
    if result.returncode == 0:
        print(f"Successfully processed year {year}.")
    else:
        print(f"Error processing year {year}:")
        print(result.stderr)