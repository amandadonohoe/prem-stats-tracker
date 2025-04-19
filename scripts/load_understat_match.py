import requests
import re
import json
from pathlib import Path

# Constants
MATCH_ID = 26727  # Man Utd 4-0 Everton
URL = f"https://understat.com/match/{MATCH_ID}"
SAVE_PATH = Path("data/understat")
SAVE_PATH.mkdir(parents=True, exist_ok=True)

# Output file
OUTPUT_FILE = SAVE_PATH / f"{MATCH_ID}_by_player.json"


def extract_shots_data(page_source: str) -> dict:
    """
    Extract and decode the JSON-encoded shotsData block from Understat match HTML.
    Returns a dictionary with 'h' and 'a' shot lists (home/away).
    """
    match = re.search(r"shotsData\s*=\s*JSON.parse\('([^']+)'\)", page_source)
    if not match:
        raise ValueError("Could not find shotsData block in the page source.")

    raw_data = match.group(1)
    decoded = bytes(raw_data, "utf-8").decode("unicode_escape")
    shots_json = json.loads(decoded)
    return shots_json


def organize_by_player(shots_json: dict) -> dict:
    """
    Takes raw shots data split by home ('h') and away ('a'),
    and reorganizes it by player with team info included in each shot.
    """
    shots_by_player = {}

    for side in ['h', 'a']:
        for shot in shots_json[side]:
            player = shot['player']
            team = shot['h_team'] if side == 'h' else shot['a_team']

            # Add team field directly to each shot dictionary
            shot['team'] = team

            if player not in shots_by_player:
                shots_by_player[player] = []

            shots_by_player[player].append(shot)

    return shots_by_player


def main():
    print(f"Fetching match data from {URL}...")
    response = requests.get(URL)
    response.raise_for_status()

    print("Parsing shots data...")
    shots_json = extract_shots_data(response.text)

    print("Organizing by player with team info...")
    shots_by_player = organize_by_player(shots_json)

    print(f"Saving structured shot data to {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, "w") as f:
        json.dump(shots_by_player, f, indent=2)

    print("✅ Done! Shot data saved and ready to use.")


if __name__ == "__main__":
    main()
