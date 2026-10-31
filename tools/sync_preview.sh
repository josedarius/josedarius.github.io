#!/bin/sh
# Copy the redesign-v2 branch into ./preview (noindex) on the current branch.
set -e
tmp=$(mktemp -d)
git --work-tree="$tmp" checkout redesign-v2 -- . && git reset -q
rm -rf preview && mkdir -p preview/assets
cp -r "$tmp"/index.html "$tmp"/about.html "$tmp"/contact.html "$tmp"/products.html "$tmp"/services.html "$tmp"/solutions.html "$tmp"/products "$tmp"/services "$tmp"/solutions preview/
mkdir -p preview/assets/css preview/assets/js preview/assets/images preview/assets/favicon preview/assets/downloads
cp "$tmp"/assets/css/v2.css preview/assets/css/; cp "$tmp"/assets/js/v2.js preview/assets/js/
cp "$tmp"/assets/images/mycloudsme-logo.png "$tmp"/assets/images/DPIIT.jpeg preview/assets/images/
cp "$tmp"/assets/favicon/* preview/assets/favicon/; cp "$tmp"/assets/downloads/* preview/assets/downloads/
find preview -name '*.html' -exec sed -i 's#<meta name="viewport" content="width=device-width, initial-scale=1" />#&\n  <meta name="robots" content="noindex, nofollow" />#' {} +
rm -rf "$tmp"
