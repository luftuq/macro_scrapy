import contextlib
import zipfile
from pathlib import Path

import polars as pl
import xlrd
from __init__ import current_year, folder_name, monthly_data_no_qy, parent_folder
from openpyxl import Workbook

zip_file = "Electricity.zip"
folder_path = fr"{parent_folder}\data\{folder_name}"
zip_file_path = fr"{parent_folder}\data\{folder_name}\input\{folder_name}_{zip_file}"

file_to_extract = "Rocni_zprava_o_trhu_2024_V0.xls"
destination_folder = fr"{parent_folder}\data\{folder_name}\input"

with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
    zip_ref.extract(file_to_extract, destination_folder)

book = xlrd.open_workbook(fr"{parent_folder}\data\{folder_name}\input\Rocni_zprava_o_trhu_2024_V0.xls")
sheet = xlrd.book.Book.sheet_by_name(book, sheet_name="VDT (EUR)")
new_workbook = Workbook()
new_sheet = new_workbook.active

for row in range(sheet.nrows):
    for col in range(sheet.ncols):
        new_sheet.cell(row=row+1, column=col+1).value = sheet.cell_value(row, col)

new_workbook.save(fr"{parent_folder}\data\{folder_name}\input\{folder_name}_Electricity.xlsx")
Path.unlink(fr"{parent_folder}\data\{folder_name}\input\Rocni_zprava_o_trhu_2024_V0.xls")

el_df = pl.read_excel(fr"{parent_folder}\data\{folder_name}\input\{folder_name}_Electricity.xlsx")
averages = list(filter(lambda x: x is not None, (el_df.select("_duplicated_35").to_series()).to_list()))
averages = averages[1:]

if (current_year % 4 == 0):
    indices = [722, 1418, 2162, 2881, 3624, 4343, 5086, 5829, 6548, 7291, 8010, 8753]
    indices2 = [745, 1441, 2184, 2904, 3647, 4366, 5109, 5852, 6571, 7314, 8033, 8776]
else:
    indices = [722, 1394, 2138, 2857, 3600, 4319, 5062, 5805, 6524, 7267, 7986, 8729]
    indices2 = [745, 1417, 2160, 2880, 3623, 4342, 5085, 5828, 6547, 7290, 8009, 8752]

ends_of_month =  []

for index, index2 in zip(indices, indices2):
        end_of_month_values = list(el_df[index:index2, 5])
        if None not in end_of_month_values:
            float_list = [float(x) for x in end_of_month_values]
            if (len(float_list) >= 1):
                average = sum(float_list)/len(float_list)
                ends_of_month.append(average)

historical_averages = [56.53, 51.06, 53.8, 60.88, 58.26, 73.83, 85.48, 85.66, 130.53, 142.1, 183.28, 233.31, 183, 157, 257, 173, 190, 237, 316, 485, 364, 174, 209, 255, 139, 143, 116, 109, 86, 99, 87, 94, 103, 96, 96, 76]
historical_ends_of_month = [45.56, 39.93, 59.92, 68.64, 68.1, 92.38, 54.36, 109.64, 116.71, 67.15, 188.88, 84.02, 201, 225, 210, 201, 210, 335, 317, 635, 354, 145, 375, 16, 144, 148, 99, 69, 85, 112, 73, 105, 91, 106, 168, 13]

def average_every_12(lst: list) -> list:
    for i in range(0, len(lst), 13):
        group = lst[i:i+12]
        group_average = sum(group)/len(group)
        lst.insert(i+12, group_average)

average_every_12(historical_averages)
average_every_12(historical_ends_of_month)

historical_averages.extend(averages)
historical_ends_of_month.extend(ends_of_month)

time_column = monthly_data_no_qy(3)
hist_avg = historical_averages + [0] * (len(time_column) - len(historical_averages))
hist_end = historical_ends_of_month + [0] * (len(time_column) - len(historical_ends_of_month))

for i in range(len(hist_avg)):
    if hist_avg[i] is not None:
        with contextlib.suppress(ValueError):
            hist_avg[i] = float(hist_avg[i])

for i in range(len(hist_end)):
    if hist_end[i] is not None:
        with contextlib.suppress(ValueError):
            hist_end[i] = float(hist_end[i])

final_df = pl.DataFrame({"Time": time_column, "Average": hist_avg, "End of month": hist_end})
final_df.write_excel(fr"{parent_folder}\data\{folder_name}\output\{folder_name}_Electricity.xlsx", worksheet = "Electricity")

