import subprocess


def run_spider():
    subprocess.run(["scrapy", "crawl", "tequila"])


if __name__ == "__main__":
    # Define the number of concurrent processes/spiders you want to run
    num_processes = 100

    while True:
        run_spider(0)
