# Deployment Guide for AMP Classifier Frontend

This guide will help you deploy your frontend to a hosting platform.

## Backend API Configuration

Your frontend is configured to use the backend API at: `https://amp-classifier.onrender.com`

The API URL is set via environment variable `VITE_API_URL`. If not set, it defaults to the Render URL.

## Deployment Options

### Option 1: Vercel (Recommended - Easiest)

1. **Install Vercel CLI** (if not already installed):
   ```bash
   npm install -g vercel
   ```

2. **Deploy from frontend directory**:
   ```bash
   cd frontend
   vercel
   ```

3. **Follow the prompts**:
   - Link to existing project or create new
   - Set environment variable: `VITE_API_URL=https://amp-classifier.onrender.com`

4. **Or deploy via GitHub**:
   - Push your code to GitHub
   - Go to [vercel.com](https://vercel.com)
   - Import your repository
   - Set environment variable: `VITE_API_URL=https://amp-classifier.onrender.com`
   - Deploy!

### Option 2: Netlify

1. **Install Netlify CLI**:
   ```bash
   npm install -g netlify-cli
   ```

2. **Build the project**:
   ```bash
   cd frontend
   npm run build
   ```

3. **Deploy**:
   ```bash
   netlify deploy --prod
   ```

4. **Set environment variable** in Netlify dashboard:
   - Go to Site settings > Environment variables
   - Add: `VITE_API_URL` = `https://amp-classifier.onrender.com`

5. **Or deploy via GitHub**:
   - Push to GitHub
   - Go to [netlify.com](https://netlify.com)
   - Add new site from Git
   - Set build command: `npm run build`
   - Set publish directory: `dist`
   - Add environment variable: `VITE_API_URL=https://amp-classifier.onrender.com`

### Option 3: GitHub Pages

1. **Install gh-pages**:
   ```bash
   cd frontend
   npm install --save-dev gh-pages
   ```

2. **Update package.json** scripts:
   ```json
   "scripts": {
     "predeploy": "npm run build",
     "deploy": "gh-pages -d dist"
   }
   ```

3. **Deploy**:
   ```bash
   npm run deploy
   ```

4. **Set environment variable** via GitHub Actions or use a build-time replacement script.

### Option 4: Render (Same as Backend)

1. **Create a new Static Site** on Render
2. **Connect your GitHub repository**
3. **Set build command**: `npm run build`
4. **Set publish directory**: `dist`
5. **Add environment variable**: `VITE_API_URL=https://amp-classifier.onrender.com`

## Testing Locally

Before deploying, test locally:

1. **Create a `.env.local` file** in the frontend directory:
   ```
   VITE_API_URL=https://amp-classifier.onrender.com
   ```

2. **Run the dev server**:
   ```bash
   cd frontend
   npm run dev
   ```

3. **Test the API connection** by submitting a protein sequence

## Environment Variables

- **Production**: Set `VITE_API_URL=https://amp-classifier.onrender.com` in your hosting platform's environment variables
- **Local Development**: Create `.env.local` with the same variable (this file is gitignored)

## Important Notes

- Make sure your backend CORS settings allow requests from your frontend domain
- The backend at `https://amp-classifier.onrender.com` should already have CORS configured for `*` origins
- If you need to restrict CORS, update the backend's `ALLOW_ORIGINS` environment variable

## Quick Start (Vercel - Fastest)

```bash
cd frontend
npm install -g vercel
vercel
# Follow prompts, set VITE_API_URL=https://amp-classifier.onrender.com when asked
```

Your frontend will be live in minutes!

