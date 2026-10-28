"""티스토리 글을 Quartz content/ 폴더의 마크다운으로 가져온다.

사용법: python3 scripts/import_tistory.py  (bs4, markdownify 필요)
"""
import hashlib
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

from bs4 import BeautifulSoup
from markdownify import MarkdownConverter

BLOG = "https://choimino.tistory.com"
ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
ASSETS = CONTENT / "attachments"
FORMULAS = json.loads((Path(__file__).parent / "formulas.json").read_text(encoding="utf-8"))
UA = {"User-Agent": "Mozilla/5.0 (Macintosh) tistory-import"}


def fetch(url, binary=False):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        data = r.read()
    return data if binary else data.decode("utf-8", "replace")


def post_ids():
    xml = fetch(f"{BLOG}/sitemap.xml")
    return sorted({int(m) for m in re.findall(r"tistory\.com/(\d+)</loc>", xml)})


def safe_name(title):
    name = re.sub(r'[\\/:*?"<>|#^\[\]]', " ", title)
    return re.sub(r"\s+", " ", name).strip()[:100] or "untitled"


class TistoryConverter(MarkdownConverter):
    def convert_pre(self, el, text, parent_tags):
        lang = el.get("data-ke-language") or (el.get("class") or [""])[0]
        lang = "" if lang in ("plaintext", "html", "") and not el.get("data-ke-language") else lang
        code = el.get_text()
        return f"\n\n```{lang}\n{code.rstrip()}\n```\n\n"

    def convert_figure(self, el, text, parent_tags):
        # 티스토리 링크 카드는 제목 링크와 사이트 이름만 남긴다
        if el.get("data-ke-type") == "opengraph":
            url = el.get("data-og-source-url") or el.get("data-og-url") or ""
            title = (el.get("data-og-title") or url).replace("[", "(").replace("]", ")").strip()
            host = el.get("data-og-host") or urllib.parse.urlparse(url).netloc
            return f"\n\n> [{title}]({url})  \n> {host}\n\n"
        return f"\n\n{text.strip()}\n\n"


def to_md(html):
    return TistoryConverter(
        heading_style="ATX",
        bullets="-",
        escape_underscores=False,
        escape_asterisks=False,
        escape_misc=False,
    ).convert(html)


def escape_hashtags(md):
    """본문의 '#을' 같은 글자가 옵시디언 태그로 읽히지 않게 코드 블록 밖의 #을 이스케이프한다."""
    out, in_code = [], False
    for line in md.split("\n"):
        if line.startswith("```"):
            in_code = not in_code
        elif not in_code:
            parts = re.split(r"(`[^`]*`)", line)
            line = "".join(x if x.startswith("`") else re.sub(r"(?<![\w&/#\\])#(?=[^\s#])", r"\\#", x) for x in parts)
        out.append(line)
    return "\n".join(out)


def fix_bold(md):
    """'**연결(concatenation)**하고'처럼 굵게 표시 바로 뒤에 글자가 붙으면 마크다운에서
    굵게가 풀리므로, 그런 경우만 <strong> 태그로 바꾼다."""
    import unicodedata

    def is_punct(ch):
        return unicodedata.category(ch).startswith("P")

    def repl(m):
        before, inner = m.group(1), m.group(2)
        after = md[m.end():m.end() + 1]
        if (is_punct(inner[-1]) and after and not after.isspace() and not is_punct(after)) or (
            is_punct(inner[0]) and before and not before.isspace() and not is_punct(before)
        ):
            return f"{before}<strong>{inner}</strong>"
        return m.group(0)

    return re.sub(r"(^|.)\*\*([^*\n]+?)\*\*", repl, md, flags=re.M)


def download_image(src, post_id):
    if src.startswith("//"):
        src = "https:" + src
    # 티스토리 썸네일 URL이면 원본 주소를 꺼낸다
    q = urllib.parse.parse_qs(urllib.parse.urlparse(src).query)
    if "fname" in q:
        src = q["fname"][0]
    ext = Path(urllib.parse.urlparse(src).path).suffix.lower()
    if ext not in (".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"):
        ext = ".png"
    name = f"{post_id}-{hashlib.md5(src.encode()).hexdigest()[:10]}{ext}"
    dest = ASSETS / name
    if not dest.exists():
        try:
            dest.write_bytes(fetch(src, binary=True))
        except Exception as e:  # 이미지 하나 실패해도 계속
            print(f"  ! image failed {src}: {e}", file=sys.stderr)
            return None
    return name


def main():
    ASSETS.mkdir(parents=True, exist_ok=True)
    posts = {}
    for pid in post_ids():
        soup = BeautifulSoup(fetch(f"{BLOG}/{pid}"), "html.parser")
        body = soup.select_one("div.contents_style") or soup.select_one(".tt_article_useless_p_margin")
        if body is None:
            print(f"skip {pid}: no body", file=sys.stderr)
            continue
        title = soup.find("meta", property="og:title")["content"]
        date = soup.find("meta", property="article:published_time")["content"][:10]
        cat_el = soup.select_one("a.category")
        category = cat_el.get_text(strip=True) if cat_el else "Uncategorized"
        cat_path = urllib.parse.unquote(cat_el["href"]).removeprefix("/category").strip("/") if cat_el else ""
        if not cat_path:
            category, cat_path = "Others", "Others/Others"
        posts[pid] = dict(soup=body, title=title, date=date, category=category, cat_path=cat_path)
        print(f"{pid}: [{cat_path}] {title}")
        time.sleep(0.3)

    names = {pid: safe_name(p["title"]) for pid, p in posts.items()}

    for pid, p in posts.items():
        body = p["soup"]
        for img in body.find_all("img"):
            src = img.get("src") or img.get("data-src") or ""
            name = download_image(src, pid) if src else None
            if name in FORMULAS:
                img.replace_with(f"FORMULA[{name}]")
            elif name:
                img.replace_with(f"![[{name}]]")
        # 같은 블로그 내부 링크는 위키링크로
        for a in body.find_all("a", href=True):
            m = re.fullmatch(r"(?:https?:)?//choimino\.tistory\.com/(?:m/)?(\d+)/?|/(\d+)", a["href"])
            if m and int(m.group(1) or m.group(2)) in names:
                target = names[int(m.group(1) or m.group(2))]
                label = a.get_text(strip=True)
                a.replace_with(f"[[{target}|{label}]]" if label and label != target else f"[[{target}]]")

        md = to_md(str(body))
        md = md.replace("\\[\\[", "[[").replace("\\]\\]", "]]").replace("\\!", "!")
        md = md.replace("\u00a0", " ").replace("****", "")
        # 제목(#)에 붙은 굵게 표시는 제거
        md = re.sub(r"^(#{1,6} )(.*)$", lambda m: m.group(1) + m.group(2).replace("**", "").strip(), md, flags=re.M)
        md = re.sub(r"[ \t]+$", lambda m: "  " if len(m.group(0)) >= 2 else "", md, flags=re.M)
        md = escape_hashtags(md)
        md = fix_bold(md)
        # 수식 이미지는 LaTeX 블록으로 바꾼다 (scripts/formulas.json)
        md = re.sub(r"FORMULA\[([^\]]+)\]", lambda m: f"\n\n$$\n{FORMULAS[m.group(1)]}\n$$\n\n", md)
        md = re.sub(r"\n{3,}", "\n\n", md).strip() + "\n"

        tags = [t for t in p["cat_path"].split("/") if t]
        front = {
            "title": p["title"],
            "date": p["date"],
            "tags": tags,
            "aliases": [f"tistory-{pid}"],
            "source": f"{BLOG}/{pid}",
        }
        fm = "---\n" + "\n".join(f"{k}: {json.dumps(v, ensure_ascii=False)}" for k, v in front.items()) + "\n---\n\n"
        folder = CONTENT / Path(*p["cat_path"].split("/"))
        folder.mkdir(parents=True, exist_ok=True)
        (folder / f"{names[pid]}.md").write_text(fm + md, encoding="utf-8")

    # 수식으로 바뀌어 더 이상 쓰지 않는 가져온 이미지는 지운다
    used = set()
    for md_file in CONTENT.rglob("*.md"):
        used |= set(re.findall(r"!\[\[([^\]|]+)", md_file.read_text(encoding="utf-8")))
    for f in ASSETS.iterdir():
        if re.fullmatch(r"\d+-[0-9a-f]{10}\.\w+", f.name) and f.name not in used:
            f.unlink()

    print(f"done: {len(posts)} posts")


if __name__ == "__main__":
    main()
