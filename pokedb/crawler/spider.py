import subprocess
import time
from concurrent.futures import ProcessPoolExecutor


def run_spider():
    subprocess.run(["scrapy", "crawl", "tequila"])


if __name__ == "__main__":
    # Define the number of concurrent processes/spiders you want to run
    num_processes = 3

    with ProcessPoolExecutor(max_workers=num_processes) as executor:
        while True:
            # Submit the spider running function to the executor
            future = executor.submit(run_spider)

            # Wait for a bit before submitting the next spider
            time.sleep(2)  # wait for 10 seconds before starting the next spider
