#!/bin/sh
# Workers Builds checks out the generated gh-pages branch, not the source branch.
set -eu
for file in wrangler.jsonc worker.js; do
    git show "origin/master:$file" > "$file"
done
git fetch origin gh-pages:refs/remotes/origin/gh-pages --depth=1
mkdir -p .build
git show origin/master:scripts/prepare-assets.sh > .build/prepare-assets.sh
git show origin/master:e2e/acceptance.py > .build/http-acceptance.py
sh .build/prepare-assets.sh origin/gh-pages
