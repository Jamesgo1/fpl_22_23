from visualizations import DataFramePathMaker, DataFrameConstructor, create_visual
import pickle


def test_data_frame_path_maker():
    df_maker = DataFramePathMaker("2021-22", "gws", "merged_gw.csv")
    df = df_maker.get_df_csv()
    assert not df.empty


class TestDataFrameConstructor:
    with open('mock_data/gws_df.pickle', 'rb') as handle:
        mock_df = pickle.load(handle)
    cols_to_keep = ["GW", "name", "team", "position", "xP", "value", "minutes"]
    sum_dict = {"xP": "sum", "value": "first"}
    sum_dict2 = {**sum_dict, "minutes": "sum"}

    def test_keep_cols(self):
        df_constructor = DataFrameConstructor(self.mock_df, self.sum_dict, *self.cols_to_keep)
        df_constructor.trim_unwanted_cols()
        assert set(df_constructor.df.columns) == set(self.cols_to_keep)

    def test_reduce_to_season(self):
        df_constructor = DataFrameConstructor(self.mock_df, self.sum_dict, *self.cols_to_keep)
        df_constructor.reduce_to_season()

    def test_filter_df(self):
        df_constructor = DataFrameConstructor(self.mock_df, self.sum_dict, *self.cols_to_keep)
        df_constructor.filter_df("position", "=", "FWD")

        dfc2 = DataFrameConstructor(self.mock_df, self.sum_dict2, *self.cols_to_keep)
        dfc2.reduce_to_season()
        dfc2.filter_df("minutes", ">", "2394")

    def test_group_df(self):
        dfc2 = DataFrameConstructor(self.mock_df, self.sum_dict2, *self.cols_to_keep)
        dfc2.reduce_to_season()
        dfc2.group_df("team")
        # dfc2.print_df()

    def test_add_df_score(self):
        dfc2 = DataFrameConstructor(self.mock_df, self.sum_dict2, *self.cols_to_keep)
        dfc2.reduce_to_season()
        dfc2.group_df("team")
        dfc2.add_diff_score()
        dfc2.print_df()