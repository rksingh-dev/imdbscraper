import requests
from bs4 import BeautifulSoup
import json
import re

print("=" * 80)
print("🎬 IMDb Movie/Series Review Analyzer with AI")
print("=" * 80)

# OpenRouter API configuration
OPENROUTER_API_KEY = "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"
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Get user input
print("\n📝 Enter the name of a movie or web series:")
movie_name = input("➤ ").strip()

if not movie_name:
    print("❌ Error: Movie name cannot be empty!")
    exit()

print(f"\n🔍 Searching for '{movie_name}' on IMDb...")

# Add headers to mimic a real browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

# Search for the movie on IMDb
search_url = f"https://www.imdb.com/find/?q={movie_name.replace(' ', '+')}&s=tt&ttype=ft,tv"
search_response = requests.get(search_url, headers=headers)

if search_response.status_code != 200:
    print(f"❌ Failed to search IMDb. Status code: {search_response.status_code}")
    exit()

# Parse search results
search_soup = BeautifulSoup(search_response.text, 'html.parser')

# Find the first result
# IMDb search results are in <a> tags with href containing /title/
title_links = search_soup.find_all('a', href=re.compile(r'/title/tt\d+/'))

if not title_links:
    print(f"❌ No results found for '{movie_name}' on IMDb.")
    print("💡 Try a different search term or check the spelling.")
    exit()

# Get the first result's IMDb ID
first_result = title_links[0]
movie_url = first_result['href']
# Extract just the title ID (e.g., /title/tt1234567/)
match = re.search(r'/title/(tt\d+)/', movie_url)
if match:
    imdb_id = match.group(1)
    reviews_url = f"https://www.imdb.com/title/{imdb_id}/reviews/"
    
    # Get the movie title
    title_text = first_result.get_text(strip=True)
    print(f"✅ Found: {title_text}")
    print(f"🔗 IMDb ID: {imdb_id}")
    print(f"📄 Reviews URL: {reviews_url}")
else:
    print("❌ Could not extract IMDb ID from search results.")
    exit()

# Now fetch the reviews
print(f"\n📥 Fetching reviews from IMDb...")

response = requests.get(reviews_url, headers=headers)
print(f"Received response with status code: {response.status_code}")

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    print("Successfully parsed the HTML.")
    
    # Find review articles on IMDb
    reviews = soup.find_all('article')
    
    print(f"\nFound {len(reviews)} reviews.\n")
    print("=" * 80)
    
    # Collect all reviews for AI summarization
    all_reviews_text = []
    
    if len(reviews) > 0:
        for index, review in enumerate(reviews[:20], start=1):  # Collect first 20 reviews
            # Extract review text
            review_text = review.get_text(strip=True, separator=' ')
            
            # Try to extract rating (usually starts with "X / 10")
            lines = review_text.split()
            rating = "No rating"
            if len(lines) >= 3 and lines[1] == '/' and lines[2] == '10':
                rating = f"{lines[0]}/10"
                # Remove rating from the beginning of text
                review_text = ' '.join(lines[3:])
            
            # Store for AI analysis
            all_reviews_text.append(f"Rating: {rating}\nReview: {review_text[:500]}")
            
            print(f"\n📝 Review #{index}")
            print(f"⭐ Rating: {rating}")
            print(f"💬 Review: {review_text[:400]}...")  # Show first 400 characters
            print("-" * 80)
        
        # Now use AI to summarize the reviews
        print("\n\n🤖 AI Analysis in Progress...")
        print("=" * 80)
        
        # Prepare the prompt for AI
        reviews_combined = "\n\n".join(all_reviews_text)
        prompt = f"""Based on the following movie reviews, provide:
1. A brief summary of the overall sentiment and key points from the reviews
2. A one-line recommendation on whether to watch the movie or not
3. At the end, provide a rating out of 100 based on the sentiment and ratings in these reviews (format: "Overall Rating: X/100")

Reviews:
{reviews_combined}

Please provide your analysis."""

        # Call OpenRouter API
        try:
            ai_headers = {
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            }
            
            ai_payload = {
                "model": "deepseek/deepseek-chat",  # DeepSeek V3.1 free model
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }
            
            print("Sending request to DeepSeek AI...")
            ai_response = requests.post(OPENROUTER_API_URL, headers=ai_headers, json=ai_payload)
            
            if ai_response.status_code == 200:
                ai_result = ai_response.json()
                ai_summary = ai_result['choices'][0]['message']['content']
                
                print("\n✨ AI SUMMARY:")
                print("=" * 80)
                print(ai_summary)
                print("=" * 80)
                
                # Save summary to file
                with open('movie_review_summary.txt', 'w', encoding='utf-8') as f:
                    f.write("MOVIE REVIEW SUMMARY\n")
                    f.write("=" * 80 + "\n")
                    f.write(f"Movie/Series: {title_text}\n")
                    f.write(f"IMDb ID: {imdb_id}\n")
                    f.write(f"Reviews URL: {reviews_url}\n")
                    f.write(f"Total Reviews Analyzed: {len(all_reviews_text)}\n")
                    f.write("=" * 80 + "\n\n")
                    f.write(ai_summary)
                
                print("\n💾 Summary saved to 'movie_review_summary.txt'")
            else:
                print(f"\n❌ AI API Error: {ai_response.status_code}")
                print(f"Response: {ai_response.text}")
        
        except Exception as e:
            print(f"\n❌ Error calling AI API: {str(e)}")
    else:
        print("⚠️  No reviews found. The page structure may have changed.")
        print("Try checking the URL or IMDb's website structure.")
else:
    print(f"❌ Failed to retrieve the page. Status code: {response.status_code}")
    print("\n💡 Possible reasons:")
    print("  - IMDb is blocking the request (needs better headers)")
    print("  - Network connection issue")
    print("  - Invalid URL")
