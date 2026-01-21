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

Write-Host "✅ Done! .github/workflows/autodoc.yml has been created." -ForegroundColor Green