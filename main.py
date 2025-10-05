import os
import csv
import trakt
import trakt.movies
import trakt.tv
from dotenv import load_dotenv

load_dotenv()

# --- Constants ---
TSV_FILE = os.path.join('data', 'data.tsv')
UNIDENTIFIED_CSV_FILE = 'unidentified.csv'

# --- Trakt.tv Integration ---
trakt.CLIENT_ID = os.environ.get('TRAKT_CLIENT_ID')
trakt.CLIENT_SECRET = os.environ.get('TRAKT_CLIENT_SECRET')

# --- CSV Handling ---
def write_unidentified_title(title, year):
    with open(UNIDENTIFIED_CSV_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([title, year])

# --- Main Logic ---
def main():
    # Authenticate with Trakt
    try:
        trakt.init(store=True)
    except Exception as e:
        print(f"Authentication failed: {e}")
        return

    # Create data directory if it doesn't exist
    if not os.path.exists('data'):
        os.makedirs('data')

    # Create unidentified.csv with header if it doesn't exist
    if not os.path.exists(UNIDENTIFIED_CSV_FILE):
        with open(UNIDENTIFIED_CSV_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Title', 'Year'])

    # Get data from TSV file
    try:
        with open(TSV_FILE, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter='\t')
            # Skip the first two lines
            next(reader, None)
            next(reader, None)
            values = list(reader)
    except FileNotFoundError:
        print(f"Error: '{TSV_FILE}' not found. Please create it.")
        return

    if not values:
        print('No data found in TSV file.')
        return

    for row in values:
        if len(row) < 2:
            continue
        title = row[1]
        year = row[2] if len(row) > 2 else None

        print(f"Processing '{title}' ({year})...")

        try:
            # Search for the movie/show on Trakt
            search_results = trakt.search(title, search_type='movie,show')

            if not search_results:
                print(f"  > Could not find '{title}' ({year}) on Trakt.")
                write_unidentified_title(title, year)
                continue

            if len(search_results) > 1:
                print(f"  > Found multiple results for '{title}' ({year}). Skipping.")
                write_unidentified_title(title, year)
                continue

            item = search_results[0]

            # Mark as watched
            if isinstance(item, trakt.movies.Movie):
                item.mark_as_seen()
            elif isinstance(item, trakt.tv.TVShow):
                item.mark_as_seen()

            print(f"  > Marked '{title}' ({year}) as watched.")

        except Exception as e:
            print(f"  > An error occurred: {e}")

if __name__ == '__main__':
    main()
