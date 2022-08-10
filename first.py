"""
Just importing relevant libraries and making a first stab at creating a team using data
"""

import json
import pandas as pd
import pickle
import requests
from visualizations import CSVData


def get_data():
    """ Retrieve the fpl player data from the hard-coded url
    """
    response = requests.get("https://fantasy.premierleague.com/api/bootstrap-static/")
    if response.status_code != 200:
        raise Exception("Response was code " + str(response.status_code))
    response_str = response.text
    data = json.loads(response_str)
    return data


def update_pickle():
    fpl_data = get_data()
    with open('latest_api.pickle', 'wb') as handle:
        pickle.dump(fpl_data, handle, protocol=pickle.HIGHEST_PROTOCOL)


class ExcelFileAdder:
    """
    excel_types: ref, to_match
    """
    base_path = "matching_ids/"

    def __init__(self, df, file_name, excluded_clubs=()):
        self.df = df
        self.file_name = file_name
        self.excluded_clubs = excluded_clubs

        self.full_file_path = None

    def get_full_path(self, suffix):
        self.full_file_path = self.base_path + self.file_name + f"_{suffix}" + ".xlsx"

    def add_excel_matching_ref_file(self, suffix="ref"):
        self.get_full_path(suffix)
        current_df = self.df[["id_x", "full_name", "name_x"]].sort_values(["name_x", "full_name"]).reset_index(
            drop=True)
        current_df.to_excel(self.full_file_path)

    def add_excel_unmatched(self, suffix="unmatched"):
        self.get_full_path(suffix)
        current_df = self.df[
            self.df["full_name"].isnull() &
            ~self.df["name_x"].isin([*self.excluded_clubs])
            ]
        current_df = current_df[["team_y", "name_y"]]
        current_df = current_df.sort_values(["team_y", "name_y"]).reset_index(drop=True)
        current_df.to_excel(self.full_file_path)

    def add_all_files(self):
        self.add_excel_matching_ref_file()
        self.add_excel_unmatched()


# update_pickle()

def format_api_call(from_pickle=True, list_cols=False):
    if from_pickle:
        with open('latest_api.pickle', 'rb') as handle:
            all_data = pickle.load(handle)
    else:
        all_data = get_data()
        with open("latest_api.pickle", "wb") as handle:
            pickle.dump(all_data, handle)
    team_dict_list = all_data["teams"]
    team_dict_list = [{k: v for k, v in d.items() if k in ["id", "name"]} for d in team_dict_list]
    team_df = pd.DataFrame(team_dict_list)

    player_data_df = pd.DataFrame(all_data["elements"])
    player_data_df["full_name"] = player_data_df["first_name"] + " " + player_data_df["second_name"]
    player_data_df = player_data_df[["chance_of_playing_next_round", "cost_change_event", "ep_next", "ep_this",
                                     "event_points", "full_name", "id", "news", "news_added", "now_cost", "status",
                                     "team", "minutes"]]
    api_df = pd.merge(player_data_df, team_df, "inner", left_on="team", right_on="id")
    return api_df


csv_data = CSVData(group_by=("team", "name"))
df_csv = csv_data.create_df(print_df=False)
name_to_id = pd.read_csv(r"C:\Users\jgough\PycharmProjects\Fantasy-Premier-League\data\2021-22\player_idlist.csv")
name_to_id["full_name"] = name_to_id["first_name"] + " " + name_to_id["second_name"]
df_joined_csv_data = pd.merge(df_csv, name_to_id, "inner", left_on="name", right_on="full_name")
df_joined_csv_data = df_joined_csv_data.rename(columns={"id": "csv_id"})

df_api = format_api_call(from_pickle=True)

df_joined = pd.merge(df_api, df_joined_csv_data, "left", left_on="id_x", right_on="csv_id")
print(df_joined.to_string())
quit()
df_joined = df_joined[~df_joined["team_y"].isin(["Burnley", "Watford", "Norwich"])]

# df_id_join = pd.merge(df_joined, name_to_id, "outer", )

file_adder = ExcelFileAdder(df_joined, "beg_22_23", excluded_clubs=("Nott'm Forest", "Fulham", "Bournemouth"))
file_adder.add_all_files()

# for k, v in all_data["elements"].items():
#     print(k)
#     print(v)
#     print("-"*100)
