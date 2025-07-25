# Tesco Scraper Setup Script
Write-Host "Installing Tesco Scraper Dependencies..." -ForegroundColor Green
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version
    Write-Host "Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "Python not found! Please install Python first." -ForegroundColor Red
    exit 1
}

# Install required packages
Write-Host "Installing required packages..." -ForegroundColor Yellow
pip install requests beautifulsoup4 pandas lxml flask

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ Dependencies installed successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "You can now run:" -ForegroundColor Cyan
    Write-Host "  python launch_ui.py       - Start the Web UI (Recommended)" -ForegroundColor Yellow
    Write-Host "  python examples.py        - Run example scraping" -ForegroundColor White
    Write-Host "  python tesco_scraper.py   - Run the main scraper" -ForegroundColor White
    Write-Host "  python quick_test.py      - Test the scraper" -ForegroundColor White
    Write-Host ""
    Write-Host "🌐 To publish to GitHub and deploy online:" -ForegroundColor Cyan
    Write-Host "  .\publish_github.ps1      - Publish to GitHub" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "❌ Failed to install dependencies!" -ForegroundColor Red
}

Write-Host ""
Write-Host "Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
