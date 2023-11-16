from urllib.request import urlretrieve

links = [
# "http://www.archive.org/download/MIT6.042JF10/MIT6_042JF10_lec11_300k.mp4",
# "http://www.archive.org/download/MIT6.042JF10/MIT6_042JF10_lec02_300k.mp4",
# "http://www.archive.org/download/MIT6.042JF10/MIT6_042JF10_lec04_300k.mp4",
# "http://www.archive.org/download/MIT6.042JF10/MIT6_042JF10_lec23_300k.mp4",
# "http://www.archive.org/download/MIT6.042JF10/MIT6_042JF10_lec07_300k.mp4",
# "http://www.archive.org/download/MIT6.042JF10/MIT6_042JF10_lec15_300k.mp4",
# "http://www.archive.org/download/MIT6.042JF10/MIT6_042JF10_lec12_300k.mp4",
# "http://www.archive.org/download/MIT6.042JF10/MIT6_042JF10_lec20_300k.mp4",
# "http://www.archive.org/download/MIT6.042JF10/MIT6_042JF10_lec01_300k.mp4",
# "http://www.archive.org/download/MIT6.042JF10/MIT6_042JF10_lec16_300k.mp4",
# "http://www.archive.org/download/MIT6.042JF10/MIT6_042JF10_lec14_300k.mp4",
# "http://www.archive.org/download/MIT6.042JF10/MIT6_042JF10_lec10_300k.mp4",
# "http://www.archive.org/download/MIT6.042JF10/MIT6_042JF10_lec25_300k.mp4",
# "http://www.archive.org/download/MIT6.042JF10/MIT6_042JF10_lec24_300k.mp4",
# "http://www.archive.org/download/MIT6.042JF10/MIT6_042JF10_lec13_300k.mp4",
# "http://www.archive.org/download/MIT6.042JF10/MIT6_042JF10_lec17_300k.mp4",
# "http://www.archive.org/download/MIT6.042JF10/MIT6_042JF10_lec03_300k.mp4",
# "http://www.archive.org/download/MIT6.042JF10/MIT6_042JF10_lec05_300k.mp4",
# "http://www.archive.org/download/MIT6.042JF10/MIT6_042JF10_lec18_300k.mp4",
# "http://www.archive.org/download/MIT6.042JF10/MIT6_042JF10_lec09_300k.mp4",
# "http://www.archive.org/download/MIT6.042JF10/MIT6_042JF10_lec21_300k.mp4",
"http://www.archive.org/download/MIT6.042JF10/MIT6_042JF10_lec19_300k.mp4",
# "http://www.archive.org/download/MIT6.042JF10/MIT6_042JF10_lec08_300k.mp4",
"http://www.archive.org/download/MIT6.042JF10/MIT6_042JF10_lec22_300k.mp4",
"http://www.archive.org/download/MIT6.042JF10/MIT6_042JF10_lec06_300k.mp4"
]

def download_with_progress(url, filename):
    def reporthook(count, block_size, total_size):
        percent = int(count * block_size * 100 / total_size)
        print("\rDownloading {}: {}%".format(filename, percent), end='', flush=True)

    try:
        urlretrieve(url, filename, reporthook=reporthook)
        print("\nDownloaded:", filename)
    except Exception as e:
        print("\nError downloading {}: {}".format(filename, e))

for link in links:
    download_with_progress(link, link.split("/")[-1])
