import json
import os
from extractors.linkedin_parser import LinkedInParser
from outputs.exporters import Exporter

def load_inputs(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f.readlines() if line.strip()]
    return urls

def main():
    input_file = os.path.join("data", "inputs.sample.txt")
    output_file = os.path.join("data", "sample_output.json")

    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")

    urls = load_inputs(input_file)
    parser = LinkedInParser()

    all_data = []
    for url in urls:
        print(f"Scraping LinkedIn post: {url}")
        data = parser.scrape_post(url)
        all_data.extend(data)

    exporter = Exporter()
    exporter.to_json(all_data, output_file)
    print(f"Scraping complete. Results saved to {output_file}")

if __name__ == "__main__":
    main()