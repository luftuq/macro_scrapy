"""Main module for processing electricity data."""
from pathlib import Path
from __init__ import ExcelHandler, input_path, output_path, input_folder

class Gas:
    """A class to process Gas prices data from an Excel file within a zip."""

    def __init__(self):
        """Initialize Gas with necessary attributes."""
        self.output_file = '{0}Gas.xlsx'.format(output_path)
        self.input_file = '{0}Gas.zip'.format(input_path)
        self.file_to_extract = "Rocni_zprava_o_trhu_plyn_2024_V0.xls"
        self.input_file_xls = input_folder + self.file_to_extract
        self.input_file_xlsx = Path(self.input_file_xls).with_suffix('.xlsx')
        self.excel_handler = ExcelHandler()

    def run_it_all(self):
        self.excel_handler.extract_zipfile(self.input_file, self.file_to_extract, input_folder)
        self.excel_handler.convert_xls_to_xlsx(self.input_file_xls, self.input_file_xlsx)
        self.excel_handler.read_data(
            excel_stream=self.input_file_xlsx,
            sheet_name='VDT',
            skip_rows=5, 
            has_header=True,
            )
#        self.process_data()
        self.excel_handler.write_data(output_file=self.output_file)

if __name__ == '__main__':
    Gas().run_it_all()