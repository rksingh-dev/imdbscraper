from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import requests
from bs4 import BeautifulSoup
import json
import re
import os
from typing import Optional

app = FastAPI(title="IMDb Review Analyzer")

# Templates
templates = Jinja2Templates(directory="templates")

# OpenRouter API configuration
OPENROUTER_API_KEY = os.getenv(
    "OPENROUTER_API_KEY", 
    "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"
)
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Headers for IMDb requests
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render the home page"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/search")
async def search_movies(movie_name: str = Form(...)):
    """Search for movies and return multiple results for user selection"""
    try:
        # Search for the movie on IMDb
        search_url = f"https://www.imdb.com/find/?q={movie_name.replace(' ', '+')}&s=tt&ttype=ft,tv"
        search_response = requests.get(search_url, headers=HEADERS, timeout=10)
        
        if search_response.status_code != 200:
            return JSONResponse(
                status_code=400,
                content={"error": f"Failed to search IMDb. Status code: {search_response.status_code}"}
            )
        
        # Parse search results
        search_soup = BeautifulSoup(search_response.text, 'html.parser')
        
        # Find all title results
        results = []
        seen_ids = set()
        
        # Find all links to titles
        title_links = search_soup.find_all('a', href=re.compile(r'/title/tt\d+/'))
        
        for link in title_links[:15]:  # Get up to 15 results
            href = link.get('href', '')
            match = re.search(r'/title/(tt\d+)/', href)
            
            if match:
                imdb_id = match.group(1)
                
                # Avoid duplicates
                if imdb_id in seen_ids:
                    continue
                seen_ids.add(imdb_id)
                
                # Get title text
                title_text = link.get_text(strip=True)
                
                # Skip empty or very short titles
                if not title_text or len(title_text) < 2:
                    continue
                
                # Try to find additional info (year, type, poster)
                parent = link.find_parent(['li', 'div'])
                year = ""
                media_type = ""
                poster_url = ""
                
                if parent:
                    # Look for year
                    year_match = re.search(r'\((\d{4})\)', parent.get_text())
                    if year_match:
                        year = year_match.group(1)
                    
                    # Look for type (TV Series, Movie, etc.)
                    if 'TV Series' in parent.get_text():
                        media_type = 'TV Series'
                    elif 'TV Mini Series' in parent.get_text():
                        media_type = 'Mini Series'
                    else:
                        media_type = 'Movie'
                    
                    # Look for poster image
                    img_tag = parent.find('img')
                    if img_tag and img_tag.get('src'):
                        poster_url = img_tag.get('src')
                        # IMDb sometimes uses low-res placeholders, try to get higher res
                        if poster_url:
                            # Replace size parameters for better quality
                            poster_url = re.sub(r'_V1_.*?\.jpg', '_V1_UX300.jpg', poster_url)
                
                # If no poster found in parent, try to fetch from title page
                if not poster_url:
                    try:
                        title_page_url = f"https://www.imdb.com/title/{imdb_id}/"
                        title_response = requests.get(title_page_url, headers=HEADERS, timeout=5)
                        if title_response.status_code == 200:
                            title_soup = BeautifulSoup(title_response.text, 'html.parser')
                            
                            # Look for poster in various places
                            poster_img = title_soup.find('img', class_=re.compile(r'.*poster.*', re.I))
                            if not poster_img:
                                poster_img = title_soup.find('img', attrs={'data-testid': re.compile(r'.*poster.*', re.I)})
                            if not poster_img:
                                # Try meta tags
                                meta_img = title_soup.find('meta', property='og:image')
                                if meta_img:
                                    poster_url = meta_img.get('content', '')
                            
                            if poster_img and poster_img.get('src'):
                                poster_url = poster_img.get('src')
                    except:
                        pass  # If fetching poster fails, continue without it
                
                # Use placeholder if no poster found
                if not poster_url:
                    poster_url = "https://via.placeholder.com/300x450/667eea/ffffff?text=No+Poster"
                
                results.append({
                    'imdb_id': imdb_id,
                    'title': title_text,
                    'year': year,
                    'type': media_type,
                    'poster': poster_url
                })
        
        if not results:
            return JSONResponse(
                status_code=404,
                content={
                    "error": f"No results found for '{movie_name}'. Please check the spelling or try a different search term."
                }
            )
        
        return JSONResponse(content={
            "success": True,
            "results": results,
            "count": len(results)
        })
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"An error occurred: {str(e)}"}
        )

@app.post("/analyze")
async def analyze_movie(movie_name: str = Form(...), imdb_id: str = Form(None)):
    """Analyze movie reviews from IMDb"""
    try:
        # If imdb_id is provided, use it directly. Otherwise, search first
        if not imdb_id:
            # Search for the movie on IMDb
            search_url = f"https://www.imdb.com/find/?q={movie_name.replace(' ', '+')}&s=tt&ttype=ft,tv"
            search_response = requests.get(search_url, headers=HEADERS, timeout=10)
            
            if search_response.status_code != 200:
                return JSONResponse(
                    status_code=400,
                    content={"error": f"Failed to search IMDb. Status code: {search_response.status_code}"}
                )
            
            # Parse search results
            search_soup = BeautifulSoup(search_response.text, 'html.parser')
            title_links = search_soup.find_all('a', href=re.compile(r'/title/tt\d+/'))
            
            if not title_links:
                return JSONResponse(
                    status_code=404,
                    content={"error": f"No results found for '{movie_name}' on IMDb."}
                )
            
            # Get the first result's IMDb ID
            first_result = title_links[0]
            movie_url = first_result['href']
            match = re.search(r'/title/(tt\d+)/', movie_url)
            
            if not match:
                return JSONResponse(
                    status_code=400,
                    content={"error": "Could not extract IMDb ID from search results."}
                )
            
            imdb_id = match.group(1)
            title_text = first_result.get_text(strip=True)
        else:
            # IMDb ID provided, fetch title info
            title_text = movie_name  # Use provided name or fetch from IMDb
        
        reviews_url = f"https://www.imdb.com/title/{imdb_id}/reviews/"
        
        # Fetch reviews
        response = requests.get(reviews_url, headers=HEADERS, timeout=10)
        
        if response.status_code != 200:
            return JSONResponse(
                status_code=400,
                content={"error": f"Failed to fetch reviews. Status code: {response.status_code}"}
            )
        
        soup = BeautifulSoup(response.text, 'html.parser')
        reviews = soup.find_all('article')
        
        if len(reviews) == 0:
            return JSONResponse(
                status_code=404,
                content={"error": "No reviews found for this title."}
            )
        
        # Collect reviews for AI analysis
        all_reviews_text = []
        reviews_data = []
        
        for index, review in enumerate(reviews[:20], start=1):
            review_text = review.get_text(strip=True, separator=' ')
            lines = review_text.split()
            rating = "No rating"
            
            if len(lines) >= 3 and lines[1] == '/' and lines[2] == '10':
                rating = f"{lines[0]}/10"
                review_text = ' '.join(lines[3:])
            
            all_reviews_text.append(f"Rating: {rating}\nReview: {review_text[:500]}")
            reviews_data.append({
                "rating": rating,
                "text": review_text[:400]
            })
        
        # Prepare AI prompt
        reviews_combined = "\n\n".join(all_reviews_text)
        prompt = f"""Based on the following movie reviews, provide:
1. A brief summary of the overall sentiment and key points from the reviews
2. A one-line recommendation on whether to watch the movie or not
3. At the end, provide a rating out of 100 based on the sentiment and ratings in these reviews (format: "Overall Rating: X/100")

Reviews:
{reviews_combined}

Please provide your analysis."""

        # Call OpenRouter API
        ai_headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        
        ai_payload = {
            "model": "deepseek/deepseek-chat",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        
        ai_response = requests.post(OPENROUTER_API_URL, headers=ai_headers, json=ai_payload, timeout=30)
        
        if ai_response.status_code != 200:
            return JSONResponse(
                status_code=400,
                content={"error": f"AI API Error: {ai_response.status_code}"}
            )
        
        ai_result = ai_response.json()
        ai_summary = ai_result['choices'][0]['message']['content']
        
        # Extract rating from AI summary
        rating_match = re.search(r'(\d+)/100', ai_summary)
        ai_rating = rating_match.group(1) if rating_match else "N/A"
        
        # Save to file
        with open('movie_review_summary.txt', 'w', encoding='utf-8') as f:
            f.write("MOVIE REVIEW SUMMARY\n")
            f.write("=" * 80 + "\n")
            f.write(f"Movie/Series: {title_text}\n")
            f.write(f"IMDb ID: {imdb_id}\n")
            f.write(f"Reviews URL: {reviews_url}\n")
            f.write(f"Total Reviews Analyzed: {len(all_reviews_text)}\n")
            f.write("=" * 80 + "\n\n")
            f.write(ai_summary)
        
        return JSONResponse(content={
            "success": True,
            "movie_name": title_text,
            "imdb_id": imdb_id,
            "reviews_url": reviews_url,
            "total_reviews": len(all_reviews_text),
            "reviews": reviews_data[:10],  # Send first 10 reviews to display
            "ai_summary": ai_summary,
            "ai_rating": ai_rating
        })
        
    except requests.Timeout:
        return JSONResponse(
            status_code=408,
            content={"error": "Request timeout. Please try again."}
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"An error occurred: {str(e)}"}
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
