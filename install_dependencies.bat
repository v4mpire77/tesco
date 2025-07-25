@echo off
echo Installing Tesco Scraper Dependencies...
echo.

REM Install Python packages
pip install requests beautifulsoup4 pandas lxml

echo.
echo Dependencies installed!
echo.
echo You can now run:
echo   python test_scraper.py    - To test the scraper
echo   python examples.py        - To run example scraping
echo   python tesco_scraper.py   - To run the main scraper
echo.
pause
