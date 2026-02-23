#!/usr/bin/env python3
"""
Reads the article tag from each article file and syncs it to the
matching card in index.html. Run this before committing whenever
you change a tag in an article.

Usage: python3 sync-tags.py
"""

import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
ARTICLES_DIR = os.path.join(ROOT, 'articles')
INDEX_FILE = os.path.join(ROOT, 'index.html')


def get_article_tag(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    match = re.search(r'class="article-meta"[^<]*<span class="article-tag">([^<]+)</span>', content)
    return match.group(1) if match else None


def sync_tags():
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        index = f.read()

    changed = []

    for filename in sorted(os.listdir(ARTICLES_DIR)):
        if not filename.endswith('.html'):
            continue

        tag = get_article_tag(os.path.join(ARTICLES_DIR, filename))
        if not tag:
            continue

        # Match the article-tag span immediately before the h3 link for this file
        pattern = re.compile(
            r'(<div class="article-card">\s*<span class="article-tag">)'
            r'([^<]+)'
            r'(</span>\s*<h3><a href="articles/' + re.escape(filename) + r'")',
            re.DOTALL
        )

        match = pattern.search(index)
        if not match:
            continue

        current_tag = match.group(2)
        if current_tag != tag:
            index = pattern.sub(r'\g<1>' + tag + r'\g<3>', index)
            changed.append(f'  {filename}: {current_tag!r} → {tag!r}')

    if changed:
        with open(INDEX_FILE, 'w', encoding='utf-8') as f:
            f.write(index)
        print('Tags synced:')
        for c in changed:
            print(c)
    else:
        print('All tags already in sync.')


if __name__ == '__main__':
    sync_tags()
