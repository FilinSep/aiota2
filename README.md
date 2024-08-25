# AioTA2
![enter image description here](https://img.shields.io/pypi/v/aiota2?color=success)![enter image description here](https://img.shields.io/pypi/pyversions/aiota2)![enter image description here](https://img.shields.io/github/followers/FilinSep?style=social)![enter image description here](https://img.shields.io/github/issues/FilinSep/aiota2)

Asynchronous python interface for \<OPENDOTA/> API
## Features
* A function for each API call
* Asynchrony support
* Allows API keys authentication
* Abstract Models class
## Usage
### Use <OPENDOTA/> API in a project BUT WITH ASYNCHRONICITY
```python
from aiota2 import AioClient
import asyncio

async def main():
  # Initalize API interface object
  dota = AioClient()

asyncio.run(main=main())
```
Get player / match / team / heroes
```python
await dota.get_player(account_id: int)
await dota.get_match(match_id: int)
await dota.get_team(team_id: int)
await dota.get_heroes()
```
### Query Params
```python
await dota.search_player_by_personaname(**query_params)
await dota.find_matches(**query_params)
await dota.get_teams(**query_params)
# ...
```
### Hero attribute
That give you ability to access the dota heroes base without sending a request to API many times, just use object attribute "heroes"
```python
from aiota2 import AioClient
import asyncio

async def main():
    # Initalize API interface object with heroes attribute
    dota = await AioClient().load_heroes() # Pay attention to await
    # load_heroes() is dota.heroes = await get_heroes()

asyncio.run(main=main())
```
So that allows you:
```python
dota.heroes
dota.get_hero_by_param(param: str, value: Any)
dota.get_heroes_by_param(param: str, value: Any)
```
### DataModel
Using DataModel
```python
from aiota2 import AioClient
import asyncio

async def main():
  # Initalize API interface object
  dota = AioClient(with_models=True)

asyncio.run(main=main())
```
```python
>>> answer = await dota.get_player(player_id: int)
<DataModel of Player at address>
>>> answer.rank_tier
0
```
#### Deepening
Creating DataModel
```python
from aiota2 import DataModel

colors = {
    "sky": "blue",
    "grass": "green"
}

model = DataModel("colors", colors)
```
## About OpenDota API
The OpenDota API provides Dota 2 related data including advanced match data extracted from match replays.

OpenDota API Documentation: https://docs.opendota.com/

## Credits
This package uses data provided by The OpenDota API.
