from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright

app = Flask(__name__)

@app.route('/search')
def search():
    keyword = request.args.get('keyword')
    if not keyword:
        return jsonify({"error": "缺少关键词参数"}), 400

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(f"https://www.xiaohongshu.com/search_result?keyword={keyword}")
        page.wait_for_timeout(5000)

        results = []

        # 注意：页面结构可能需适配。这里只做结构示例
        items = page.query_selector_all('div.note-item')
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
    app.run(host='0.0.0.0', port=10000)
