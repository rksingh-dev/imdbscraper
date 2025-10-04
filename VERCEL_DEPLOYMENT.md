# 🚀 Vercel Deployment Guide

## ✅ Your IMDb Review Analyzer is Ready for Vercel!

This guide will walk you through deploying your FastAPI application to Vercel.

## 📋 Prerequisites

1. **Vercel Account** - [Sign up at vercel.com](https://vercel.com)
2. **Git Repository** - GitHub, GitLab, or Bitbucket account
3. **Your Code** - All files in the `web scraper` folder

## 📁 Required Files (Already Created!)

Your project now includes all necessary Vercel files:

```
web scraper/
├── app.py                    # Main FastAPI application
├── index.py                  # Vercel entry point
├── vercel.json              # Vercel configuration
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variables template
├── .gitignore              # Git ignore rules
├── templates/
│   └── index.html          # Frontend template
└── README.md
```

## 🔧 Step-by-Step Deployment

### Step 1: Push to Git Repository

1. **Initialize Git** (if not already done):
   ```bash
   cd "c:\Users\Sanjay\Downloads\web scraper"
   git init
   ```

2. **Add all files**:
   ```bash
   git add .
   ```

3. **Commit**:
   ```bash
   git commit -m "Initial commit - IMDb Review Analyzer"
   ```

4. **Create a GitHub repository**:
   - Go to [github.com](https://github.com)
   - Click "New repository"
   - Name it: `imdb-review-analyzer`
   - Don't initialize with README (we already have one)

5. **Push to GitHub**:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/imdb-review-analyzer.git
   git branch -M main
   git push -u origin main
   ```

### Step 2: Deploy to Vercel

#### Option A: Using Vercel Dashboard (Recommended)

1. **Go to Vercel**:
   - Visit [vercel.com/new](https://vercel.com/new)
   - Sign in with GitHub

2. **Import Project**:
   - Click "Import Git Repository"
   - Select your `imdb-review-analyzer` repository
   - Click "Import"

3. **Configure Project**:
   - **Framework Preset**: Other
   - **Root Directory**: `./` (leave as default)
   - **Build Command**: (leave empty)
   - **Output Directory**: (leave empty)

4. **Add Environment Variables**:
   - Click "Environment Variables"
   - Add:
     - Name: `OPENROUTER_API_KEY`
     - Value: `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`
   - Click "Add"

5. **Deploy**:
   - Click "Deploy"
   - Wait 1-2 minutes for deployment
   - Your app will be live at `https://your-project.vercel.app`

#### Option B: Using Vercel CLI

1. **Install Vercel CLI**:
   ```bash
   npm install -g vercel
   ```

2. **Login**:
   ```bash
   vercel login
   ```

3. **Deploy**:
   ```bash
   cd "c:\Users\Sanjay\Downloads\web scraper"
   vercel
   ```

4. **Follow prompts**:
   - Set up and deploy? Y
   - Which scope? (select your account)
   - Link to existing project? N
   - Project name? imdb-review-analyzer
   - Directory? ./
   - Want to override settings? N

5. **Add environment variable**:
   ```bash
   vercel env add OPENROUTER_API_KEY
   ```
   - Paste your API key
   - Select all environments (production, preview, development)

6. **Redeploy**:
   ```bash
   vercel --prod
   ```

## 🔑 Environment Variables

Set these in Vercel Dashboard → Settings → Environment Variables:

| Variable Name | Value | Environment |
|--------------|-------|-------------|
| `OPENROUTER_API_KEY` | Your OpenRouter API key | Production, Preview, Development |

## ✅ Verification

After deployment, test your app:

1. **Visit your URL**: `https://your-project.vercel.app`
2. **Test search**: Enter "Inception"
3. **Check results**: Should show search results with posters
4. **Test analysis**: Click "Analyze" and wait for AI summary
5. **Verify**: Check that rating and reviews appear

## 🎯 Vercel Configuration Details

### `vercel.json`
```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
```

**What it does**:
- `builds`: Tells Vercel to build the Python app
- `routes`: Routes all requests to app.py

### `requirements.txt`
```
fastapi
uvicorn
python-multipart
jinja2
requests
beautifulsoup4
```

**What it does**:
- Lists all Python dependencies
- Vercel installs these automatically

### `index.py`
```python
from app import app
```

**What it does**:
- Entry point for Vercel serverless functions
- Imports the FastAPI app

## 🌐 Custom Domain (Optional)

### Add Your Own Domain:

1. **Go to Vercel Dashboard**
2. **Select your project**
3. **Settings** → **Domains**
4. **Add Domain**: Enter your domain (e.g., `moviereviews.com`)
5. **Configure DNS**: Add records as shown by Vercel
6. **Wait for SSL**: Automatic HTTPS certificate

## 📊 Monitoring

### Vercel Dashboard Features:

1. **Analytics**: View traffic and performance
2. **Logs**: Real-time function logs
3. **Deployments**: History of all deployments
4. **Preview**: Test before production

### Access Logs:
```bash
vercel logs
```

## 🔄 Updating Your App

### After making changes:

**Option 1: Git Push (Automatic)**
```bash
git add .
git commit -m "Update: description of changes"
git push
```
- Vercel auto-deploys on push to main branch

**Option 2: Manual Deploy**
```bash
vercel --prod
```

## ⚡ Performance Tips

### 1. **Cold Starts**
- Serverless functions may have cold starts (1-2s delay)
- First request after idle period may be slower
- Subsequent requests are fast

### 2. **Caching**
- Vercel caches static assets automatically
- HTML template is served quickly

### 3. **Function Timeout**
- Default: 10 seconds
- AI analysis may take 15-30 seconds
- **Solution**: Upgrade to Pro plan for 60s timeout
- Or optimize by reducing reviews analyzed

### 4. **Region**
- Vercel deploys globally
- Choose edge region closest to users

## 🐛 Troubleshooting

### Issue: "Application Error"
**Solution**:
- Check Vercel logs: `vercel logs`
- Verify environment variables are set
- Check `requirements.txt` includes all dependencies

### Issue: "Module not found"
**Solution**:
- Add missing module to `requirements.txt`
- Redeploy: `vercel --prod`

### Issue: "Timeout Error"
**Solution**:
- Reduce number of reviews analyzed (line 247 in app.py)
- Or upgrade to Vercel Pro for longer timeout

### Issue: "API Key Error"
**Solution**:
- Verify `OPENROUTER_API_KEY` is set in Vercel dashboard
- Check key is valid and not expired

### Issue: Static Files Not Loading
**Solution**:
- Templates are served correctly by default
- Check `templates/` directory exists
- Verify `index.html` is in templates folder

## 🔒 Security Best Practices

1. **Never commit API keys**:
   - ✅ Use environment variables
   - ✅ Add `.env` to `.gitignore`
   - ❌ Don't hardcode in source

2. **Keep dependencies updated**:
   ```bash
   pip list --outdated
   pip install --upgrade package-name
   ```

3. **Rate limiting**:
   - Consider adding rate limits for API calls
   - Use Vercel Edge Config for tracking

## 💰 Pricing

### Vercel Free Tier:
- ✅ Unlimited deployments
- ✅ 100GB bandwidth/month
- ✅ Automatic HTTPS
- ✅ Global CDN
- ⚠️ 10s function timeout
- ⚠️ Limited analytics

### Vercel Pro ($20/month):
- ✅ 60s function timeout (better for AI)
- ✅ Advanced analytics
- ✅ Team collaboration
- ✅ Priority support

**Recommendation**: Start with Free, upgrade if needed

## 📱 Mobile Optimization

Your app is already mobile-responsive:
- ✅ Responsive CSS
- ✅ Touch-friendly buttons
- ✅ Adaptive layouts
- ✅ Fast loading

## 🎯 Next Steps

After successful deployment:

1. **Share your URL**: `https://your-project.vercel.app`
2. **Test thoroughly**: Try various movies
3. **Monitor usage**: Check Vercel dashboard
4. **Gather feedback**: Share with users
5. **Iterate**: Make improvements based on feedback

## 📚 Resources

- **Vercel Docs**: [vercel.com/docs](https://vercel.com/docs)
- **FastAPI Docs**: [fastapi.tiangolo.com](https://fastapi.tiangolo.com)
- **OpenRouter Docs**: [openrouter.ai/docs](https://openrouter.ai/docs)
- **Vercel Support**: [vercel.com/support](https://vercel.com/support)

## 🎉 Success Checklist

- [ ] Code pushed to Git repository
- [ ] Vercel account created
- [ ] Project imported to Vercel
- [ ] Environment variables set
- [ ] Deployment successful
- [ ] App tested and working
- [ ] Custom domain added (optional)
- [ ] Analytics enabled

---

## 🚀 Quick Deploy Command

```bash
# One-line deploy (after git setup)
git add . && git commit -m "Deploy to Vercel" && git push && vercel --prod
```

---

**Your IMDb Review Analyzer is now ready for the world!** 🌍🎬✨

**Live URL**: https://your-project.vercel.app
