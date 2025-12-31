from ImageDownloader import Image_Downloader

BLOCK_SIZE = 1024 * 1024  # 1 MB
WALLPAPER_URL = "https://4kwallpapers.com"
PAGES_LINK = {
    'random': 'https://4kwallpapers.com/random-wallpapers/',
    'recent': 'https://4kwallpapers.com/',
    'popular': 'https://4kwallpapers.com/most-popular-4k-wallpapers/',
    'featured': 'https://4kwallpapers.com/best-4k-wallpapers/',
    'abstract': 'https://4kwallpapers.com/abstract/',
    'animal': 'https://4kwallpapers.com/animals/',
    'anime': 'https://4kwallpapers.com/anime/',
    'architecture': 'https://4kwallpapers.com/architecture/',
    'bikes': 'https://4kwallpapers.com/bikes/',
    'black': 'https://4kwallpapers.com/black-dark/',
    'car': 'https://4kwallpapers.com/cars/',
    'celebrations': 'https://4kwallpapers.com/celebrations/',
    'cute': 'https://4kwallpapers.com/cute/',
    'fantasy': 'https://4kwallpapers.com/fantasy/',
    'flowers': 'https://4kwallpapers.com/flowers/',
    'food': 'https://4kwallpapers.com/food/',
    'games': 'https://4kwallpapers.com/games/',
    'gradients': 'https://4kwallpapers.com/gradients/',
    'cgi': 'https://4kwallpapers.com/graphics-cgi/',
    'lifestyle': 'https://4kwallpapers.com/lifestyle/',
    'love': 'https://4kwallpapers.com/love/',
    'milatery': 'https://4kwallpapers.com/military/',
    'movies': 'https://4kwallpapers.com/movies/',
    'music': 'https://4kwallpapers.com/music/',
    'nature': 'https://4kwallpapers.com/nature/',
    'people': 'https://4kwallpapers.com/people/',
    'photography': 'https://4kwallpapers.com/photography/',
    'quotes': 'https://4kwallpapers.com/quotes/',
    'sci-fi': 'https://4kwallpapers.com/sci-fi/',
    'space': 'https://4kwallpapers.com/space/',
    'sports': 'https://4kwallpapers.com/sports/',
    'technology': 'https://4kwallpapers.com/technology/',
    'world': 'https://4kwallpapers.com/world/'
 }
SITEMAP_URL = "https://4kwallpapers.com/sitemap.xml"
RESOLUTION = {
    "fhd":"1920x1080",
    "whd":"1920x1200",
    "uhd":"2560x1080",
    "qhd":"2560x1440",
    "retina_widescreen":"2880x1800",
    "uqhd":"3440x1440",
    "dhd":"3840x1080",
    "4k":"3840x2160",
    "4.5k":"4480x2520",
    "5k":"5120x280"
    }

def main():
    downloader = Image_Downloader(page_link=PAGES_LINK['cgi'], limit=5, save_dir="~/Downloads")
    downloader.download_from_page()

if __name__ == "__main__":
    main()