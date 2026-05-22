"""Build single-page HTML documentation from Markdown files."""
import re, os, json

DOCS_DIR = os.path.dirname(os.path.abspath(__file__))

# Section config: (id, title, filename)
SECTIONS = [
    ("overview",       "1. 概述",           "index.md"),
    ("file-structure", "2. 文件结构",       "getting-started.md"),
    ("enums",          "3. 枚举与常量",      "enums.md"),
    ("rpc-attribute",  "4. RPC 属性",       "rpc-attribute.md"),
    ("data-models",    "5. 数据模型",       "data-models.md"),
    ("client",         "6. 核心客户端 API",  "client.md"),
    ("message-handler","7. 消息处理器",     "message-handler.md"),
    ("protocol",       "8. 协议格式",       "protocol.md"),
    ("examples",       "9. 完整使用示例",   "examples.md"),
    ("faq",            "10. 常见问题",      "faq.md"),
]

def read_md(filename):
    path = os.path.join(DOCS_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def strip_frontmatter(text):
    """Remove YAML front matter (--- ... ---)"""
    text = text.strip()
    if text.startswith("---"):
        idx = text.find("---", 3)
        if idx != -1:
            text = text[idx + 3:].strip()
    return text

def md_to_html(text):
    """Simple markdown to HTML converter."""
    lines = text.split("\n")
    out = []
    i = 0
    in_code_block = False
    in_table = False
    code_lines = []
    table_lines = []
    in_arch = False
    arch_lines = []
    pending_prev_next = []

    def flush_inline():
        nonlocal pending_prev_next
        if pending_prev_next:
            out.append('<div class="prev-next">')
            for link in pending_prev_next:
                out.append(link)
            out.append('</div>')
            pending_prev_next = []

    while i < len(lines):
        line = lines[i]

        # Architecture diagram block (between ``` and ```)
        if line.startswith("```") and not in_code_block:
            # Check if this is an architecture diagram (detected by box-drawing chars)
            next_lines = lines[i+1:i+5] if i+5 <= len(lines) else lines[i+1:]
            combined = "\n".join(next_lines)
            if any(c in combined for c in ["┌", "└", "├", "│", "┬", "┴", "─"]):
                i += 1
                while i < len(lines) and not lines[i].startswith("```"):
                    arch_lines.append(lines[i])
                    i += 1
                i += 1  # skip closing ```
                out.append('<div class="arch-diagram">')
                out.append("\n".join(arch_lines))
                out.append('</div>')
                arch_lines = []
                continue
            else:
                # Normal code block
                i += 1
                while i < len(lines) and not lines[i].startswith("```"):
                    code_lines.append(lines[i])
                    i += 1
                i += 1
                out.append('<pre><code>' + escape_html("\n".join(code_lines)) + '</code></pre>')
                code_lines = []
                continue

        # Table detection
        if re.match(r'^\|.*\|.*\|$', line) and not in_code_block:
            flush_inline()
            table_lines.append(line)
            # Check if next line is separator
            if i + 1 < len(lines) and re.match(r'^\|[\s\-:|]+\|$', lines[i+1].strip()):
                i += 2  # skip separator
                while i < len(lines) and re.match(r'^\|.*\|.*\|$', lines[i]):
                    table_lines.append(lines[i])
                    i += 1
                out.append(render_table(table_lines))
                table_lines = []
                continue

        # Headings
        if line.startswith("# ") and not in_code_block:
            flush_inline()
            out.append(f'<h1>{escape_html(line[2:].strip())}</h1>')
        elif line.startswith("## ") and not in_code_block:
            flush_inline()
            out.append(f'<h2>{escape_html(line[2:].strip())}</h2>')
        elif line.startswith("### ") and not in_code_block:
            flush_inline()
            out.append(f'<h3>{escape_html(line[3:].strip())}</h3>')
        elif line.startswith("#### ") and not in_code_block:
            flush_inline()
            out.append(f'<h4>{escape_html(line[4:].strip())}</h4>')

        # Horizontal rule
        elif line.strip() == "---" or line.strip() == "***":
            flush_inline()
            out.append('<hr>')

        # Navigation links (← ... →)
        elif re.match(r'^\[←.+→\]\(.+\)$', line) or re.match(r'^\[←.+\]\(.+\)\s*\|\s*\[.+\]\(.+\)$', line):
            # Collect prev/next links, render at end
            pass

        # Blockquote
        elif line.startswith("> ") and not in_code_block:
            flush_inline()
            content = line[2:]
            # Process inline formatting
            content = process_inline(content)
            out.append(f'<blockquote><p>{content}</p></blockquote>')

        # List items
        elif re.match(r'^[\-\*]\s+', line) and not in_code_block:
            flush_inline()
            content = process_inline(re.sub(r'^[\-\*]\s+', '', line))
            out.append(f'<li>{content}</li>')

        # Empty line
        elif line.strip() == "":
            flush_inline()

        # Regular paragraph
        elif not in_code_block:
            flush_inline()
            content = process_inline(line)
            if content.strip():
                out.append(f'<p>{content}</p>')

        i += 1

    flush_inline()
    return "\n".join(out)


def render_table(lines):
    """Render a markdown table to HTML."""
    header_cells = [c.strip() for c in lines[0].strip("|").split("|")]
    rows = []
    for line in lines[1:]:
        cells = [c.strip() for c in line.strip("|").split("|")]
        rows.append(cells)
    html = ['<table>', '<thead><tr>']
    for cell in header_cells:
        html.append(f'<th>{process_inline(cell)}</th>')
    html.append('</tr></thead><tbody>')
    for row in rows:
        html.append('<tr>')
        for cell in row:
            html.append(f'<td>{process_inline(cell)}</td>')
        html.append('</tr>')
    html.append('</tbody></table>')
    return "\n".join(html)


def process_inline(text):
    """Process inline markdown: bold, italic, code, links."""
    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # Italic (but not inside words)
    text = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'<em>\1</em>', text)
    # Inline code
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    # Links [text](url)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    return text


def escape_html(text):
    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    text = text.replace('"', "&quot;")
    return text


# ─── CSS ───
CSS = r"""<style>
:root {
    --sidebar-width: 260px;
    --bg: #fafbfc;
    --sidebar-bg: #1b1f2a;
    --sidebar-text: #c8ccd4;
    --sidebar-hover: #2d3344;
    --sidebar-active: #3b82f6;
    --text: #1f2937;
    --text-light: #6b7280;
    --border: #e5e7eb;
    --code-bg: #f3f4f6;
    --code-text: #dc2626;
    --link: #3b82f6;
    --table-stripe: #f9fafb;
    --heading: #111827;
    --blockquote-bg: #eff6ff;
    --blockquote-border: #3b82f6;
}
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans SC", Roboto, sans-serif;
    line-height: 1.7; color: var(--text); background: var(--bg);
    display: flex; min-height: 100vh;
}
.sidebar {
    position: fixed; top: 0; left: 0; width: var(--sidebar-width);
    height: 100vh; background: var(--sidebar-bg); color: var(--sidebar-text);
    overflow-y: auto; z-index: 100; display: flex; flex-direction: column;
}
.sidebar-header {
    padding: 24px 20px 16px; border-bottom: 1px solid rgba(255,255,255,0.08);
    font-size: 15px; font-weight: 600; color: #f1f5f9; letter-spacing: 0.3px;
}
.sidebar-header small {
    display: block; font-weight: 400; font-size: 12px; color: #94a3b8; margin-top: 4px;
}
.sidebar-nav { flex: 1; padding: 8px 0; list-style: none; }
.sidebar-nav li a {
    display: block; padding: 8px 20px; color: var(--sidebar-text);
    text-decoration: none; font-size: 13.5px; transition: all 0.15s;
    border-left: 3px solid transparent;
}
.sidebar-nav li a:hover { background: var(--sidebar-hover); color: #f1f5f9; }
.sidebar-nav li a.active {
    background: rgba(59,130,246,0.15); color: #60a5fa;
    border-left-color: var(--sidebar-active);
}
.sidebar-footer {
    padding: 12px 20px; border-top: 1px solid rgba(255,255,255,0.08);
    font-size: 12px; color: #64748b;
}
.main { margin-left: var(--sidebar-width); flex: 1; min-width: 0; }
.content { max-width: 860px; margin: 0 auto; padding: 48px 40px 40px; width: 100%; }
h1 { font-size: 28px; font-weight: 700; color: var(--heading); margin-bottom: 4px; }
h2 {
    font-size: 20px; font-weight: 600; color: var(--heading);
    margin-top: 40px; margin-bottom: 14px; padding-bottom: 8px;
    border-bottom: 1px solid var(--border);
}
h3 { font-size: 16px; font-weight: 600; color: var(--heading); margin-top: 28px; margin-bottom: 10px; }
h4 { font-size: 14px; font-weight: 600; color: var(--heading); margin-top: 20px; margin-bottom: 8px; }
p { margin-bottom: 12px; font-size: 15px; }
a { color: var(--link); text-decoration: none; }
a:hover { text-decoration: underline; }
code {
    background: var(--code-bg); padding: 2px 6px; border-radius: 4px;
    font-family: "JetBrains Mono", Consolas, monospace; font-size: 13px; color: var(--code-text);
}
pre {
    background: #1e293b; color: #e2e8f0; padding: 18px 20px;
    border-radius: 8px; overflow-x: auto; margin: 14px 0; font-size: 13px; line-height: 1.6;
}
pre code { background: none; color: inherit; padding: 0; font-size: inherit; }
table { width: 100%; border-collapse: collapse; margin: 14px 0 20px; font-size: 14px; }
th, td { border: 1px solid var(--border); padding: 10px 14px; text-align: left; }
th { background: #f8fafc; font-weight: 600; color: #374151; font-size: 13px; }
tr:nth-child(even) td { background: var(--table-stripe); }
blockquote {
    background: var(--blockquote-bg); border-left: 4px solid var(--blockquote-border);
    padding: 12px 18px; margin: 14px 0; border-radius: 0 6px 6px 0;
    color: #374151; font-size: 14px;
}
blockquote p { margin: 0; }
hr { border: none; border-top: 1px solid var(--border); margin: 28px 0; }
.section { scroll-margin-top: 30px; }
.tag {
    display: inline-block; background: #e0e7ff; color: #3730a3;
    padding: 2px 8px; border-radius: 4px; font-size: 12px; font-weight: 500; margin-bottom: 10px;
}
.features-grid {
    display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 6px; margin: 14px 0;
}
.feature-item {
    display: flex; align-items: flex-start; gap: 8px; font-size: 14px; padding: 6px 0;
}
.feature-item .icon { color: #22c55e; font-weight: bold; flex-shrink: 0; }
.arch-diagram {
    background: #f8fafc; border: 1px solid var(--border); border-radius: 8px;
    padding: 20px; margin: 14px 0;
    font-family: "JetBrains Mono", Consolas, monospace; font-size: 12px;
    line-height: 1.6; white-space: pre; overflow-x: auto; color: #334155;
}
ul, ol { margin: 10px 0 14px 24px; font-size: 15px; }
li { margin-bottom: 4px; }
.site-footer {
    margin-top: 48px; padding: 20px 0; border-top: 1px solid var(--border);
    text-align: center; font-size: 13px; color: var(--text-light);
}
.site-footer a { color: var(--link); font-weight: 500; }
.sidebar::-webkit-scrollbar { width: 5px; }
.sidebar::-webkit-scrollbar-track { background: transparent; }
.sidebar::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 3px; }
@media (max-width: 768px) {
    .sidebar { width: 220px; }
    .main { margin-left: 220px; }
    .content { padding: 24px 20px; }
}
</style>"""

# ─── JS ───
JS = r"""<script>
document.addEventListener("DOMContentLoaded", function() {
    const links = document.querySelectorAll(".sidebar-nav a");
    const sections = document.querySelectorAll(".section");
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                links.forEach(function(a) { a.classList.remove("active"); });
                const id = entry.target.id;
                const active = document.querySelector('.sidebar-nav a[href="#' + id + '"]');
                if (active) active.classList.add("active");
            }
        });
    }, { rootMargin: "-40px 0px -60% 0px" });
    sections.forEach(function(s) { observer.observe(s); });

    links.forEach(function(a) {
        a.addEventListener("click", function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute("href"));
            if (target) target.scrollIntoView({ behavior: "smooth" });
        });
    });
});
</script>"""


def build():
    print("Building documentation...")

    # ─── Build sidebar ───
    sidebar_items = []
    first = True
    for sid, title, _ in SECTIONS:
        active = ' class="active"' if first else ''
        sidebar_items.append(f'            <li><a href="#{sid}"{active}>{title}</a></li>')
        first = False

    sidebar = f"""<!-- ============ SIDEBAR ============ -->
<aside class="sidebar">
    <div class="sidebar-header">
        DLMTP_LinkPlay SDK
        <small>Unity 联机客户端文档 · v2.0</small>
    </div>
    <ul class="sidebar-nav">
{chr(10).join(sidebar_items)}
    </ul>
    <div class="sidebar-footer">
        <a href="https://github.com/your-repo/DLMTP_LinkPlay" target="_blank">GitHub →</a>
    </div>
</aside>"""

    # ─── Build content ───
    content_parts = []
    for i, (sid, title, filename) in enumerate(SECTIONS):
        md_text = strip_frontmatter(read_md(filename))
        html_body = md_to_html(md_text)
        # Wrap in section
        if sid == "overview":
            # Insert tag after the h1
            section_html = f"""        <!-- ====== {title} ====== -->
        <div class="section" id="{sid}">
            <span class="tag">命名空间: DLMTP_LinkPlay</span>
{html_body}
        </div>"""
        else:
            section_html = f"""        <!-- ====== {title} ====== -->
        <div class="section" id="{sid}">
{html_body}
        </div>"""

        content_parts.append(section_html)
        if i < len(SECTIONS) - 1:
            content_parts.append("")

    # ─── Footer ───
    footer = """        <div class="site-footer">
            <a href="https://github.com/your-repo/DLMTP_LinkPlay" target="_blank">View on GitHub</a>
            &nbsp;·&nbsp;
            <a href="https://github.com/your-repo/DLMTP_LinkPlay/issues" target="_blank">问题反馈</a>
            &nbsp;·&nbsp;
            文档版本 v2.0 · 最后更新 2026-05-17
        </div>"""

    # ─── Assemble ───
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DLMTP_LinkPlay SDK 文档</title>
{CSS}
</head>
<body>

{sidebar}

<!-- ============ MAIN ============ -->
<div class="main">
    <div class="content">

{chr(10).join(content_parts)}

{footer}
    </div>
</div>

{JS}
</body>
</html>"""

    output_path = os.path.join(DOCS_DIR, "index.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Generated: {output_path}")
    print(f"Size: {len(html):,} chars")


if __name__ == "__main__":
    build()
