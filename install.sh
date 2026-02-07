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


cat <<EOF > autodocconfig.yml
project_name: "$(basename "$PWD")"
language: "en"

ignore_files:
  # Python bytecode and cache
  - "*.pyc"
  - "*.pyo"
  - "*.pyd"
  - "__pycache__"
  - ".ruff_cache"
  - ".mypy_cache"
  - ".auto_doc_cache"
  # Environments and IDE settings
  - "venv"
  - "env"
  - ".venv"
  - ".env"
  - ".vscode"
  - ".idea"
  - "*.iml"
  # Databases and binary data
  - "*.sqlite3"
  - "*.db"
  - "*.pkl"
  - "data"
  # Logs and coverage reports
  - "*.log"
  - ".coverage"
  - "htmlcov"
  # Version control and assets
  - ".git"
  - ".gitignore"
  - "migrations"
  - "static"
  - "staticfiles"
  # Miscellaneous
  - "*.pdb"
  - "*.md"

build_settings:
  save_logs: false 
  log_level: 2
  

structure_settings:
  include_intro_links: true
  include_intro_text: true
  include_order: true
  
  use_global_file: true
  max_doc_part_size: 5000
EOF
echo "✅ Done! autodocconfig.yml has been created."