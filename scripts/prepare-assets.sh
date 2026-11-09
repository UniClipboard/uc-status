#!/bin/sh
set -eu
ref=${1:-origin/gh-pages}
commit=$(git rev-parse "$ref^{commit}")
python3 - <<'PYCODE'
from pathlib import Path
import shutil
p=Path('.build/assets')
if p.exists(): shutil.rmtree(p)
PYCODE
mkdir -p .build/assets
git archive "$commit" | tar -x -C .build/assets
python3 - <<'PYCODE'
from pathlib import Path
for name in ['CNAME','.nojekyll']:
    Path('.build/assets',name).unlink(missing_ok=True)
PYCODE
cat > .build/assets/_headers <<'EOF'
/*
  Cache-Control: no-cache
  X-Status-Host: cloudflare-workers
/client/*
  Cache-Control: public, max-age=31536000, immutable
EOF
printf '{"assetSource":"%s"}\n' "$commit" > .build/source.json
