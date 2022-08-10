"""
The purpose of this file is to discover team-level insights such as how well each team performed relative to their
value.
"""

import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import re


# week_one_value = current_df[current_df["GW"] == 1]

class DataFramePathMaker:
    """
    Creates the DataFrame from the desired path.
    """
    root_path = r"C:\Users\jgough\PycharmProjects\Fantasy-Premier-League\data"

    def __init__(self, *directories):
        self.dir_list = directories
        self.current_path = Path(self.root_path)

    def get_full_path(self):
        for p in self.dir_list:
            self.current_path /= p

    def get_df_csv(self):
        self.get_full_path()
        return pd.read_csv(self.current_path)


class DataFrameConstructor:
    """
    Filtering and creation of desired columns and rows.
    """
    cols_to_keep = ["GW", "name", "team", "position", "xP", "value", "minutes"]
    summarise_dict = {"xP": "sum", "value": "first", "minutes": "sum"}
    reduce_season_cols = ["position", "team", "name"]

    def __init__(self, df):
        self.df = df

    def trim_unwanted_cols(self):
        self.df = self.df[list(self.cols_to_keep)]
        return self

    def print_df(self):
        print()
        print(self.df.to_string())

    def reduce_to_season(self):
        self.df = self.df.groupby(self.reduce_season_cols, as_index=False).agg(self.summarise_dict)
        return self

    def filter_df(self, *filter_params):
        if not filter_params:
            pass
        elif filter_params[1] == "=":
            self.df = self.df[self.df[filter_params[0]] == filter_params[2]]
        elif filter_params[1] == ">":
            less_than_int = int(filter_params[2])
            self.df = self.df[self.df[filter_params[0]] > less_than_int]
        else:
            print("ERROR")
            Exception()
        return self

    def group_df(self, *group_by_cols):
        agg_dict = {k: "mean" for k in self.summarise_dict.keys()}
        self.df = self.df.groupby(list(group_by_cols), as_index=False).agg(agg_dict)
        if [v for v in self.summarise_dict if v == "count"]:
            self.df = self.df.rename(columns={"minutes": "num_players"})
            self.df = self.df.sort_values(by="num_players")
        return self

    def add_diff_score(self):
        self.df["diff_score"] = self.df["xP"] / self.df["value"]
        self.df = self.df.sort_values(by="diff_score", ascending=False)
        return self

    def filter_by_row_num(self, max_rows=10):
        if max_rows > 0:
            self.df = self.df.iloc[:max_rows]
        return self


class DataVizProgrammer:
    """
    Allows you to customise the type of graphic you desire and the styling for that graphic.
    """

    def __init__(self, df, title=""):
        self.df = df
        self.title = title

    @staticmethod
    def set_options():
        """
        Choose overall custom designs and styles for visualizations - e.g. Tableau styling.
        :return:
        """
        mpl.style.use('seaborn')

    def create_scatter(self, x_lab="value", y_lab="xP", hue="team"):
        self.set_options()
        ax = sns.scatterplot(data=self.df, x=x_lab, y=y_lab, hue=hue)
        ax.set_title(self.title)
        for line in range(0, self.df.shape[0]):
            ax.text(self.df.value[line] + 0.01, getattr(self.df, y_lab)[line],
                    self.df.name[line], horizontalalignment='left',
                    size='x-small', color='black', weight='light')
        plt.show()

    def create_bar(self, *y_axes, x_axis="name"):
        self.set_options()

        self.df = self.df[[x_axis, *y_axes]]
        secondary_y = None
        if len(y_axes) > 1:
            secondary_y = list(y_axes)[1:]

        self.df.plot.bar(x=x_axis, secondary_y=secondary_y,
                         title=self.title)
        plt.show()


class CSVData:
    path_to_csv = ["2021-22", "gws", "merged_gw.csv"]

    def __init__(self, filter_by=(), group_by=(), x_axis="name", y_axes=None, max_rows=0):
        self.filter_by = filter_by
        self.group_by = group_by
        self.x_axis = x_axis
        self.y_axes = y_axes
        self.max_rows = max_rows

        self.df = None

    def create_df(self, print_df=True):
        df_maker = DataFramePathMaker(*self.path_to_csv)
        raw_df = df_maker.get_df_csv()

        df_constructor = DataFrameConstructor(raw_df)
        df_constructor \
            .trim_unwanted_cols() \
            .reduce_to_season() \
            .filter_df(*self.filter_by) \
            .group_df(*self.group_by) \
            .add_diff_score() \
            .filter_by_row_num(max_rows=self.max_rows)
        if print_df:
            df_constructor.print_df()
        self.df = df_constructor.df
        return self.df

    def make_graphic(self, graph_type="bar"):
        viz_prog = DataVizProgrammer(self.df)
        if graph_type == "bar":
            viz_prog.create_bar(*self.y_axes, x_axis=self.x_axis)
        else:
            viz_prog.create_scatter()


