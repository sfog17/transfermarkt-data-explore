""" 
Analyse the relationship between country of birth and national team
Using transfermarkt data
"""
import csv
import re
from pathlib import Path
from typing import Dict
import pandas as pd
import requests
from bs4 import BeautifulSoup as soup


def download_html_data(html_dir: Path):
    """ Download HTML pages for all the players of all the national teams"""
    core_url = "https://www.transfermarkt.co.uk"
    # Parse countries url from the FIFA ranking webpage
    ref_url = []
    for page_idx in range(1, 10):
        suffix_url = f"/statistik/weltrangliste?ajax=yw1&page={str(page_idx)}"
        res = requests.get(core_url + suffix_url, headers={"User-Agent": "python"})
        # Regex countries page
        # Example: "/brasilien/startseite/verein/3439"
        ref_url.extend(re.findall(r"/[a-z\-]+/startseite/verein/\d+", res.text))
    countries_url = set(ref_url)

    # Parse players url for each national team
    for country_suffix in list(countries_url):
        print(country_suffix)
        res = requests.get(core_url + country_suffix, headers={"User-Agent": "python"})
        ref_url = []
        # Regex players page
        # Example: "/ederson/profil/spieler/238223"
        ref_url.extend(re.findall(r"/[a-z\-]+/profil/spieler/\d+", res.text))
        players_url = set(ref_url)

        # Scrape webpage for each player and save the html
        for p in players_url:
            print(p)
            res = requests.get(core_url + p, headers={"User-Agent": "python"})
            filename = p.split("/")[1] + '_' + p.split("/")[-1] + ".html"
            with open(html_dir / filename, "w", encoding="utf-8") as f_out:
                f_out.write(res.text)


def delete_html_data(html_dir: Path):
    """ Remove all HTML files """
    for path in list(html_dir.glob('*.html')):
        path.unlink()


def clean_string(text: str) -> str:
    return ' '.join(text.strip().split())


def parse_player_country_data(page_html: str)  -> Dict[str, str]:
    """ Extract the country of birth and national team from a transfermarkt webpage"""
    page_soup = soup(page_html, "html.parser")
    # Get name
    player_name = page_soup.find_all("div", {"class": "dataName"})[0].find_all("h1")[0].text
    # Get banner with data
    dc = page_soup.find("div",attrs={"class":"dataContent"})
    # List the attributes, values and countries (title of the flag image)
    # Includes coutries, but also date of birth, position, etc...
    data_items = [clean_string(di.text)[:-1] for di in dc.findAll("span",attrs={"class":"dataItem"})]
    data_values = []
    data_countries = []
    for dv in dc.findAll("span",attrs={"class":"dataValue"}):
        data_values.append(clean_string(dv.text))
        if img := dv.find("img",attrs={"class":"flaggenrahmen"}):
            country = img['title']
        else:
            country = ''
        data_countries.append(country)
    # Convert to dataframe and select the fields of interest
    # Written fast with Jupyter Notebook, the code could be cleaner and faster
    df = pd.DataFrame(list(zip(data_items, data_values, data_countries)))
    # Tranpose and use first rows as headers
    df = df.transpose()
    new_header = df.iloc[0]
    df = df[1:]
    df.columns = new_header
    # Normalise football nationality
    # Browsing, it can be "Former International", "Current international", "National Player"
    col_fifa_country = [col for col in df.columns if 'international' in col.lower()]
    if len(col_fifa_country) > 0:
        df.rename(columns={col_fifa_country[0]: "International"}, inplace=True)
    df.rename(columns={'National player': "International"}, inplace=True)
    # Output information to a dictionary
    player_dict = {
        'player_name': player_name,
        'country_birth': df['Place of birth'][2] if 'Place of birth' in df.columns else '',
        'country_fifa': df['International'][2] if 'International' in df.columns else ''
    }
    return player_dict


def transform_data(html_dir: Path, output_csv: Path):
    """
    Take a folder with HTML player pages
    Output csv with (player_name, country_birth, country_fifa)
    """
    with open(output_csv, 'w', encoding='utf-8', newline='') as f_out:
        csv_writer = csv.DictWriter(f_out, ['player_name', 'country_birth', 'country_fifa'])
        csv_writer.writeheader()
        for idx, path in enumerate(list(html_dir.glob('*.html')), start=1):
            with open(path, encoding='utf-8') as f_in:
                if idx % 100 == 0:
                    print(f'Lines read: {idx:,}')
                page_html = f_in.read()
                csv_writer.writerow(parse_player_country_data(page_html))


if __name__ == '__main__':
    HTML_DIR = Path(".") / "data_html"
    HTML_DIR.mkdir(exist_ok=True)
    download_html_data(HTML_DIR)
    RESULTS_DIR = Path(".") / "results"
    RESULTS_DIR.mkdir(exist_ok=True)
    transform_data(HTML_DIR, RESULTS_DIR / 'nationality_players.csv')
    delete_html_data(HTML_DIR)
