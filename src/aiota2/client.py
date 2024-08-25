from datamodel import DataModel, DataArray
from exceptions import *
from urllib.parse import urlencode
import aiohttp


class AioClient:
    def __init__(self, with_models: bool = True, api_key: str = None, url: str = "https://api.opendota.com") -> None:
        """
        **aiotA2** - Asynchronous OPENDOTA API interface\n
        *Main class that provides API methods of OPENDOTA API.*\n
        Every API method can return dict and list | DataModel and DataArray object. To switch return type change **with_models** argument.

        *Also check query params at main documentation https://docs.opendota.com/*

        Arguments:
            with_models (bool): If True, methods will return DataModel objects, else dicts.
            api_key (str): Api Key for Open Dota API
            url (str): Change it, if you using another url. ?

        Examples:
            >>> answer = Client(with_models=False).get_player(account_id=...)
            answer = {...}
            >>> answer["rank_tier"]
            1
            ------------------------------
            >>> answer = Client(with_models=False).get_player(account_id=...)
            answer = DataModel({...})
            >>> answer.rank_tier
            1
        """

        self.api_key = api_key
        self.with_models = with_models
        self.url = url


    async def provide(self, path_with_args, retname, /, params={}) -> DataModel | dict:
        async with aiohttp.ClientSession() as session:
            
            # Api Key
            if self.api_key:
                session.headers['Authorization'] = f'Bearer {self.api_key}'

            async with session.get(self.url + path_with_args + "?" + urlencode(params)) as ans: 
                ans = await ans.json()

                if "error" in ans:
                    raise OpenDotaAPIError(ans["error"])

                if not self.with_models:
                    return ans

                if type(ans) is dict:
                    return DataModel(retname, ans)
                elif type(ans) is list:
                    return DataArray(map(lambda x: DataModel(retname, x), ans))


    def with_hero_attr(func):
        """DECORATOR THAT REQUIRES LOADED HEROES ATTRIBUTE, ALSO FUNC MUST BE SYNC!!!"""
        def wrap(self, *args, **kwargs):
            try: 
                getattr(self, "heroes")
                return func(self, *args, **kwargs)
            except AttributeError:
                raise ConstantsError("\n\nAioClient attribute \"heroes\" didn\'t load, use await AioClient().load_heroes()")
        
        return wrap


    async def load_heroes(self):
        """
        Load constant - heroes from Dota 2\n
        In more details, set attribute \"heroes\" to AioClient object.\n
        That give you ability to access the dota heroes base without sending a request to API many times, just use object attribute \"heroes\"

        Returns:
            self (AioClient object):
        """
        setattr(self, "heroes", await self.provide("/api/heroes", "Hero"))

        return self


    

    @with_hero_attr
    def get_heroes_by_param(self, param: str, value) -> DataModel | dict | None:
        """
        Requires loaded heroes attribute *

        Returns a list | DataArray of hero DataModel | Dict with given parametr
        """
        if self.with_models:
            ft = list(filter(lambda x: x.raw_json[param] == value, self.heroes))
            return ft
        else:
            ft = list(filter(lambda x: x[param] == value, self.heroes))
            return ft
        

    @with_hero_attr
    def get_hero_by_param(self, param: str, value) -> DataModel | dict | None:
        """
        Requires loaded heroes attribute *

        Returns a first hero DataModel | Dict with given parametr or None if it doesn\'t exists
        """
        if self.with_models:
            ft = list(filter(lambda x: x.raw_json[param] == value, self.heroes))
            if ft:
                return ft[0]
            else:
                return None  
        else:
            ft = list(filter(lambda x: x[param] == value, self.heroes))
            if ft:
                return ft[0]
            else:
                return None


    @with_hero_attr
    def get_heroes_names(self):
        """
        Requires loaded heroes attribute *

        Returns a list with every hero localized name
        """
        return list(map(lambda x: x.localized_name if self.with_models else x["localized_name"], self.heroes))  


    # Players
    async def get_player(self, account_id: int):
        "Player data"
        return await self.provide(f"/api/players/{account_id}", "Player")    

    async def get_player_wl(self, account_id: int, /, **query_params):
        "Win/Loss count"
        return await self.provide(f"/api/players/{account_id}/wl", "Player_WL", query_params)    

    async def get_player_recent_matches(self, account_id: int):
        "Recent matches played"
        return await self.provide(f"/api/players/{account_id}/recentMatches", "Match")
    
    async def get_player_matches(self, account_id: int, /, **query_params):
        "Matches played"
        return await self.provide(f"/api/players/{account_id}/matches", "Match", query_params)
    
    async def get_player_heroes(self, account_id: int, /, **query_params):
        "Heroes played"
        return await self.provide(f"/api/players/{account_id}/heroes", "Hero", query_params)
    
    async def get_player_peers(self, account_id: int, /, **query_params):
        "Players played with"
        return await self.provide(f"/api/players/{account_id}/peers", "Player", query_params)
    
    async def get_player_pros(self, account_id: int, /, **query_params):
        "Pro players played with"
        return await self.provide(f"/api/players/{account_id}/pros", "Pro_Player", query_params)
    
    async def get_player_totals(self, account_id: int, /, **query_params):
        "Totals in stats"
        return await self.provide(f"/api/players/{account_id}/totals", "Total", query_params)
    
    async def get_player_counts(self, account_id: int, /, **query_params):
        "Counts in categories"
        return await self.provide(f"/api/players/{account_id}/counts", "Count", query_params)

    async def get_player_histograms(self, account_id: int, field: str, /, **query_params):
        "Distribution of matches in a single stat"
        return await self.provide(f"/api/players/{account_id}/histograms/{field}", "Distribution", query_params)
    
    async def get_player_wardmap(self, account_id: int, /, **query_params):
        "Wards placed in matches played"
        return await self.provide(f"/api/players/{account_id}/wardmap", "Wardmap", query_params)
    
    async def get_player_wordcloud(self, account_id: int, /, **query_params):
        "Words said/read in matches played"
        return await self.provide(f"/api/players/{account_id}/wordcloud", "Word", query_params)
    
    async def get_player_ratings(self, account_id: int):
        "Player rating history"
        return await self.provide(f"/api/players/{account_id}/ratings", "Rating")
    
    async def get_player_rankings(self, account_id: int):
        "Player hero rankings"
        return await self.provide(f"/api/players/{account_id}/rankings", "Ranking")
    
    async def search_player_by_personaname(self, **query_params):
        "Search players by personaname"
        return await self.provide(f"/api/search", "Ranking", query_params)
    
    async def refresh_player(self, account_id: int) -> None: # Post
        "Refresh player match history"
        async with aiohttp.ClientSession() as session:
            await session.post(self.url + f"/api/players/{account_id}/refresh")
    

    # Pro
    async def get_pro_players(self):
        "Get list of pro players"
        return await self.provide(f"/api/proPlayers", "Pro_Player")

    async def get_pro_matches(self, **query_params):
        "Get list of pro matches"
        return await self.provide(f"/api/proMatches", "Pro_Match", query_params)
    

    # Matches
    async def get_match(self, match_id: int):
        "Match data"
        return await self.provide(f"/api/matches/{match_id}", "Match")
    
    async def get_public_matches(self, **query_params):
        "Get list of randomly sampled public matches"
        return await self.provide(f"/api/publicMatches", "Match", query_params)
    
    async def get_parsed_matches(self, **query_params):
        "Get list of parsed match IDs"
        return await self.provide(f"/api/parsedMatches", "Match", query_params)
    
    async def find_matches(self, **query_params):
        "Finds recent matches by heroes played"
        return await self.provide(f"/api/findMatches", "Match", query_params)
    

    # Heroes
    async def get_heroes(self):
        "Get hero data"
        return await self.provide(f"/api/heroes", "Hero")

    async def get_hero_matches(self, hero_id: int):
        "Get recent matches with a hero"
        return await self.provide(f"/api/heroes/{hero_id}/matches", "Match")
    
    async def get_hero_matchups(self, hero_id: int):
        "Get results against other heroes for a hero"
        return await self.provide(f"/api/heroes/{hero_id}/matchups", "Matchup")
    
    async def get_hero_durations(self, hero_id: int):
        "Get hero performance over a range of match durations"
        return await self.provide(f"/api/heroes/{hero_id}/durations", "Duration")
    
    async def get_hero_players(self, hero_id: int):
        "Get players who have played this hero"
        return await self.provide(f"/api/heroes/{hero_id}/players", "Player")
    
    async def get_hero_item_popularity(self, hero_id: int):
        "Get item popularity of hero categoried by start, early, mid and late game, analyzed from professional games"
        return await self.provide(f"/api/heroes/{hero_id}/itemPopularity", "Item")
    
    async def get_hero_stats(self):
        "Get stats about hero performance in recent matches"
        return await self.provide(f"/api/heroStats", "Statistic")


    # Leagues
    async def get_leagues(self):
        "Get league data"
        return await self.provide(f"/api/leagues", "League")
    
    async def get_league(self, league_id: int):
        "Get data for a league"
        return await self.provide(f"/api/leagues/{league_id}", "League")
    
    async def get_league_matches(self, league_id: int):
        "Get matches for a team"
        return await self.provide(f"/api/leagues/{league_id}/matches", "Match")
    
    async def get_league_teams(self, league_id: int):
        "Get teams for a league"
        return await self.provide(f"/api/leagues/{league_id}/teams", "Team")


    # Teams
    async def get_teams(self, **query_params):
        "Get team data"
        return await self.provide(f"/api/teams", "Team", query_params)
    
    async def get_team(self, team_id: int):
        "Get data for a team"
        return await self.provide(f"/api/teams/{team_id}", "Team")
    
    async def get_team_matches(self, team_id: int):
        "Get matches for a team"
        return await self.provide(f"/api/teams/{team_id}/matches", "Match")
    
    async def get_team_players(self, team_id: int):
        "Get players who have played for a team"
        return await self.provide(f"/api/teams/{team_id}/players", "Player")
    
    async def get_team_heroes(self, team_id: int):
        "Get heroes for a team"
        return await self.provide(f"/api/teams/{team_id}/heroes", "Hero")


    # ...
    async def get_explorer(self):
        "Submit arbitrary SQL queries to the database"
        return await self.provide(f"/api/explorer", "...")

    async def get_distributions(self):
        "Distributions of MMR data by bracket and country"
        return await self.provide(f"/api/distributions", "Ranks")
    
    async def get_rankings(self, **query_params):
        "Top players by hero"
        return await self.provide(f"/api/rankings", "Ranking", query_params)
    
    async def get_benchmarks(self, **query_params):
        "Benchmarks of average stat values for a hero"
        return await self.provide(f"/api/benchmarks", "Benchmark", query_params)
    
    async def check_status(self):
        "Get current service statistics"
        return await self.provide(f"/api/status", "...")
    
    async def check_health(self):
        "Get service health data"
        return await self.provide(f"/api/health", "...")
    
    async def get_request(self, job_id: str):
        "Get parse request state"
        return await self.provide(f"/api/request/{job_id}", "...")
    
    async def post_request(self, match_id: str):
        "Submit a new parse request. This call counts as 10 calls for rate limit (but not billing) purposes."
        async with aiohttp.ClientSession() as session:
            await session.post(self.url + f"/api/request/{match_id}")

    async def get_records(self, field: str):
        "Get top performances in a stat"
        return await self.provide(f"/api/records/{field}", "Record")
    
    async def check_lives(self):
        "Get top currently ongoing live games"
        return await self.provide(f"/api/live", "Game")
    
    async def check_schema(self):
        "Get database schema"
        return await self.provide(f"/api/schema", "Schema")
    
    async def get_constant(self, recource: str):
        "Get static game data mirrored from the dotaconstants repository"
        return await self.provide(f"/api/constants/{recource}", "...")
    
    async def get_constants(self):
        "Gets an array of available resources"
        return await self.provide(f"/api/constants", "Constant")
    

    # Scenarios
    async def get_scenarios_item_timings(self, **query_params):
        "Win rates for certain item timings on a hero for items that cost at least 1400 gold"
        return await self.provide(f"/api/scenarios/itemTimings", "Timing", query_params)
    
    async def get_scenarios_lane_roles(self, **query_params):
        "Win rates for heroes in certain lane roles"
        return await self.provide(f"/api/scenarios/laneRoles", "Timing", query_params)
    
    async def get_scenarios_misc(self, **query_params):
        "Miscellaneous team scenarios"
        return await self.provide(f"/api/scenarios/misc", "...", query_params)
