#!/usr/bin/env python3
"""
FP-ASM Documentation HTML Generator

Converts markdown documentation to a beautiful HTML wiki-style website.

Usage:
    python generate_html_docs.py

Output:
    Creates 'docs/html/' directory with all HTML files
"""

import re
import os
import sys
import shutil
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DOCS_DIR = BASE_DIR / 'docs'
OUTPUT_DIR = DOCS_DIR / 'html'

# Allow importing helper utilities from the scripts/python directory
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.append(str(SCRIPT_DIR))

from extract_doxygen_docs import generate_api_markdown  # noqa: E402

# HTML Template
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - FP-ASM Library</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
        }}

        .container {{
            display: flex;
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            min-height: 100vh;
        }}

        /* Sidebar Navigation */
        .sidebar {{
            width: 280px;
            background: #2c3e50;
            color: white;
            padding: 20px;
            position: sticky;
            top: 0;
            height: 100vh;
            overflow-y: auto;
        }}

        .sidebar h2 {{
            color: #3498db;
            margin-bottom: 20px;
            font-size: 1.4em;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }}

        .sidebar nav ul {{
            list-style: none;
        }}

        .sidebar nav li {{
            margin: 8px 0;
        }}

        .sidebar nav a {{
            color: #ecf0f1;
            text-decoration: none;
            display: block;
            padding: 8px 12px;
            border-radius: 4px;
            transition: all 0.3s;
        }}

        .sidebar nav a:hover {{
            background: #34495e;
            color: #3498db;
            transform: translateX(5px);
        }}

        .sidebar nav a.active {{
            background: #3498db;
            color: white;
        }}

        .sidebar .badge {{
            display: inline-block;
            background: #27ae60;
            color: white;
            font-size: 0.7em;
            padding: 2px 6px;
            border-radius: 3px;
            margin-left: 8px;
        }}

        /* Main Content */
        .content {{
            flex: 1;
            padding: 40px 60px;
            overflow-y: auto;
        }}

        .content h1 {{
            color: #2c3e50;
            font-size: 2.5em;
            margin-bottom: 20px;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}

        .content h2 {{
            color: #34495e;
            font-size: 2em;
            margin-top: 40px;
            margin-bottom: 15px;
            border-left: 4px solid #3498db;
            padding-left: 15px;
        }}

        .content h3 {{
            color: #34495e;
            font-size: 1.5em;
            margin-top: 30px;
            margin-bottom: 10px;
        }}

        .content h4 {{
            color: #7f8c8d;
            font-size: 1.2em;
            margin-top: 20px;
            margin-bottom: 10px;
        }}

        .content p {{
            margin: 15px 0;
            line-height: 1.8;
        }}

        .content ul, .content ol {{
            margin: 15px 0 15px 30px;
        }}

        .content li {{
            margin: 8px 0;
        }}

        /* Code Blocks */
        .content pre {{
            background: #2c3e50;
            color: #ecf0f1;
            padding: 20px;
            border-radius: 6px;
            overflow-x: auto;
            margin: 20px 0;
            border-left: 4px solid #3498db;
        }}

        .content code {{
            background: #ecf0f1;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            color: #c7254e;
        }}

        .content pre code {{
            background: transparent;
            padding: 0;
            color: #ecf0f1;
        }}

        /* Tables */
        .content table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}

        .content th {{
            background: #3498db;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: bold;
        }}

        .content td {{
            padding: 12px;
            border-bottom: 1px solid #ecf0f1;
        }}

        .content tr:hover {{
            background: #f8f9fa;
        }}

        /* Badges */
        .badge-green {{
            background: #27ae60;
            color: white;
            padding: 4px 10px;
            border-radius: 4px;
            font-size: 0.85em;
            font-weight: bold;
        }}

        .badge-blue {{
            background: #3498db;
            color: white;
            padding: 4px 10px;
            border-radius: 4px;
            font-size: 0.85em;
            font-weight: bold;
        }}

        .badge-orange {{
            background: #e67e22;
            color: white;
            padding: 4px 10px;
            border-radius: 4px;
            font-size: 0.85em;
            font-weight: bold;
        }}

        /* Blockquotes */
        .content blockquote {{
            border-left: 4px solid #3498db;
            padding: 15px 20px;
            background: #ecf0f1;
            margin: 20px 0;
            font-style: italic;
        }}

        /* Links */
        .content a {{
            color: #3498db;
            text-decoration: none;
            border-bottom: 1px solid transparent;
            transition: border-color 0.3s;
        }}

        .content a:hover {{
            border-bottom-color: #3498db;
        }}

        /* Horizontal Rules */
        .content hr {{
            border: none;
            border-top: 2px solid #ecf0f1;
            margin: 40px 0;
        }}

        /* Emoji support */
        .emoji {{
            font-size: 1.2em;
        }}

        /* Top banner */
        .banner {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px 60px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}

        .banner h1 {{
            color: white;
            border: none;
            margin: 0;
            font-size: 1.8em;
        }}

        .banner p {{
            margin: 5px 0 0 0;
            opacity: 0.9;
        }}

        /* Function signature boxes */
        .signature {{
            background: #f8f9fa;
            border: 2px solid #3498db;
            border-radius: 6px;
            padding: 15px;
            margin: 20px 0;
            font-family: 'Courier New', monospace;
        }}

        /* Performance badges */
        .perf-badge {{
            display: inline-block;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: bold;
            margin: 5px 5px 5px 0;
        }}

        .perf-excellent {{ background: #27ae60; color: white; }}
        .perf-good {{ background: #2ecc71; color: white; }}
        .perf-okay {{ background: #f39c12; color: white; }}
        .perf-competitive {{ background: #3498db; color: white; }}

        /* Scrollbar styling */
        ::-webkit-scrollbar {{
            width: 10px;
        }}

        ::-webkit-scrollbar-track {{
            background: #f1f1f1;
        }}

        ::-webkit-scrollbar-thumb {{
            background: #888;
            border-radius: 5px;
        }}

        ::-webkit-scrollbar-thumb:hover {{
            background: #555;
        }}

        @media (max-width: 768px) {{
            .container {{
                flex-direction: column;
            }}

            .sidebar {{
                width: 100%;
                height: auto;
                position: relative;
            }}

            .content {{
                padding: 20px;
            }}

            .banner {{
                padding: 15px 20px;
            }}
        }}
    </style>
</head>
<body>
    <div class="banner">
        <h1>🚀 FP-ASM Library Documentation</h1>
        <p>Complete Functional Programming Toolkit for C • 100% FP Coverage • 36 Functions • Production Ready</p>
    </div>
    <div class="container">
        <aside class="sidebar">
            <h2>📚 Documentation</h2>
            <nav>
                <ul>
                    <li><a href="index.html" class="{active_index}">🏠 Home</a></li>
                    <li><a href="README.html" class="{active_readme}">📄 Overview</a></li>
                    <li><a href="wiki/index.html" class="{active_wiki}">📖 Wiki</a></li>
                    <li><a href="QUICK_START.html" class="{active_quick}">🚀 Quick Start</a></li>
                    <li><a href="EXAMPLES.html" class="{active_examples}">🧪 Practical Examples</a></li>
                    <li><a href="API_REFERENCE.html" class="{active_api}">📘 API Reference <span class="badge">36 funcs</span></a></li>
                    <li><a href="AUTO_API_REFERENCE.html" class="{active_auto_api}">🧵 Header Reference</a></li>
                    <li><a href="COMPLETE_LIBRARY_REPORT.html" class="{active_complete}">🎉 Journey Report</a></li>
                    <li><a href="TIER1_COMPLETENESS_REPORT.html" class="{active_tier1}">📊 TIER 1 Report</a></li>
                    <li><a href="TIER2_COMPLETENESS_REPORT.html" class="{active_tier2}">📊 TIER 2 Report</a></li>
                    <li><a href="TIER3_COMPLETENESS_REPORT.html" class="{active_tier3}">📊 TIER 3 Report</a></li>
                    <li><a href="ACHIEVEMENT_SUMMARY.html" class="{active_achievement}">🏆 Achievement</a></li>
                </ul>
            </nav>
        </aside>
        <main class="content">
            {content}
        </main>
    </div>
</body>
</html>
"""

WIKI_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} · FP-ASM Wiki</title>
    <style>
        body {{
            font-family: 'Linux Libertine', 'Georgia', 'Times New Roman', serif;
            margin: 0;
            padding: 0;
            background: #f6f6f6;
            color: #202122;
        }}

        a {{
            color: #0645ad;
            text-decoration: none;
        }}

        a:hover {{
            text-decoration: underline;
        }}

        header {{
            background: #ffffff;
            border-bottom: 1px solid #a2a9b1;
            padding: 16px 24px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: sticky;
            top: 0;
            z-index: 10;
        }}

        header .title {{
            font-size: 1.6em;
            font-weight: bold;
            color: #202122;
        }}

        header nav a {{
            margin-left: 18px;
            font-size: 0.95em;
            color: #3366cc;
        }}

        .page {{
            display: flex;
            max-width: 1400px;
            margin: 0 auto;
            padding: 24px;
            gap: 28px;
        }}

        .sidebar {{
            width: 260px;
            background: #ffffff;
            border: 1px solid #a2a9b1;
            border-radius: 4px;
            padding: 18px;
            height: fit-content;
        }}

        .sidebar h2 {{
            font-size: 1.1em;
            border-bottom: 1px solid #a2a9b1;
            margin-bottom: 12px;
            padding-bottom: 6px;
        }}

        .sidebar ul {{
            list-style: none;
            padding-left: 0;
            margin: 0;
        }}

        .sidebar li {{
            margin: 6px 0;
        }}

        .sidebar a {{
            display: block;
            padding: 6px 8px;
            border-radius: 4px;
            color: #0645ad;
            font-family: 'Segoe UI', Tahoma, sans-serif;
            font-size: 0.95em;
        }}

        .sidebar a.active {{
            background: #eaf3ff;
            font-weight: bold;
            border: 1px solid #a2a9b1;
        }}

        .article {{
            flex: 1;
            background: #ffffff;
            border: 1px solid #a2a9b1;
            border-radius: 4px;
            padding: 24px 32px;
            box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        }}

        .article h1 {{
            font-size: 2.3em;
            margin-top: 0;
            border-bottom: 1px solid #a2a9b1;
            padding-bottom: 8px;
            font-family: 'Linux Libertine', 'Georgia', serif;
        }}

        .article h2 {{
            font-size: 1.6em;
            border-bottom: 1px solid #a2a9b1;
            padding-bottom: 4px;
            margin-top: 32px;
        }}

        .article h3 {{
            font-size: 1.3em;
            margin-top: 24px;
            border-bottom: 1px dotted #c8ccd1;
            padding-bottom: 3px;
        }}

        .article p {{
            margin: 14px 0;
            line-height: 1.7;
        }}

        .article ul, .article ol {{
            margin: 12px 0 12px 24px;
        }}

        .article li {{
            margin: 6px 0;
        }}

        .article pre {{
            background: #f8f9fa;
            border: 1px solid #a2a9b1;
            padding: 16px;
            border-radius: 4px;
            overflow-x: auto;
        }}

        .article code {{
            background: #f1f2f4;
            padding: 2px 5px;
            border-radius: 3px;
            font-size: 0.9em;
        }}

        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 18px 0;
            background: #ffffff;
        }}

        th, td {{
            border: 1px solid #a2a9b1;
            padding: 8px 12px;
            text-align: left;
        }}

        th {{
            background: #eaecf0;
        }}

        .infobox {{
            float: right;
            width: 320px;
            margin: 0 0 18px 24px;
            font-size: 0.9em;
            background: #f8f9fa;
        }}

        .article blockquote {{
            border-left: 3px solid #a2a9b1;
            margin: 18px 0;
            padding: 10px 18px;
            background: #f8f9fa;
            font-style: italic;
        }}

        .footer-note {{
            margin-top: 36px;
            font-size: 0.85em;
            color: #54595d;
            border-top: 1px solid #a2a9b1;
            padding-top: 12px;
        }}

        @media (max-width: 992px) {{
            .page {{
                flex-direction: column;
            }}

            .sidebar {{
                width: 100%;
            }}

            .infobox {{
                float: none;
                width: 100%;
                margin: 0 0 18px 0;
            }}
        }}
    </style>
</head>
<body>
    <header>
        <div class="title">📖 FP-ASM Knowledge Base</div>
        <nav>
            <a href="../index.html">Documentation Home</a>
            <a href="../README.html">Overview</a>
            <a href="../API_REFERENCE.html">API Reference</a>
        </nav>
    </header>
    <div class="page">
        <aside class="sidebar">
            <h2>Wiki Pages</h2>
            <ul>
                {sidebar}
            </ul>
        </aside>
        <main class="article">
            <h1>{title}</h1>
            {content}
            <div class="footer-note">This article was generated on {generated_on}.</div>
        </main>
    </div>
</body>
</html>
"""

def convert_markdown_to_html(markdown_text):
    """Convert markdown to HTML with basic formatting."""
    html = markdown_text

    # Headers
    html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^#### (.+)$', r'<h4>\1</h4>', html, flags=re.MULTILINE)

    # Code blocks
    html = re.sub(r'```(\w+)?\n(.*?)```', r'<pre><code>\2</code></pre>', html, flags=re.DOTALL)

    # Inline code
    html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)

    # Bold
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)

    # Italic
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)

    # Links
    html = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2">\1</a>', html)

    # Horizontal rules
    html = re.sub(r'^---+$', r'<hr>', html, flags=re.MULTILINE)

    # Lists (simple)
    html = re.sub(r'^\- (.+)$', r'<li>\1</li>', html, flags=re.MULTILINE)
    html = re.sub(r'(<li>.*</li>)', r'<ul>\1</ul>', html, flags=re.DOTALL)

    # Numbered lists
    html = re.sub(r'^\d+\. (.+)$', r'<li>\1</li>', html, flags=re.MULTILINE)

    # Tables (basic)
    def convert_table(match):
        lines = match.group(0).split('\n')
        if len(lines) < 3:
            return match.group(0)

        table = '<table>\n'

        # Header
        headers = [h.strip() for h in lines[0].split('|')[1:-1]]
        table += '<tr>'
        for h in headers:
            table += f'<th>{h}</th>'
        table += '</tr>\n'

        # Rows (skip separator line)
        for line in lines[2:]:
            if line.strip():
                cells = [c.strip() for c in line.split('|')[1:-1]]
                table += '<tr>'
                for c in cells:
                    table += f'<td>{c}</td>'
                table += '</tr>\n'

        table += '</table>'
        return table

    html = re.sub(r'\|[^\n]+\|\n\|[-:\| ]+\|\n(\|[^\n]+\|\n)+', convert_table, html)

    # Paragraphs
    lines = html.split('\n')
    in_block = False
    result = []

    for line in lines:
        stripped = line.strip()

        if stripped.startswith(('<h', '<pre>', '<ul>', '<ol>', '<table>', '<hr>', '<li>')):
            in_block = True
            result.append(line)
        elif stripped.startswith(('</pre>', '</ul>', '</ol>', '</table>')):
            in_block = False
            result.append(line)
        elif stripped == '':
            result.append(line)
        elif not in_block and stripped and not stripped.startswith('<'):
            result.append(f'<p>{line}</p>')
        else:
            result.append(line)

    html = '\n'.join(result)

    # Convert emojis to spans
    emoji_pattern = r'([\U0001F300-\U0001F9FF]|[\u2600-\u26FF]|[\u2700-\u27BF])'
    html = re.sub(emoji_pattern, r'<span class="emoji">\1</span>', html)

    return html

def slugify(title: str) -> str:
    """Convert a wiki page title into a filesystem-friendly slug."""
    slug = re.sub(r'[^A-Za-z0-9]+', '-', title.strip())
    slug = re.sub(r'-{2,}', '-', slug)
    slug = slug.strip('-')
    return slug or 'page'

def generate_wiki_pages():
    """Generate a Wikipedia-style site from the github-wiki markdown files."""
    wiki_source = BASE_DIR / 'github-wiki'
    if not wiki_source.exists():
        print(f"[WARN] Skipping wiki generation (missing directory: {wiki_source})")
        return 0

    wiki_files = sorted(
        wiki_source.glob('*.md'),
        key=lambda path: (0 if path.stem.lower() == 'home' else 1, path.stem.lower()),
    )

    if not wiki_files:
        print(f"[WARN] No markdown files found in {wiki_source}, skipping wiki generation")
        return 0

    wiki_output = OUTPUT_DIR / 'wiki'
    if wiki_output.exists():
        shutil.rmtree(wiki_output)
    wiki_output.mkdir(parents=True, exist_ok=True)

    pages = []
    for path in wiki_files:
        title = path.stem
        slug = slugify(title)
        pages.append({'title': title, 'slug': slug, 'path': path})

    title_to_slug = {}
    for page in pages:
        title_to_slug[page['title']] = page['slug']
        title_to_slug[page['title'].lower()] = page['slug']

    print(f"[*] Generating wiki HTML ({len(pages)} pages)...")
    generated = 0

    for page in pages:
        with open(page['path'], 'r', encoding='utf-8') as f:
            markdown = f.read()

        def replace_wiki_links(match):
            label = match.group(1).strip()
            slug = title_to_slug.get(label) or title_to_slug.get(label.lower()) or slugify(label)
            return f'[{label}]({slug}.html)'

        markdown = re.sub(r'\[\[([^\]]+)\]\]', replace_wiki_links, markdown)

        html_content = convert_markdown_to_html(markdown)
        # Drop the leading H1 because the template provides the page title headline
        html_content = re.sub(r'^<h1>.*?</h1>\n?', '', html_content, count=1, flags=re.DOTALL)

        sidebar_items = []
        for item in pages:
            css_class = 'active' if item['slug'] == page['slug'] else ''
            sidebar_items.append(
                f'<li><a class="{css_class}" href="{item["slug"]}.html">{item["title"]}</a></li>'
            )

        sidebar_html = '\n'.join(sidebar_items)
        generated_on = datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')

        final_html = WIKI_TEMPLATE.format(
            title=page['title'],
            content=html_content,
            sidebar=sidebar_html,
            generated_on=generated_on,
        )

        output_path = wiki_output / f"{page['slug']}.html"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(final_html)

        print(f"    [OK] {page['title']} -> {output_path.relative_to(BASE_DIR)}")
        generated += 1

    # Duplicate the Home page to index.html for convenience
    home_page = next((p for p in pages if p['slug'].lower() == 'home'), pages[0])
    home_html = wiki_output / f"{home_page['slug']}.html"
    shutil.copyfile(home_html, wiki_output / 'index.html')
    print(f"    [OK] index.html -> wiki/{home_page['slug']}.html")

    return generated + 1  # include index.html copy

def create_index_page():
    """Create the main index page."""
    content = """
<h1>Welcome to FP-ASM Library Documentation</h1>

<p>A complete, production-ready functional programming toolkit for C with hand-optimized x64 assembly and AVX2 SIMD acceleration.</p>

<h2>🎯 Quick Navigation</h2>

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin: 30px 0;">
    <div style="padding: 20px; background: #ecf0f1; border-radius: 8px; border-left: 4px solid #3498db;">
        <h3>📖 Getting Started</h3>
        <p>New to FP-ASM? Start here!</p>
        <a href="README.html">Read the Overview</a> •
        <a href="QUICK_START.html">Quick Start Tutorial</a>
    </div>

    <div style="padding: 20px; background: #ecf0f1; border-radius: 8px; border-left: 4px solid #27ae60;">
        <h3>🧪 Examples & Guides</h3>
        <p>See the library in action with complete samples</p>
        <a href="EXAMPLES.html">Hands-on Examples</a> •
        <a href="AUTO_API_REFERENCE.html">Header Commentary</a>
    </div>

    <div style="padding: 20px; background: #ecf0f1; border-radius: 8px; border-left: 4px solid #e67e22;">
        <h3>🎉 Achievement Reports</h3>
        <p>See the journey to 100% completion</p>
        <a href="COMPLETE_LIBRARY_REPORT.html">Journey Report</a> •
        <a href="ACHIEVEMENT_SUMMARY.html">Final Summary</a>
    </div>
</div>

<h2>📊 Library Statistics</h2>

<table>
    <tr>
        <th>Metric</th>
        <th>Value</th>
    </tr>
    <tr>
        <td><strong>Total Functions</strong></td>
        <td><span class="badge-green">36</span></td>
    </tr>
    <tr>
        <td><strong>Assembly Modules</strong></td>
        <td><span class="badge-blue">10</span></td>
    </tr>
    <tr>
        <td><strong>FP Completeness</strong></td>
        <td><span class="badge-green">100%</span></td>
    </tr>
    <tr>
        <td><strong>Performance Range</strong></td>
        <td><span class="badge-orange">1.0-4.0x vs GCC -O3</span></td>
    </tr>
    <tr>
        <td><strong>Platform</strong></td>
        <td>Windows x64 • AVX2</td>
    </tr>
    <tr>
        <td><strong>Status</strong></td>
        <td><span class="badge-green">Production Ready</span></td>
    </tr>
</table>

<h2>🚀 Quick Example</h2>

<pre><code>#include &lt;stdio.h&gt;
#include "fp_core.h"

int main() {
    // Sum an array (1.5-1.8x faster than C)
    int64_t numbers[] = {1, 2, 3, 4, 5};
    int64_t sum = fp_reduce_add_i64(numbers, 5);
    printf("Sum: %lld\\n", sum);  // Output: 15

    // Find median
    double data[] = {25.3, 19.2, 28.5, 21.8};
    fp_sort_f64(data, 4);
    printf("Median: %.1f\\n", data[2]);

    return 0;
}
</code></pre>

<p><strong>Compile:</strong> <code>gcc your_program.c fp_core_*.o -o your_program.exe</code></p>

<h2>🎓 What Makes FP-ASM Special?</h2>

<ul>
    <li><strong>✅ 100% Complete</strong> - All standard FP operations from Haskell/ML/Lisp</li>
    <li><strong>⚡ High Performance</strong> - 1.0-4.0x faster than GCC -O3</li>
    <li><strong>🔧 Production Ready</strong> - Tested, documented, ABI-compliant</li>
    <li><strong>📦 Zero Dependencies</strong> - Just include and link</li>
    <li><strong>🎯 Type Safe</strong> - Separate i64 and f64 variants</li>
    <li><strong>📚 Well Documented</strong> - 170+ KB of guides and references</li>
</ul>

<h2>📖 Documentation Overview</h2>

<ul>
    <li><strong><a href="README.html">README</a></strong> - Main overview and quick examples</li>
    <li><strong><a href="QUICK_START.html">Quick Start</a></strong> - Tutorial from basics to advanced</li>
    <li><strong><a href="API_REFERENCE.html">API Reference</a></strong> - Complete docs for all 36 functions</li>
    <li><strong><a href="AUTO_API_REFERENCE.html">Header Reference</a></strong> - Auto generated from Doxygen comments</li>
    <li><strong><a href="EXAMPLES.html">Practical Examples</a></strong> - End-to-end scenarios using the API</li>
    <li><strong><a href="COMPLETE_LIBRARY_REPORT.html">Journey Report</a></strong> - 40% → 100% story</li>
    <li><strong><a href="TIER1_COMPLETENESS_REPORT.html">TIER 1 Report</a></strong> - List operations (scans, filter, partition)</li>
    <li><strong><a href="TIER2_COMPLETENESS_REPORT.html">TIER 2 Report</a></strong> - Sorting & sets details</li>
    <li><strong><a href="TIER3_COMPLETENESS_REPORT.html">TIER 3 Report</a></strong> - Grouping, unfold, boolean operations</li>
    <li><strong><a href="ACHIEVEMENT_SUMMARY.html">Achievement Summary</a></strong> - Final celebration</li>
</ul>

<hr>

<p style="text-align: center; color: #7f8c8d; margin-top: 40px;">
    <em>Bringing Haskell's elegance to C's performance. One assembly instruction at a time.</em> 💙⚡
</p>
"""
    return content

def generate_html_docs():
    """Generate HTML documentation from markdown files."""
    print("[*] FP-ASM HTML Documentation Generator")
    print("=" * 60)

    # Create output directory
    output_dir = OUTPUT_DIR
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"[OK] Created output directory: {output_dir}")

    # Ensure the autogenerated API reference is up to date
    auto_api_path = generate_api_markdown()
    print(f"[OK] Refreshed autogenerated docs: {auto_api_path}")

    # Markdown files to convert
    md_files = [
        BASE_DIR / "README.md",
        DOCS_DIR / "QUICK_START.md",
        DOCS_DIR / "EXAMPLES.md",
        DOCS_DIR / "API_REFERENCE.md",
        DOCS_DIR / "AUTO_API_REFERENCE.md",
        DOCS_DIR / "COMPLETE_LIBRARY_REPORT.md",
        DOCS_DIR / "TIER1_COMPLETENESS_REPORT.md",
        DOCS_DIR / "TIER2_COMPLETENESS_REPORT.md",
        DOCS_DIR / "TIER3_COMPLETENESS_REPORT.md",
        DOCS_DIR / "ACHIEVEMENT_SUMMARY.md"
    ]

    converted = 0

    # Convert each markdown file
    for md_path in md_files:
        if not md_path.exists():
            print(f"[WARN] Skipping {md_path.name} (not found)")
            continue

        md_name = md_path.name
        print(f"[*] Converting {md_name}...", end=" ")

        # Read markdown
        with open(md_path, 'r', encoding='utf-8') as f:
            markdown_content = f.read()

        # Convert to HTML
        html_content = convert_markdown_to_html(markdown_content)

        # Determine active page for navigation
        active_flags = {
            'active_index': '',
            'active_readme': '',
            'active_wiki': '',
            'active_quick': '',
            'active_examples': '',
            'active_api': '',
            'active_auto_api': '',
            'active_complete': '',
            'active_tier1': '',
            'active_tier2': '',
            'active_tier3': '',
            'active_achievement': ''
        }

        if md_name == "README.md":
            active_flags['active_readme'] = 'active'
        elif md_name == "QUICK_START.md":
            active_flags['active_quick'] = 'active'
        elif md_name == "EXAMPLES.md":
            active_flags['active_examples'] = 'active'
        elif md_name == "API_REFERENCE.md":
            active_flags['active_api'] = 'active'
        elif md_name == "AUTO_API_REFERENCE.md":
            active_flags['active_auto_api'] = 'active'
        elif md_name == "COMPLETE_LIBRARY_REPORT.md":
            active_flags['active_complete'] = 'active'
        elif md_name == "TIER1_COMPLETENESS_REPORT.md":
            active_flags['active_tier1'] = 'active'
        elif md_name == "TIER2_COMPLETENESS_REPORT.md":
            active_flags['active_tier2'] = 'active'
        elif md_name == "TIER3_COMPLETENESS_REPORT.md":
            active_flags['active_tier3'] = 'active'
        elif md_name == "ACHIEVEMENT_SUMMARY.md":
            active_flags['active_achievement'] = 'active'

        # Get title from first h1
        title_match = re.search(r'<h1>(.+?)</h1>', html_content)
        title = title_match.group(1) if title_match else "FP-ASM"
        title = re.sub(r'<[^>]+>', '', title)  # Strip HTML tags from title

        # Generate final HTML
        final_html = HTML_TEMPLATE.format(
            title=title,
            content=html_content,
            **active_flags
        )

        # Fix markdown links to HTML links
        final_html = final_html.replace('.md"', '.html"')
        final_html = final_html.replace('.md#', '.html#')
        final_html = final_html.replace('../README.html', 'README.html')
        final_html = final_html.replace('../README.md', 'README.html')
        final_html = final_html.replace('href="html/', 'href="')

        # Write HTML file
        html_path = output_dir / md_path.with_suffix('.html').name
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(final_html)

        print(f"[OK] -> {html_path}")
        converted += 1

    # Create index.html
    print("[*] Creating index.html...", end=" ")
    index_content = create_index_page()
    index_html = HTML_TEMPLATE.format(
        title="Home",
        content=index_content,
        active_index='active',
        active_readme='',
        active_wiki='',
        active_quick='',
        active_examples='',
        active_api='',
        active_auto_api='',
        active_complete='',
        active_tier1='',
        active_tier2='',
        active_tier3='',
        active_achievement=''
    )
    with open(output_dir / "index.html", 'w', encoding='utf-8') as f:
        f.write(index_html)
    print("[OK]")

    wiki_generated = generate_wiki_pages()
    if wiki_generated:
        print(f"[OK] Generated wiki site with {wiki_generated} HTML files")

    print("\n" + "=" * 60)
    total_pages = converted + 1 + wiki_generated
    print(f"[SUCCESS] Generated {converted + 1} documentation pages and {wiki_generated} wiki pages ({total_pages} total)!")
    print(f"[DIR] Output directory: {output_dir.absolute()}")
    print(f"\n[BROWSER] Open: file:///{output_dir.absolute()}/index.html")
    print("=" * 60)

if __name__ == "__main__":
    generate_html_docs()
