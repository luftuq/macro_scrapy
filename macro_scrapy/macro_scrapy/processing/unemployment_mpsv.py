import zipfile
from pathlib import Path

import polars as pl
from __init__ import folder_name, parent_folder

zip_file = "Unemployment_MPSV.zip"
folder_path = fr"{parent_folder}\data\{folder_name}"
zip_file_path = fr"{parent_folder}\data\{folder_name}\input\{folder_name}_{zip_file}"

# Name of the file you want to extract - MIGHT CHANGE as it often does (MPSV...),
# in case there is a change to the name, just rename it here too
file_to_extract = "2. Nez 2022_2024.xlsx"
destination_folder = fr"{parent_folder}\data\{folder_name}\input"

# Open the zip file and extract the specific file
with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
    zip_ref.extract(file_to_extract, destination_folder)

# Get the path of the extracted file and rename it to your liking
extracted_file_path = Path(destination_folder) / file_to_extract
new_file_name = fr"{folder_name}_Unemployment_MPSV.xlsx"
new_file_path = Path(destination_folder) / new_file_name
Path.rename(extracted_file_path, new_file_path)

mpsv_df = pl.read_excel(fr"{parent_folder}\data\{folder_name}\input\{folder_name}_Unemployment_MPSV.xlsx", sheet_name="List1")

# Transforming the data for Unemployed and Vacancies information
def unemployed_vacancies(df: pl.DataFrame) -> pl.DataFrame:
    initial_df = pl.DataFrame(df)

    df_transposed = initial_df.transpose()
    df_transformed = df_transposed.drop("column_2")
    df_transformed = df_transformed.slice(1,len(df_transformed)-1)

    month_names = ["January", "February", "March", "April", "May", "June",
                   "July", "August", "September", "October", "November", "December"]
    num_years = len(df_transformed) // 12
    last_year_rows = len(df_transformed) % 12

    years = pl.Series([year for year in range(1991, 1991 + num_years) for _ in range(12)])
    years.extend(pl.Series([1991 + num_years] * last_year_rows))

    months = pl.Series([month_names[(month - 1) % 12] for month in range(1, len(df_transformed) + 1)])
    df_final = df_transformed.with_columns(year=years, month=months)
    df_final.columns = ["Unemployed", "Vacancies", "Year", "Month"]
    df_final.write_excel(fr"{parent_folder}\data\{folder_name}\output\{folder_name}_UnemployedVacancies.xlsx", worksheet = "UnemployedVacancies")

unemployed_vacancies(mpsv_df)
