from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright
import os

app = Flask(__name__)

@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    keyword = data.get('keyword') if data else None
    if not keyword:
        keyword = "美肤"  # ✅ 预设默认关键词

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(f"https://www.xiaohongshu.com/search_result?keyword={keyword}")
        page.wait_for_timeout(5000)

        results = []
        items = page.query_selector_all('div.note-item')  # ⚠️ 页面结构可能需要你实际调整

        for item in items[:5]:
            try:
                title = item.query_selector('div.title').inner_text()
                img = item.query_selector('img').get_attribute('src')
                link = item.query_selector('a').get_attribute('href')
                results.append({
                    "title": title,
                    "image": img,
                    "url": "https://www.xiaohongshu.com" + link
                })
            except Exception:
                continue

        browser.close()

    return jsonify(results)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
