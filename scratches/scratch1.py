"""
Exploratory data analysis of player and team performance in FPL history.
"""
import pathlib


class DataCollector:
    """
    A general utility class for extracting the data - used in conjunction with other classes to create visualizations.

    Extracts the desired data from the Fantasy-Premier-League package and stores it as a dataframe for further
    processing.
    """

    def __init__(self, start_year: int = 2016, end_year: int = 2021):
        """

        :param start_year:
        :param end_year:
        """
        # Initialize params
        self.start_year = start_year
        self.end_year = end_year

        # Initialize encapsulated variables
        self.base_path = pathlib.Path.cwd() / r"Fantasy-Premier-League/data"
        self.current_path = None
        self.current_year = self.start_year

    def get_next_year_data(self):
        self.current_year += 1
        year_folder = self.current_year + "-" + str(self.current_year + 1)[-2:]
        return self.base_path / year_folder

    def get_data_type(self):
        pass

    def collect_all_data(self):
        """
        A cumulative class that gets data as specified in self.desired_data by using the above methods.
        :return:
        """
        pass


class PlayerDataCombination:
    """
    Combine stats across years.
    """

    def __init__(self, fpl_player_id, years="all"):
        self.years = years
        self.player_path = pathlib.Path.cwd() / r"Fantasy-Premier-League/data/"
