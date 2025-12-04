# Deployment Guide

## Railway (Recommended for Production)

### Prerequisites
- Railway account (https://railway.app)
- Node.js installed

### Steps

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Set environment variables
railway variables set NOTION_API_TOKEN="your_token"
railway variables set COMPTEXT_DATABASE_ID="0e038c9b52c5466694dbac288280dd93"
railway variables set LOG_LEVEL="INFO"

# Deploy
railway up

# Get public domain
railway domain
```

Your API will be available at: `https://comptext-api-production.up.railway.app`

## Docker

### Build and Run

```bash
# Build image
docker build -f Dockerfile.rest -t comptext-api .

# Run container
docker run -p 8000:8000 \
  -e NOTION_API_TOKEN="your_token" \
  -e COMPTEXT_DATABASE_ID="0e038c9b52c5466694dbac288280dd93" \
  comptext-api
```

### Docker Compose

```bash
# Create .env file
echo "NOTION_API_TOKEN=your_token" > .env

# Start
docker-compose up -d

# Stop
docker-compose down
```

## ngrok (Temporary Public URL)

### Installation

```bash
# macOS
brew install ngrok

# Windows: Download from https://ngrok.com/download
```

### Usage

```bash
# Terminal 1: Start API
python rest_api_wrapper.py

# Terminal 2: Create tunnel
ngrok http 8000

# Use the generated URL (e.g., https://abc123.ngrok-free.app)
```

**Note:** Free tier URLs change on each restart.

## Vercel (Serverless)

### Prerequisites
- Vercel account
- Vercel CLI

### Steps

```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy
vercel

# Set environment variables
vercel env add NOTION_API_TOKEN
vercel env add COMPTEXT_DATABASE_ID

# Production deploy
vercel --prod
```

## Render

### Via Dashboard

1. Go to https://render.com
2. New → Web Service
3. Connect GitHub repository
4. Configure:
   - **Build Command:** `pip install -r requirements-rest.txt`
   - **Start Command:** `uvicorn rest_api_wrapper:app --host 0.0.0.0 --port $PORT`
5. Add environment variables:
   - `NOTION_API_TOKEN`
   - `COMPTEXT_DATABASE_ID`
6. Deploy

## Environment Variables

Required for all deployments:

```bash
NOTION_API_TOKEN=your_token_here
COMPTEXT_DATABASE_ID=0e038c9b52c5466694dbac288280dd93
LOG_LEVEL=INFO  # optional
HOST=0.0.0.0    # for REST API
PORT=8000       # for REST API
```

## Monitoring

### Health Check

```bash
curl https://your-api-url.com/health
```

### Logs

- **Railway:** `railway logs`
- **Docker:** `docker logs comptext-api`
- **Local:** Check console output

## Troubleshooting

### Build fails

- Check Python version (3.10+ required)
- Verify requirements.txt is complete
- Check environment variables

### Connection errors

- Verify NOTION_API_TOKEN is valid
- Check database ID is correct
- Test locally first

### Performance issues

- Enable caching (already implemented)
- Consider scaling Railway instance
- Monitor API usage
