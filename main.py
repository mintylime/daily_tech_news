import urllib.parse
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import email.utils as eut
import json

# ------------------- CONFIG -------------------
# Load categories and search terms from JSON
def load_categories(path="search_keywords_tech.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

categories = load_categories()

# Time cutoffs
cutoff = datetime.now() - timedelta(hours=48)  # recent window
seven_days_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')  # fetch window

# ------------------- FETCH ARTICLES -------------------
output_rows = []
for category, terms in categories.items():
    base_query = " OR ".join(f'\"{term}\"' for term in terms)
    query = base_query
    encoded = urllib.parse.quote(query)
    rss_url = f"https://news.google.com/rss/search?q={encoded}+when:7d"
    try:
        req = Request(rss_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urlopen(req) as response:
            xml_data = response.read()
        soup = BeautifulSoup(xml_data, 'lxml-xml')
        for item in soup.find_all('item'):
            try:
                pub_dt = datetime(*eut.parsedate(item.pubDate.text)[:6])
                title = item.title.text
                link = item.link.text
                desc = item.description.text if item.description else ''
                date_str = pub_dt.strftime('%Y-%m-%d %H:%M')
                row_class = 'recent' if pub_dt >= cutoff else 'older'
                content = desc
                output_rows.append((pub_dt, date_str, category, content, row_class))
            except Exception:
                continue
    except Exception as e:
        print(f"Error fetching category {category}: {e}")

# ------------------- SORT ARTICLES -------------------
# Category ascending, then date descending
output_rows.sort(key=lambda x: x[2])  # category asc
output_rows.sort(key=lambda x: x[0], reverse=True)  # date desc

# ------------------- COUNTS -------------------
total_articles = len(output_rows)
recent_articles = sum(1 for (_dt, _ds, _cat, _cont, cls) in output_rows if cls == 'recent')

# ------------------- WRITE HTML -------------------
with open("index.html", "w", encoding="utf-8") as f:
    f.write(f"""<!DOCTYPE html>
<html>
<head>
<meta charset=\"UTF-8\">
<title>Cyber & Tech News Feed</title>
<style>
  body {{ font-family: Arial, sans-serif; margin: 40px; }}
  table {{ border-collapse: collapse; width: 100%; }}
  th, td {{ text-align: left; padding: 8px; border-bottom: 1px solid #ddd; }}
  th {{ background-color: #f2f2f2; cursor: pointer; }}
  .date-filter {{ margin-bottom: 20px; }}
  a {{ color: #1a0dab; text-decoration: none; }}
</style>
<script>
  let currentSort = {{ col: 0, asc: false }};
  let showingRecent = true;
  function toggleOld() {{
    const oldRows = document.querySelectorAll('.older');
    oldRows.forEach(row => {{
      if (row.style.display === 'none' || row.style.display === '') {{ row.style.display = 'table-row'; }}
      else {{ row.style.display = 'none'; }}
    }});
    showingRecent = !showingRecent;
    document.getElementById('toggleBtn').innerText = showingRecent ? 'Show older articles' : 'Hide older articles';
    document.getElementById('countText').innerText = showingRecent ?
      `{recent_articles} of {total_articles} articles` :
      `{total_articles} of {total_articles} articles`;
  }}
  function sortTable(colIndex) {{
    const tbody = document.querySelector('#newsTable tbody');
    let asc;
    if (currentSort.col === colIndex) asc = !currentSort.asc;
    else asc = (colIndex === 1);
    currentSort = {{ col: colIndex, asc }};
    const rows = Array.from(tbody.rows);
    rows.sort((a, b) => {{
      let valA = a.cells[colIndex].textContent.trim();
      let valB = b.cells[colIndex].textContent.trim();
      if (colIndex === 0) return asc ? new Date(valA) - new Date(valB) : new Date(valB) - new Date(valA);
      return asc ? valA.localeCompare(valB) : valB.localeCompare(valA);
    }});
    tbody.innerHTML = '';
    rows.forEach(r => tbody.appendChild(r));
  }}
  document.addEventListener('DOMContentLoaded', () => {{
    // Hide older by default
    document.querySelectorAll('.older').forEach(row => row.style.display = 'none');
    document.getElementById('toggleBtn').innerText = 'Show older articles';
    document.getElementById('countText').innerText = '{recent_articles} of {total_articles} articles';
    sortTable(0);
  }});
</script>
</head>
<body>
<h2>Cyber & Tech News Feed</h2>
<p class=\"date-filter\"><span id=\"countText\"></span> <button id=\"toggleBtn\" onclick=\"toggleOld()\"></button></p>
<table id=\"newsTable\">
<thead><tr>
  <th onclick=\"sortTable(0)\">Date ▲▼</th>
  <th onclick=\"sortTable(1)\">Category ▲▼</th>
  <th>Title</th>
</tr></thead>
<tbody>
""")
    for pub_dt, date_str, cat, content, row_class in output_rows:
        f.write(f"<tr class='{row_class}'><td>{date_str}</td><td>{cat}</td><td>{content}</td></tr>\n")
    f.write("</tbody>\n</table>\n</body>\n</html>")
print(f"✅ index.html generated: {total_articles} articles.")
