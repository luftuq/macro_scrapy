"""Output for IndEvo calculation."""
from __init__ import ExcelHandler, input_path, output_path


class IndEvo:
    """A class to handle the processing of IndEvo data."""

    def __init__(self, freq: str, columns_to_skip: int) -> None:
        """Initialize the IndEvo class.

        Args:
            freq: Any number of lists of strings.
            columns_to_skip: Number of columns to skip when loading df
        """
        self.freq = freq
        self.columns_to_skip = columns_to_skip

        self.input_file = '{0}IndustrialEvolution_{1}.xlsx'.format(
            input_path, self.freq,
            )
        self.output_file = '{0}IndustrialEvolution_{1}.xlsx'.format(
            output_path, self.freq,
            )
        self.excel_handler = ExcelHandler()

    def process_data(self) -> 'IndEvo':
        """Process the data.

        Slice the data, transpose the sliced dataframe and choose column names.

        Returns:
            IndEvo: An instance of the IndEvo class.
        """
        df = self.excel_handler.df
        df[0, 2] = 'Time'
        df[1, 2] = 'Průmysl celkem'
        column_names = df[:, 2]
        column_names = column_names.to_list()
        column_names = column_names[:-1]
        df = df[:35, columns_to_skip:]
        df = df.transpose(
            include_header=False,
            column_names=column_names,
        )
        self.excel_handler.df = df
        return self

    def run_it_all(self) -> None:
        """Execute all the steps to process the industrial evolution data."""
        self.excel_handler.read_data(
            excel_stream=self.input_file,
            sheet_name='Sheet1',
            skip_rows=7,
            has_header=False,
            )
        self.process_data()
        self.excel_handler.write_data(output_file=self.output_file)


if __name__ == '__main__':
    freq_columns_to_skip = [
        ('M', 3),
        ('Q', 3),
        ('Y', 4),
        ]

    for freq, columns_to_skip in freq_columns_to_skip:
        IndEvo(freq, columns_to_skip).run_it_all()
