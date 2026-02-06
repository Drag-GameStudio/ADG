# Создаем директорию, если она не существует
New-Item -ItemType Directory -Force -Path .github/workflows

# Используем одинарные кавычки для обрамления текста (here-string), 
# чтобы PowerShell не пытался искать переменные внутри
$content = @'
name: AutoDoc
on: [workflow_dispatch]
jobs:
  run:
    permissions:
      contents: write
    uses: Drag-GameStudio/ADG/.github/workflows/reuseble_agd.yml@main
    secrets:
      GROCK_API_KEY: ${{ secrets.GROCK_API_KEY }}
'@

# Сохраняем в файл
$content | Out-File -FilePath .github/workflows/autodoc.yml -Encoding utf8

# Получаем название текущей папки
$currentFolderName = (Get-Item .).Name

# Формируем строку с использованием переменной
$configContent = @"
project_name: "$currentFolderName"
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
  use_global_file: true
  include_order: true
  max_doc_part_size: 5000
"@
$configContent | Out-File -FilePath autodocconfig.yml -Encoding utf8

Write-Host "✅ Done! .github/workflows/autodoc.yml has been created. autodocconfig.yml has been created." -ForegroundColor Green