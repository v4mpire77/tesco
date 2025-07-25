# Tesco Scraper - GitHub Publisher
Write-Host "🚀 Publishing Tesco Scraper to GitHub..." -ForegroundColor Green
Write-Host ""

# Check if Git is installed
try {
    $gitVersion = git --version
    Write-Host "✅ Git found: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Git not found! Please install Git first:" -ForegroundColor Red
    Write-Host "   Download from: https://git-scm.com/download/win" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Press any key to exit..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

Write-Host ""

# Get repository name
$defaultRepoName = "tesco-scraper"
$repoName = Read-Host "Enter repository name (press Enter for '$defaultRepoName')"
if ([string]::IsNullOrWhiteSpace($repoName)) {
    $repoName = $defaultRepoName
}

Write-Host ""
Write-Host "📝 Setting up Git repository..." -ForegroundColor Yellow

# Initialize git if not already done
if (!(Test-Path ".git")) {
    git init
    Write-Host "✅ Git repository initialized" -ForegroundColor Green
} else {
    Write-Host "✅ Git repository already exists" -ForegroundColor Green
}

# Create .gitignore if it doesn't exist
if (!(Test-Path ".gitignore")) {
    @"
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
.venv/
venv/
ENV/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Project specific
static/downloads/
*.csv
*.json
test_*.csv
test_*.json

# Logs
*.log
"@ | Out-File -FilePath ".gitignore" -Encoding UTF8
    Write-Host "✅ .gitignore created" -ForegroundColor Green
}

# Add all files
Write-Host "📦 Adding files to repository..." -ForegroundColor Yellow
git add .

# Check if there are changes to commit
$status = git status --porcelain
if ($status) {
    # Commit changes
    $commitMessage = "Initial commit: Tesco Web Scraper with UI"
    git commit -m $commitMessage
    Write-Host "✅ Files committed: $commitMessage" -ForegroundColor Green
} else {
    Write-Host "ℹ️  No changes to commit" -ForegroundColor Blue
}

Write-Host ""
Write-Host "🌐 Next steps to publish on GitHub:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Go to https://github.com" -ForegroundColor White
Write-Host "2. Click the '+' button → 'New repository'" -ForegroundColor White
Write-Host "3. Repository name: $repoName" -ForegroundColor Yellow
Write-Host "4. Make it Public (so you can deploy for free)" -ForegroundColor White
Write-Host "5. DON'T initialize with README (we already have files)" -ForegroundColor White
Write-Host "6. Click 'Create repository'" -ForegroundColor White
Write-Host ""
Write-Host "7. Copy the repository URL and run:" -ForegroundColor White
Write-Host "   git remote add origin https://github.com/YOURUSERNAME/$repoName.git" -ForegroundColor Green
Write-Host "   git branch -M main" -ForegroundColor Green
Write-Host "   git push -u origin main" -ForegroundColor Green
Write-Host ""

# Offer to open GitHub
$openGitHub = Read-Host "Open GitHub in browser? (y/n)"
if ($openGitHub -eq 'y' -or $openGitHub -eq 'Y' -or $openGitHub -eq '') {
    Start-Process "https://github.com/new"
    Write-Host "✅ GitHub opened in browser" -ForegroundColor Green
}

Write-Host ""
Write-Host "🚀 After publishing to GitHub, you can deploy to:" -ForegroundColor Cyan
Write-Host "   • Render (Free): https://render.com" -ForegroundColor Green
Write-Host "   • Railway (Free): https://railway.app" -ForegroundColor Green
Write-Host "   • Vercel (Free): https://vercel.com" -ForegroundColor Green
Write-Host ""
Write-Host "📖 See HOW_TO_SHARE.md for detailed deployment instructions" -ForegroundColor Yellow

Write-Host ""
Write-Host "Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
