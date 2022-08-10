import aiohttp
import asyncio
from fpl import FPL
from understat import Understat
from pathlib import Path

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def run_understat():
    async with aiohttp.ClientSession() as session:
        understat = Understat(session)
        data = await understat.get_league_players("epl", 2018, {"team_title": "Manchester United"})
        return json.dumps(data)


async def get_player(player_id):
    async with aiohttp.ClientSession() as session:
        fpl = FPL(session)
        player = await fpl.get_player(player_id, return_json=True)
        first_name = player["first_name"]
        second_name = player["second_name"]
        cost = player["now_cost"]
        return cost


def get_cost_now():
    data_path = Path.cwd().parent / "Fantasy-Premier-League" / "data"
    desired_path = data_path / "2022-23" / "player_idlist.csv"
    current_df = pd.read_csv(desired_path)
    id_list = list(current_df.id)
    all_player_info = []
    for player_id in id_list:
        cost = get_player(player_id)
        all_player_info.append(get_player(player_id))
    with open('api_player_data.pickle', 'wb') as handle:
        pickle.dump(all_player_info, handle)
