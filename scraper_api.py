from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright
import urllib.parse

app = Flask(__name__)

class UpworkSearchBuilder:
    def __init__(self):
        self.base_url = "https://www.upwork.com/nx/jobs/search/"
        self.params = {}

    def set_query(self, query):
        self.params["q"] = query
        return self

    def set_experience_level(self, level):
        self.params["experience_level"] = level
        return self

    def set_job_type(self, job_type):
        self.params["job_type"] = job_type
        return self

    def set_hourly_rate(self, min_rate=None, max_rate=None):
        if min_rate is not None:
            self.params["hourly_rate_min"] = str(min_rate)
        if max_rate is not None:
            self.params["hourly_rate_max"] = str(max_rate)
        return self

    def set_project_length(self, length):
        self.params["duration"] = length
        return self

    def build(self):
        query_string = urllib.parse.urlencode(self.params)
        return f"{self.base_url}?{query_string}"

def scrape_jobs(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, args=["--disable-blink-features=AutomationControlled"])
        page = browser.new_page()
        page.goto(url, timeout=60000)

        # Sayfa içeriğini kaydet (debug için)
        with open("debug_page.html", "w", encoding="utf-8") as f:
            f.write(page.content())

        # Burada beklemeyi yoruma aldık çünkü sayfa yavaş yükleniyorsa hata veriyor olabilir
        # page.wait_for_selector("article[data-test='JobTile']", timeout=30000)

        job_cards = page.query_selector_all("article[data-test='JobTile']")

        jobs = []
        for card in job_cards:
            try:
                title_el = card.query_selector("a[data-test*='job-tile-title-link']")
                title = title_el.inner_text().strip()
                href = title_el.get_attribute("href")
                job_url = f"https://www.upwork.com{href}"

                description_el = card.query_selector("div[data-test='UpCLineClamp JobDescription']")
                description = description_el.inner_text().strip() if description_el else ""

                rate_el = card.query_selector("li[data-test='job-type-label']")
                rate = rate_el.inner_text().strip() if rate_el else ""

                experience_el = card.query_selector("li[data-test='experience-level']")
                experience = experience_el.inner_text().strip() if experience_el else ""

                duration_el = card.query_selector("li[data-test='duration-label']")
                duration = duration_el.inner_text().strip() if duration_el else ""

                tags_el = card.query_selector_all("div[data-test='TokenClamp JobAttrs'] span")
                tags = [tag.inner_text().strip() for tag in tags_el]

                jobs.append({
                    "title": title,
                    "url": job_url,
                    "description": description,
                    "rate": rate,
                    "experience": experience,
                    "duration": duration,
                    "tags": tags
                })
            except Exception as e:
                print(f"Scraping error: {e}")

        browser.close()
        return jobs

@app.route("/search", methods=["GET"])
def search():
    q = request.args.get("query", "python")
    job_type = request.args.get("job_type")
    experience = request.args.get("experience")
    duration = request.args.get("duration")
    rate_min = request.args.get("rate_min")
    rate_max = request.args.get("rate_max")

    builder = UpworkSearchBuilder()
    builder.set_query(q)
    if job_type:
        builder.set_job_type(job_type)
    if experience:
        builder.set_experience_level(experience)
    if duration:
        builder.set_project_length(duration)
    if rate_min or rate_max:
        builder.set_hourly_rate(min_rate=int(rate_min) if rate_min else None,
                                max_rate=int(rate_max) if rate_max else None)

    search_url = builder.build()
    print(f"🔍 Arama URL: {search_url}")

    jobs = scrape_jobs(search_url)
    return jsonify(jobs)

if __name__ == "__main__":
    app.run(debug=True, port=5000)