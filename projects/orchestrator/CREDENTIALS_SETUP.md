# Credential Generation & Setup Guide

**Status:** Awaiting execution by Brad
**Last Updated:** 2026-02-23

---

## Overview

This guide covers generating all credentials needed for the orchestration system. **Do not skip the security steps (vault, gitignore, etc.).**

---

## 1. X Developer API (Twitter/Grok Sentiment)

### 10-15 Minute Setup

1. **Create X Developer Account**
   - Go to https://developer.x.com
   - Sign in with your X account (create one if needed)
   - Click "Create an app"
   - App name: `CryptoSentimentBot` (or your preference)
   - Accept terms, click "Create"

2. **Choose Pricing Tier**
   - **Recommended:** Basic tier ($200/month)
   - Covers 10,000 posts/month (sufficient for ~10 coins, 30-50 posts each daily)
   - Alternative: Free tier (100 posts/month) for testing only
   - Billing: Credit card required, charged monthly

3. **Generate API Credentials**
   - Go to your app's "Keys and tokens" tab
   - Under "API Keys":
     - **API Key** → `X_CONSUMER_KEY`
     - **API Secret Key** → `X_CONSUMER_SECRET`
   - Under "Authentication Tokens":
     - **Access Token** → `X_ACCESS_TOKEN`
     - **Access Token Secret** → `X_ACCESS_TOKEN_SECRET`
   - Click "Regenerate" if needed (this invalidates old keys)

4. **Enable OAuth 1.0a (Required for Search)**
   - Go to "App Settings" → "User authentication settings"
   - Toggle **OAuth 1.0a** to ON
   - Set Callback URI: `http://localhost:8000` (for development)
   - Check: "Request email address" (optional)
   - Save

5. **Copy & Secure**
   - Save all 4 credentials to a secure location (password manager, not email)
   - **Do not paste into code or Slack**
   - These go into your encrypted vault (see Step 6 below)

### Estimated Cost
- **Basic Tier:** $200/month ($2,400/year)
- **Sentiment API calls:** 1-2 seconds per coin (negligible cost impact)

---

## 2. Google Ads API

### 30-45 Minute Setup

1. **Create Google Cloud Project**
   - Go to https://console.cloud.google.com
   - Create new project: `CryptoAdsOrchestrator`
   - Enable billing (required for API access)

2. **Enable Google Ads API**
   - In Cloud Console, go to "APIs & Services" → "Library"
   - Search for "Google Ads API"
   - Click "Enable"
   - Wait 2-3 minutes for activation

3. **Create Service Account** (Recommended over OAuth for automated access)
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "Service Account"
   - Service account name: `crypto-ads-orchestrator`
   - Grant role: `Editor` (or more restrictive if you prefer)
   - Create & download JSON key file
   - Save as `google-ads-service-account.json` → **VAULT ONLY**

4. **Link Google Ads Account**
   - Go to https://ads.google.com (your main ads account)
   - Settings → Linked accounts
   - Add the service account email: `crypto-ads-orchestrator@PROJECT_ID.iam.gserviceaccount.com`
   - Approve the link

5. **Generate Google Ads API Credentials**
   - Use service account JSON (contains all needed credentials)
   - Extract: `project_id`, `private_key`, `client_email`
   - Store in vault under `google-ads-credentials`

### Estimated Cost
- **Free:** Service account access to Google Ads API (no API fees)
- **Ads spend:** You'll pay for ad impressions as usual, not for API access

---

## 3. Coinbase Pro API

### 15-20 Minute Setup

1. **Create Coinbase Pro Account** (if not already done)
   - Go to https://www.coinbase.com/join
   - Sign up, verify email & ID
   - Enable 2FA (highly recommended)

2. **Generate API Key**
   - Log into Coinbase Pro
   - Go to Settings → API
   - Click "New API Key"
   - Permissions:
     - **Trading:** ✅ (buy/sell)
     - **Withdrawals:** ❌ (disable for safety)
     - **Viewing:** ✅ (read balances)
   - **Passphrase:** Create a strong passphrase (you'll need this to authenticate)
   - Generate key

3. **Save Credentials**
   - **API Key** → `COINBASE_API_KEY`
   - **API Secret** → `COINBASE_API_SECRET`
   - **Passphrase** → `COINBASE_PASSPHRASE`
   - Save to secure location immediately (Coinbase shows secret only once)

4. **Set IP Whitelist** (Recommended)
   - Go to API settings
   - Add IP(s) where bot will run (AWS EC2 IP, VPS IP, etc.)
   - Only those IPs can authenticate

5. **Test Connection** (Before going live)
   - Use sandbox: https://sandbox.coinbase.com
   - Generate separate sandbox API keys
   - Test all trading logic there first

---

## 4. Secure Credential Storage

### Choose Your Vault Strategy

**Option A: AWS Secrets Manager (Recommended for Production)**
```bash
# Install AWS CLI
pip install boto3

# Create secret
aws secretsmanager create-secret \
  --name crypto-orchestrator-x-api \
  --secret-string '{"consumer_key":"...","consumer_secret":"...","access_token":"...","access_token_secret":"..."}'

# Retrieve secret in Python
import boto3
client = boto3.client('secretsmanager', region_name='us-west-2')
secret = client.get_secret_value(SecretId='crypto-orchestrator-x-api')
credentials = json.loads(secret['SecretString'])
```

**Option B: HashiCorp Vault (Self-hosted)**
```bash
# Install Vault CLI
brew install vault  # or apt-get on Linux

# Start Vault dev server
vault server -dev

# Store secret
vault kv put secret/crypto-orchestrator-x-api \
  consumer_key="..." \
  consumer_secret="..."

# Retrieve in Python
import hvac
client = hvac.Client(url='http://localhost:8200')
secret = client.secrets.kv.read_secret_version(path='crypto-orchestrator-x-api')
```

**Option C: .env File (Development Only)**
```bash
# Create .env (NEVER commit to git)
echo "X_CONSUMER_KEY=..." >> .env
echo "X_CONSUMER_SECRET=..." >> .env
echo "COINBASE_API_KEY=..." >> .env
# ... etc

# .gitignore (add this)
*.env
.env.local
credentials/
secrets/

# Load in Python
from dotenv import load_dotenv
load_dotenv()
import os
consumer_key = os.getenv('X_CONSUMER_KEY')
```

### Recommended: Multi-Layer Approach
1. **Production (AWS/VPS):** AWS Secrets Manager or Vault
2. **Development (Local):** .env file + strict gitignore
3. **Backup:** Password manager (1Password, Bitwarden) for manual access if needed

---

## 5. Credential Rotation & Updates

### Quarterly Rotation (Recommended)
1. Generate new credentials in respective services
2. Update vault with new values
3. Invalidate old credentials
4. Test agents with new credentials in sandbox
5. Deploy to production
6. Document in `CREDENTIALS_AUDIT.md`

### Incident Response
- **Exposed/Compromised Credential:**
  - Immediately regenerate in source service
  - Update vault
  - Restart all agents
  - Review audit logs for unauthorized access
  - File incident report

---

## 6. Vault Implementation Checklist

- [ ] Choose vault strategy (AWS Secrets Manager / Vault / .env)
- [ ] Install & configure chosen vault
- [ ] Create secret store for each service:
  - [ ] `crypto-orchestrator-x-api`
  - [ ] `crypto-orchestrator-google-ads`
  - [ ] `crypto-orchestrator-coinbase-pro`
- [ ] Update `.gitignore` with `.env`, `credentials/`, `secrets/`
- [ ] Create helper function to fetch credentials from vault
- [ ] Test credential retrieval in all agents
- [ ] Document vault access procedures
- [ ] Set up audit logging for credential access

---

## 7. Testing Credentials

Before deploying, test each credential set:

### X API Test
```python
import tweepy

auth = tweepy.OAuth1UserHandler(
    consumer_key=os.getenv('X_CONSUMER_KEY'),
    consumer_secret=os.getenv('X_CONSUMER_SECRET'),
    access_token=os.getenv('X_ACCESS_TOKEN'),
    access_token_secret=os.getenv('X_ACCESS_TOKEN_SECRET')
)
api = tweepy.API(auth)
tweets = api.search_tweets(q="bitcoin", lang="en", count=5)
print(f"✓ X API working: {len(tweets)} tweets fetched")
```

### Google Ads API Test
```python
from google.ads.googleads.client import GoogleAdsClient

client = GoogleAdsClient.load_from_storage(
    './google-ads-service-account.json'
)
print("✓ Google Ads API credentials valid")
```

### Coinbase Pro API Test
```python
from coinbase.wallet.client import Client

client = Client(api_key=os.getenv('COINBASE_API_KEY'),
                api_secret=os.getenv('COINBASE_API_SECRET'),
                api_version=os.getenv('COINBASE_PASSPHRASE'))
account = client.get_accounts()
print(f"✓ Coinbase Pro API working: {len(account)} accounts found")
```

---

## Next Steps

1. **Execute this guide** (10-15 min per service)
2. **Set up vault** (30 min)
3. **Add credentials** to vault (15 min)
4. **Test each service** (30 min)
5. **Update SECURITY_REVIEW.md** with ✓ marks
6. **Notify Brad** when complete

---

**Status:** Ready for execution
**Estimated Total Time:** 2-3 hours (all services + vault setup)
