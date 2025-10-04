# 🎬 IMDb Review Analyzer with AI

A beautiful, AI-powered web application that analyzes IMDb movie and TV series reviews to provide instant recommendations.

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/YOUR_USERNAME/imdb-review-analyzer)

## ✨ Features

- 🔍 **Smart Search** - Search any movie or TV series with typo tolerance
- 🖼️ **Visual Results** - Movie posters displayed for easy identification
- 🤖 **AI Analysis** - Powered by DeepSeek V3.1 for sentiment analysis
- ⭐ **Rating System** - Get a rating out of 100 based on reviews
- 💡 **One-Line Recommendation** - Quick watch/skip advice
- 🎨 **Animated Background** - Beautiful UnicornStudio animations
- 📱 **Responsive Design** - Works perfectly on all devices
- 💾 **Save Results** - Download analysis as text file

## 🚀 Live Demo

**[View Live Demo](https://your-project.vercel.app)** (Replace with your Vercel URL)

## 📸 Screenshots

### Search Interface
![Search Interface](https://via.placeholder.com/800x400/667eea/ffffff?text=Search+Interface)

### Movie Selection with Posters
![Movie Selection](https://via.placeholder.com/800x400/667eea/ffffff?text=Movie+Selection)

### AI Analysis Results
![AI Results](https://via.placeholder.com/800x400/667eea/ffffff?text=AI+Analysis)

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Web Scraping**: BeautifulSoup4, Requests
- **AI**: OpenRouter API (DeepSeek V3.1)
- **Animation**: UnicornStudio
- **Deployment**: Vercel (Serverless)
- **Templating**: Jinja2

## 📋 Prerequisites

- Python 3.8+
- OpenRouter API Key ([Get one here](https://openrouter.ai))
- Git (for deployment)
- Vercel Account (for deployment)

## ⚙️ Local Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/imdb-review-analyzer.git
   cd imdb-review-analyzer
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env and add your OPENROUTER_API_KEY
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Open in browser**:
   ```
   http://localhost:8000
   ```

## 🌐 Vercel Deployment

See [VERCEL_DEPLOYMENT.md](VERCEL_DEPLOYMENT.md) for detailed deployment instructions.

### Quick Deploy:

1. Push to GitHub
2. Import to Vercel
3. Add `OPENROUTER_API_KEY` environment variable
4. Deploy!

## 📖 Documentation

- **[Vercel Deployment Guide](VERCEL_DEPLOYMENT.md)** - Complete deployment instructions
- **[Animated Background Feature](ANIMATED_BACKGROUND.md)** - Technical details on animations
- **[Poster Feature Guide](POSTER_FEATURE.md)** - How movie posters work
- **[Wrong Spelling Handling](WRONG_SPELLING_GUIDE.md)** - Typo tolerance system
- **[FastAPI Instructions](FASTAPI_INSTRUCTIONS.md)** - Local development guide

## 🎯 Usage

1. **Enter a movie or TV series name** (e.g., "Inception", "Breaking Bad")
2. **Select the correct title** from search results (if multiple)
3. **Wait 15-30 seconds** for AI analysis
4. **View results**:
   - Overall rating out of 100
   - Sentiment summary
   - Key points from reviews
   - One-line recommendation
   - Sample reviews

## 🔑 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENROUTER_API_KEY` | Your OpenRouter API key | Yes |

## 📁 Project Structure

```
imdb-review-analyzer/
├── app.py                      # FastAPI backend
├── index.py                    # Vercel entry point
├── vercel.json                 # Vercel configuration
├── requirements.txt            # Python dependencies
├── .env.example                # Environment template
├── .gitignore                 # Git ignore rules
├── templates/
│   └── index.html             # Frontend template
├── scraper.py                 # CLI version (bonus)
└── docs/                      # Documentation files
    ├── VERCEL_DEPLOYMENT.md
    ├── ANIMATED_BACKGROUND.md
    ├── POSTER_FEATURE.md
    └── ...
```

## 🎨 Features in Detail

### 1. Smart Search
- Handles typos and misspellings
- Shows multiple results when ambiguous
- Displays movie posters for visual identification

### 2. AI Analysis
- Analyzes up to 20 IMDb reviews
- Uses DeepSeek V3.1 for sentiment analysis
- Provides comprehensive summary
- Generates rating out of 100

### 3. Beautiful UI
- Glass morphism design
- Animated background
- Responsive layout
- Smooth animations

### 4. Error Handling
- Graceful fallbacks for missing posters
- Clear error messages
- Timeout handling
- Network error recovery

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **IMDb** - For movie data and reviews
- **OpenRouter** - For AI API access
- **DeepSeek** - For the V3.1 language model
- **UnicornStudio** - For animated backgrounds
- **Vercel** - For hosting platform
- **FastAPI** - For the awesome framework

## 🐛 Known Issues

- AI analysis may timeout on Vercel Free tier (10s limit)
  - **Solution**: Upgrade to Pro for 60s timeout
- Some old movies may not have posters
  - **Solution**: Placeholder image shown
- First request may be slow (cold start)
  - **Solution**: Vercel warms up after first use

## 🔮 Future Enhancements

- [ ] User authentication
- [ ] Save favorite movies
- [ ] Compare multiple movies
- [ ] Export to PDF
- [ ] Social sharing
- [ ] Multi-language support
- [ ] Dark mode toggle
- [ ] Advanced filters

## 📧 Contact

Your Name - [@yourtwitter](https://twitter.com/yourtwitter)

Project Link: [https://github.com/YOUR_USERNAME/imdb-review-analyzer](https://github.com/YOUR_USERNAME/imdb-review-analyzer)

## ⭐ Show Your Support

Give a ⭐️ if this project helped you!

---

**Made with ❤️ and AI** 🎬🤖✨
