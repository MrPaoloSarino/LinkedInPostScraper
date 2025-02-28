from playwright.sync_api import sync_playwright
import time
import random
import json
import os
from datetime import datetime

def human_delay(min_seconds, max_seconds):
    """Introduce a human-like delay with randomization."""
    time.sleep(random.uniform(min_seconds, max_seconds))

def scrape_current_page(page, max_posts, scroll_delay_min, scroll_delay_max,
                          scroll_amount_min, scroll_amount_max,
                          max_scroll_attempts, extra_pause_min, extra_pause_max):
    """
    Assumes the active page is the LinkedIn company posts page.
    Scrolls to load posts and extracts content with human-like automation.
    """
    posts_data = []
    # Verify we're on a company page by checking the URL.
    page_url = page.url.lower()
    if "linkedin.com/company/" not in page_url:
        print("Not on a LinkedIn company page. Please navigate to one and try again.")
        return posts_data

    # Scroll to load more posts dynamically.
    post_count = 0
    scroll_attempts = 0
    print("Scrolling to load posts...")
    while post_count < max_posts and scroll_attempts < max_scroll_attempts:
        current_posts = []
        for selector in [".feed-shared-update-v2", ".occludable-update", ".feed-shared-article"]:
            posts = page.locator(selector).all()
            if posts and len(posts) > len(current_posts):
                current_posts = posts
        post_count = len(current_posts)
        print(f"Found {post_count} posts so far...")
        
        # Scroll a random amount to simulate human behavior.
        scroll_amount = random.randint(scroll_amount_min, scroll_amount_max)
        page.mouse.wheel(0, scroll_amount)
        human_delay(scroll_delay_min, scroll_delay_max)
        scroll_attempts += 1
        
        # Optional extra pause.
        if random.random() < 0.2:
            longer_pause = random.uniform(extra_pause_min, extra_pause_max)
            time.sleep(longer_pause)

    # Extract post content using multiple selectors with retries.
    print("Extracting post content...")
    max_attempts = 5  # Maximum extraction attempts.
    attempts = 0
    extraction_done = False
    while attempts < max_attempts and not extraction_done:
        for selector in [".feed-shared-update-v2", ".occludable-update", ".feed-shared-article"]:
            posts = page.locator(selector).all()
            if posts and len(posts) > 0:
                print(f"Found {len(posts)} posts with selector: {selector}")
                for i, post in enumerate(posts[:max_posts]):
                    try:
                        post_text = None
                        # Try multiple selectors for the post text.
                        for text_selector in [
                            ".feed-shared-update-v2__description", 
                            ".update-components-text", 
                            ".feed-shared-text",
                            ".feed-shared-inline-show-more-text"
                        ]:
                            text_element = post.locator(text_selector).first
                            if text_element and text_element.is_visible():
                                post_text = text_element.text_content().strip()
                                if post_text:
                                    break
                        if not post_text:
                            print(f"Post {i+1} has no text content, skipping...")
                            continue
                        
                        post_date = "Unknown date"
                        for date_selector in [
                            ".feed-shared-actor__sub-description", 
                            ".feed-shared-actor__creation-time",
                            ".update-components-actor__sub-description"
                        ]:
                            date_element = post.locator(date_selector).first
                            if date_element and date_element.is_visible():
                                post_date = date_element.text_content().strip()
                                if post_date:
                                    break
                        
                        reactions = "0"
                        for reactions_selector in [
                            ".social-details-social-counts__reactions-count",
                            ".social-details-social-counts__count-value"
                        ]:
                            reactions_element = post.locator(reactions_selector).first
                            if reactions_element and reactions_element.is_visible():
                                reactions = reactions_element.text_content().strip()
                                if reactions:
                                    break

                        comments = "0 comments"
                        for comments_selector in [
                            ".social-details-social-counts__comments", 
                            ".social-details-social-counts__comments-count"
                        ]:
                            comments_element = post.locator(comments_selector).first
                            if comments_element and comments_element.is_visible():
                                comments = comments_element.text_content().strip()
                                if comments:
                                    break

                        posts_data.append({
                            "index": i + 1,
                            "date": post_date,
                            "text": post_text,
                            "reactions": reactions,
                            "comments": comments
                        })
                        print(f"Processed post {i+1}/{min(len(posts), max_posts)}")
                    except Exception as e:
                        print(f"Error extracting post {i+1}: {str(e)}")
                if posts_data:
                    extraction_done = True
                    break  # Stop checking other selectors if posts are found.
        if not extraction_done:
            attempts += 1
            print(f"Retrying post extraction (Attempt {attempts}/{max_attempts})...")
            time.sleep(random.uniform(3, 5))
    
    if not posts_data:
        print("No posts were extracted. Check if LinkedIn structure has changed.")
    return posts_data

def save_results(posts_data):
    """Save the scraped data to a JSON file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = "linkedin_data"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    filename = f"{output_dir}/posts_{timestamp}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(posts_data, f, indent=4, ensure_ascii=False)
    print(f"Results saved to {filename}")

def main():
    # Initial setup inputs for performance tuning.
    max_posts = int(input("Maximum number of posts to scrape (default 50): ") or "50")
    scroll_delay_min = float(input("Minimum scroll delay in seconds (default 1): ") or "1")
    scroll_delay_max = float(input("Maximum scroll delay in seconds (default 2): ") or "2")
    scroll_amount_min = int(input("Minimum scroll amount (default 500): ") or "500")
    scroll_amount_max = int(input("Maximum scroll amount (default 1200): ") or "1200")
    max_scroll_attempts = int(input("Maximum scroll attempts (default 25): ") or "25")
    login_wait_min = float(input("Minimum login wait time in seconds (default 5): ") or "5")
    login_wait_max = float(input("Maximum login wait time in seconds (default 8): ") or "8")
    extra_pause_min = float(input("Extra pause minimum in seconds (default 0.5): ") or "0.5")
    extra_pause_max = float(input("Extra pause maximum in seconds (default 1.5): ") or "1.5")
    
    with sync_playwright() as p:
        # Connect to your running Edge instance via CDP.
        try:
            browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        except Exception as e:
            print(f"Error connecting to your browser: {e}")
            return
        
        contexts = browser.contexts
        if contexts:
            context = contexts[0]
        else:
            context = browser.new_context()
        pages = context.pages
        if not pages:
            print("No pages found in the connected browser. Make sure Edge is running and has a page open.")
            return
        
        page = pages[0]
        print("Using page:", page.url)
        
        # Wait for login to complete.
        wait_time = random.uniform(login_wait_min, login_wait_max)
        print(f"Waiting {wait_time:.1f} seconds for login to complete...")
        time.sleep(wait_time)
        
        posts_data = scrape_current_page(page, max_posts, scroll_delay_min, scroll_delay_max,
                                         scroll_amount_min, scroll_amount_max,
                                         max_scroll_attempts, extra_pause_min, extra_pause_max)
        if posts_data:
            save_results(posts_data)
        else:
            print("No posts data was scraped.")
        
        browser.close()

if __name__ == "__main__":
    main()