#!/bin/bash

# Создаем папку, если ее нет
mkdir -p .github/workflows

# Записываем контент. 
# Внимание: мы экранируем только первый знак доллара \$
cat <<EOF > .github/workflows/autodoc.yml
name: AutoDoc
on: [workflow_dispatch]
jobs:
  run:
    permissions:
      contents: write
    uses: Drag-GameStudio/ADG/.github/workflows/reuseble_agd.yml@main
    secrets:
      GROCK_API_KEY: \${{ secrets.GROCK_API_KEY }}
EOF

echo "✅ Done! .github/workflows/autodoc.yml has been created."