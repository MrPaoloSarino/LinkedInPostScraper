# LinkedIn Company Posts Scraper

A human-like web scraper that extracts posts from LinkedIn company pages using Playwright and a CDP connection to an existing browser session.

## Overview

This tool connects to a running Edge browser instance to scrape posts from LinkedIn company pages. It's designed to mimic human browsing behavior with randomized scrolling and timing patterns to avoid detection.

## Features

- Connects to an existing browser session (Edge) to utilize your logged-in LinkedIn credentials
- Simulates human-like behavior with randomized delays and scrolling patterns
- Extracts post content, dates, reaction counts, and comment counts
- Configurable parameters for controlling scraping behavior
- Handles multiple CSS selectors to adapt to LinkedIn's UI structure
- Saves results as JSON files with timestamps

## Prerequisites

- Python 3.6+
- Playwright for Python
- A running Edge browser with remote debugging enabled

## Installation

1. Clone this repository
2. Install required packages:

```bash
pip install playwright
playwright install
```

## Usage

1. Start Edge with remote debugging enabled:

```bash
# Windows
"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --remote-debugging-port=9222

# macOS
/Applications/Microsoft\ Edge.app/Contents/MacOS/Microsoft\ Edge --remote-debugging-port=9222

# Linux
microsoft-edge --remote-debugging-port=9222
```

2. Log in to LinkedIn manually in the browser
3. Navigate to the company page you want to scrape (e.g., https://www.linkedin.com/company/microsoft/)
4. Run the script:

```bash
python linkedin_scraper.py
```

5. Follow the prompts to configure the scraping parameters (or press Enter to use defaults)

## Configuration Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `max_posts` | Maximum number of posts to scrape | 50 |
| `scroll_delay_min` | Minimum delay between scrolls (seconds) | 1 |
| `scroll_delay_max` | Maximum delay between scrolls (seconds) | 2 |
| `scroll_amount_min` | Minimum scroll amount (pixels) | 500 |
| `scroll_amount_max` | Maximum scroll amount (pixels) | 1200 |
| `max_scroll_attempts` | Maximum number of scroll attempts | 25 |
| `login_wait_min` | Minimum wait time after connecting (seconds) | 5 |
| `login_wait_max` | Maximum wait time after connecting (seconds) | 8 |
| `extra_pause_min` | Minimum extra pause time (seconds) | 0.5 |
| `extra_pause_max` | Maximum extra pause time (seconds) | 1.5 |

## Output

Results are saved in the `linkedin_data` directory as JSON files with the naming pattern `posts_YYYYMMDD_HHMMSS.json`. Each post contains:

- Index number
- Post date
- Post text content
- Reaction count
- Comment count

## How It Works

1. Connects to an existing Edge browser instance using CDP (Chrome DevTools Protocol)
2. Uses the first open page in the browser
3. Verifies the current page is a LinkedIn company page
4. Scrolls down to load posts dynamically with human-like behavior
5. Extracts post data using multiple selectors with retry logic
6. Saves the collected data to a JSON file

## Limitations

- Requires manual login to LinkedIn
- Depends on LinkedIn's current HTML structure (may need updates if LinkedIn changes their UI)
- Only works with Edge browser with remote debugging enabled
- Limited to scraping visible post content (no images or attachments)

## Disclaimer

This tool is for educational purposes only. Use responsibly and in accordance with LinkedIn's terms of service. Excessive scraping may lead to account restrictions.
