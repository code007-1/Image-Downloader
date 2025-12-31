"""
This program downloads a given number of random images from 4kwallpapers.com.

original work - https://github.com/H4ppy-04/random-4k-image-downloader
Program: image-downloader
License: MIT
Modified: 31-12-2025
"""

import logging
import os
from typing import Generator

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import re

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

class Image_Downloader:
    """Downloads images in desired resolution from 4kwallpapers"""
    def __init__(self, resolution="1920x1080", page_link="https://4kwallpapers.com/random-wallpapers/", limit=10, sitemap="https://4kwallpapers.com/sitemap.xml", save_dir="~/Pictures"):
        self.resolution = resolution
        self.page_link = page_link
        self.limit = limit
        self.sitemap = sitemap
        self.save_dir = save_dir
        self.block_size = 1024 * 1024  # 1 MB
        self.wallpaper_url = "https://4kwallpapers.com"
        pass

    def __fetch_html(self, url: str) -> BeautifulSoup:
        """Fetch the HTML content of a given URL."""
        try:
            response = requests.get(url, allow_redirects=True)
            response.raise_for_status()
            return BeautifulSoup(response.text, "lxml")
        except requests.RequestException as err:
            logging.error(f"Failed to fetch HTML: {err}")
            raise

    def __fetch_xml(self, url: str) -> BeautifulSoup:
        """Fetch the HTML content of a given URL."""
        try:
            response = requests.get(url, allow_redirects=True)
            response.raise_for_status()
            return BeautifulSoup(response.text, "xml")
        except requests.RequestException as err:
            logging.error(f"Failed to fetch HTML: {err}")
            raise

    def __find_pages(self, base_url: str) -> Generator[str, None, None]:
        """Yield all page URLs from the given base URL."""
        soup = self.__fetch_html(base_url)
        for link in soup.find_all("a", itemprop="url"):
            yield link["href"] # pyright: ignore[reportReturnType]

    def __find_pages_from_xml(self, base_url: str) -> Generator[str, None, None]:
        """Yield all page URLs from the given XML URL."""
        soup = self.__fetch_xml(base_url)
        for link in soup.find_all("loc"):
            if link.text.endswith(".html"):
                yield link.text

    def __extract_image_metadata(self, soup: BeautifulSoup) -> tuple[str, str]:
        """Extract image metadata from parsed HTML."""
        image_tag = soup.find("a", id="resolution")
        if not image_tag:
            raise ValueError("Image resolution link not found")
        href = image_tag["href"]  # pyright: ignore
        href = href.replace(re.search(r"\d{3,4}x\d{3,4}", href).group(0), self.resolution) # pyright: ignore[reportArgumentType, reportAttributeAccessIssue, reportCallIssue]
        return re.search(r"[^/]+$", href).group(0), href  # pyright: ignore

    def __extract_image_metadata_quick(self, main_page_url: str) -> tuple[str, str]:
        """Extract image metadata from parsed HTML image's url."""
        start = re.search(r"[^/]+$", main_page_url).start() # pyright: ignore[reportOptionalMemberAccess]
        name = main_page_url[start:]
        start = re.search(r"(\d+)(?=\.html)", name).start() # pyright: ignore[reportOptionalMemberAccess]
        name = name[:start] + "1920x1080-" + name[start:-4] + "jpg"
        return name , "/images/wallpapers/" + name

    def __download_image(self, url: str, filepath: str):
        """Download an image and save it to a file with a progress bar."""
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            total_size = int(response.headers.get("content-length", 0))

            with open(filepath, "wb") as file, tqdm(
                total=total_size, unit="B", unit_scale=True, desc="Downloading"
            ) as progress_bar:
                for chunk in response.iter_content(self.block_size):
                    file.write(chunk)
                    progress_bar.update(len(chunk))
        except requests.RequestException as err:
            logging.error(f"Failed to download {url}: {err}")
            raise


    def __process_page(self, url: str, index: int):
        """Process a single page and download the corresponding image."""
        postfix = ""
        href = ""
        # little bit more optmized as, we are not scanning html again
        try:
            postfix , href = self.__extract_image_metadata_quick(url)
            image_url = self.wallpaper_url + href
            filepath = os.path.join(os.getcwd(), f"{postfix}")
            self.__download_image(image_url, filepath)
        # upper thing didn't worked so let's scan html
        except:
            soup = self.__fetch_html(url)
            postfix , href = self.__extract_image_metadata(soup)
            image_url = self.wallpaper_url + href
            filepath = os.path.join(os.getcwd(), f"{postfix}")
            self.__download_image(image_url, filepath)


    def download_from_page(self, page_link: str | None = None, limit: int | None = None):
        """download image from given category page"""
        if (not page_link): 
            page_link = self.page_link
        
        if (not limit):
            limit = self.limit

        os.makedirs(os.path.expanduser(self.save_dir), exist_ok=True)
        os.chdir(os.path.expanduser(self.save_dir))

        i = 0 
        for index, page_url in enumerate(self.__find_pages(page_link)):
            try:
                logging.info(f"Processing page {page_url}")
                self.__process_page(page_url, index)
                i += 1
            except Exception as e:
                logging.error(f"Error processing page {page_url}: {e}")
            
            if i >= limit: break

    def download_all(self, limit: int | None = None):
        """downloads all image from site"""
        os.makedirs(os.path.expanduser(self.save_dir), exist_ok=True)
        os.chdir(os.path.expanduser(self.save_dir))

        if (not limit):
            limit = self.limit

        i = 0
        for index, page_url in enumerate(self.__find_pages_from_xml(self.sitemap)):
            try:
                logging.info(f"Processing page {page_url}")
                self.__process_page(page_url, index)
                i += 1
            except Exception as e:
                logging.error(f"Error processing page {page_url}: {e}")
            if i >= limit: break