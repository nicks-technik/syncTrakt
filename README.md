# TSV to Trakt.tv Sync

This script syncs your watched history from a TSV file to your Trakt.tv account.

## Setup

1.  **Install dependencies:**

    ```bash
    uv pip install .
    ```

2.  **Trakt.tv API Credentials:**

    *   Create a new application on the [Trakt.tv API website](https://trakt.tv/oauth/applications/new).
    *   Set the "Redirect URI" to `urn:ietf:wg:oauth:2.0:oob`.
    *   Take note of your "Client ID" and "Client Secret".

3.  **Configure the script:**

    *   Create a `.env` file in the same directory as the script (you can copy `.example-env`).
    *   Open the `.env` file and replace the following placeholders:
        *   `YOUR_TRAKT_CLIENT_ID`: Your Trakt.tv application's Client ID.
        *   `YOUR_TRAKT_CLIENT_SECRET`: Your Trakt.tv application's Client Secret.

4.  **Prepare your data:**

    *   Create a `data` directory in the same directory as the script.
    *   Create a `data.tsv` file inside the `data` directory.
    *   The TSV file should have the title in the second column and the year (optional) in the third column.
    *   The file should be tab-separated.
    *   The data should start from the third row.

## Usage

1.  **Run the script:**

    ```bash
    python main.py
    ```

2.  **First Run:**

    *   You will be prompted to go to a URL and enter a code to authorize the application.
    *   This is a one-time process. The script will store the authentication token for future use.

3.  **Subsequent Runs:**

    The script will use the saved authentication token to automatically sync your data.


## Unidentified Titles

If a title cannot be uniquely identified on Trakt.tv (either no results or multiple results), it will be added to a new file called `unidentified.csv` for your review.
