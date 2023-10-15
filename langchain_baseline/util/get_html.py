# save html file from url with api access key

import requests
from bs4 import BeautifulSoup
import os
from config import Config
import argparse, json

config = Config().get_config()["ringley_api"]

def get_html(url, ringley_config = config, chunk=False, chunk_size=50):
    """
        This function saves the html file from the given url.
        The url is from the Ringley API.
        The received html file is saved in the data/update folder for the further embedding.

        INPUT: url: str
                ringley_config: dict
        OUTPUT: None
    """

    headers = {ringley_config["key"]: ringley_config["value"]}
    response_articles = requests.get(url=url, headers = headers)
    assert response_articles.status_code == 200
    # extract the html file using beautiful soup
    soup = BeautifulSoup(response_articles.text, "html.parser")
    
    print(f"[INFO] Saving html file from {url}...")

    file_name = url.split("/")[-1]
    name = f"html_file_{file_name}.txt"

    if chunk:
        data = []
        data_dict = json.loads(soup.prettify())
        article_list = data_dict["data"]
        print(f"[INFO] Saving {len(article_list)} objects in chunks...")
        for article in article_list:
            attributes = article["attributes"]
            temp_dict = {}
            temp_dict["title"] = attributes["title"]
            temp_dict["description"] = attributes["description"]
            data.append(temp_dict)
        name = f"html_file_{file_name}"
        for i in range(0, len(data), chunk_size):
            with open(os.path.join("data", "update", f"{name}_{i}.txt"), "w") as f:
                if i + chunk_size > len(data):
                    print(f"[INFO] Saving {i} to {len(data)} objects...")
                    json.dump(data[i:], f)
                else:
                    print(f"[INFO] Saving {i} to {i+chunk_size} objects...")
                    json.dump(data[i:i+chunk_size], f)
        print(f"[INFO] {url}... Saving complete!")

    else:
        with open(os.path.join("data", "update", name), "w") as f:
            # save the html objects as txt
            f.write(soup.prettify())


def get_multiple_html(urls=None, ringley_config = config, chunk=False):
    """
        This function saves the html file from the given urls.
        The urls are from the Ringley API.
        The received html file is saved in the data/update folder for the further embedding.

        INPUT: urls: list
                ringley_config: dict
        OUTPUT: None
    """
    urls_list = []
    if urls == None:
        urls_list = [ringley_config["articles_url"], ringley_config["blogs_url"]]
    for url in urls_list:
        get_html(url=url, ringley_config=config, chunk=chunk)

def main(args):
    get_multiple_html(chunk=args.chunk)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--chunk", action="store_true", help="Save the html file in chunks")
    main(parser.parse_args())