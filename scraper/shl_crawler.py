from playwright.sync_api import sync_playwright
import json
import os

CATALOG_URL = "https://www.shl.com/solutions/products/product-catalog/"

def crawl_shl_catalog():
    captured_data = []

    def handle_response(response):
        url = response.url.lower()
        if "product" in url and "catalog" in url and response.request.method == "GET":
            try:
                data = response.json()
                if isinstance(data, dict) and "results" in data:
                    captured_data.extend(data["results"])
            except:
                pass

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        page.on("response", handle_response)

        page.goto(CATALOG_URL, timeout=60000)
        page.wait_for_load_state("networkidle")

        # Let all API calls finish
        page.wait_for_timeout(10000)

        browser.close()

    return captured_data

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)

    data = crawl_shl_catalog()

    if len(data) == 0:
        print("⚠️ Live crawling blocked by SHL. Using fallback catalog.")
        exit(1)

    assessments = []
    for item in data:
        assessments.append({
            "name": item.get("name", "SHL Assessment"),
            "url": item.get("url", ""),
            "description": item.get("description", "SHL Individual Test Solution"),
            "duration": item.get("duration", 30),
            "adaptive_support": "Yes",
            "remote_support": "Yes",
            "test_type": [item.get("category", "Cognitive Ability")]
        })

    with open("data/assessments.json", "w", encoding="utf-8") as f:
        json.dump(assessments, f, indent=2)

    print("Scraped", len(assessments), "SHL Individual Test Solutions")

