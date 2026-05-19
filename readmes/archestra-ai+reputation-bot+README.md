# GitHub Reputation Bot

Bot that posts reputation comments on PRs and issues for archestra-ai/archestra. Automatically closes pull requests from users with very low reputation scores to maintain code quality.

## Features

- **Reputation Tracking**: Calculates and displays user reputation on PRs and issues
- **Automatic PR Closing**: Closes PRs from users with reputation below the configured threshold
- **Clickable Statistics**: All counts (PRs, issues, assigned) link to filtered GitHub searches
- **Smart Updates**: Skips updating comments when no new participants have joined

## Reputation Scoring

The bot calculates reputation scores based on GitHub activity. **Note: Scores can be negative.**

### Points System
- **Merged PRs**: +20 points
- **Open PRs**: +3 points  
- **Closed PRs**: -10 points (PRs closed without merging)
- **Issues created**: +5 points
- **Comments**: Displayed for context but don't affect score
- **Core team 👍**: +15 points (reactions on issues/PRs authored by the user)
- **Core team 👎**: -50 points (reactions on issues/PRs authored by the user)

### Automatic PR Closing
Pull requests from users with reputation below the threshold (default: -80) are automatically closed with an explanatory comment. This helps maintain code quality by preventing spam from users with poor contribution history.

### Core Team Reactions
Core team members' reactions carry significant weight. The bot tracks thumbs up (👍) and thumbs down (👎) reactions from designated core team members on issues and pull requests created by users. These reactions are only counted on the main issue/PR body, not on comments within them.

## Deployment to Google Cloud Run

### 1. Prerequisites

Install Google Cloud CLI and authenticate:
```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# Enable required services
gcloud services enable cloudbuild.googleapis.com container.googleapis.com run.googleapis.com

# Configure Docker authentication for GCR
gcloud auth configure-docker
```

### 2. Build and Deploy

```bash
# Build container for linux/amd64 platform (required for Cloud Run)
docker build --platform linux/amd64 -t gcr.io/YOUR_PROJECT_ID/reputation-bot .

# Push to Google Container Registry
docker push gcr.io/YOUR_PROJECT_ID/reputation-bot

# Deploy to Cloud Run
# Note: Use ^@^ syntax to handle commas in CORE_TEAM_MEMBERS
gcloud run deploy reputation-bot \
  --image gcr.io/YOUR_PROJECT_ID/reputation-bot \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars="^@^GITHUB_TOKEN=YOUR_GITHUB_TOKEN@GITHUB_WEBHOOK_SECRET=YOUR_WEBHOOK_SECRET@CORE_TEAM_MEMBERS=ashlkv,iskhakov,Konstantinov-Innokentii,joeyorlando,brojd,Matvey-Kuk@REPUTATION_THRESHOLD=-80" \
  --memory 512Mi \
  --max-instances 1
```

Note the URL returned (e.g., `https://reputation-bot-xxx.run.app`)

### 3. Configure GitHub Webhook

**Important**: You need admin access to the repository. If you don't have admin access, ask a repository administrator.

1. Go to `https://github.com/archestra-ai/archestra/settings/hooks` (requires admin access)
2. Click "Add webhook"
3. Configure:
   - **Payload URL**: `https://YOUR_CLOUD_RUN_URL/webhook`
   - **Content type**: `application/json`
   - **Secret**: Same value as `GITHUB_WEBHOOK_SECRET` env variable
   - **Events**: Select individual events:
     - Pull requests
     - Issues
     - Issue comments
4. Click "Add webhook"

### 4. Update Environment Variables

To update configuration after deployment:
```bash
gcloud run services update reputation-bot \
  --region us-central1 \
  --update-env-vars GITHUB_WEBHOOK_SECRET=your-new-secret
```

## Environment Variables

- `GITHUB_TOKEN`: GitHub personal access token with repo scope (needs write permissions for closing PRs)
- `GITHUB_WEBHOOK_SECRET`: Secret for webhook signature verification
- `CORE_TEAM_MEMBERS`: Comma-separated list of core team GitHub usernames (ashlkv,iskhakov,Konstantinov-Innokentii,joeyorlando,brojd,Matvey-Kuk)
- `REPUTATION_THRESHOLD`: Minimum reputation score to keep PRs open (default: -80)
- `PORT`: Automatically set by Cloud Run

## Local Testing

### Build and run with Docker

```bash
# 1. Build the Docker image
docker build -t reputation-bot .

# 2. Run the container with test environment variables
docker run -p 8080:8080 \
  -e GITHUB_TOKEN="your_github_personal_access_token" \
  -e GITHUB_WEBHOOK_SECRET="test-secret-123" \
  -e CORE_TEAM_MEMBERS="ashlkv,iskhakov,Konstantinov-Innokentii,joeyorlando,brojd,Matvey-Kuk" \
  -e PORT=8080 \
  reputation-bot

# 3. In another terminal, test the webhook
python3 test_webhook.py
```

The `test_webhook.py` script simulates GitHub webhook events for issue #1849 and test PRs.