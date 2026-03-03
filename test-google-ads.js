#!/usr/bin/env node

const fs = require("fs");
const path = require("path");
const { GoogleAdsApi } = require("google-ads-api");

const serviceAccountPath = path.join(__dirname, "service-account.json");

if (!fs.existsSync(serviceAccountPath)) {
  console.error("❌ service-account.json not found");
  process.exit(1);
}

const serviceAccount = JSON.parse(fs.readFileSync(serviceAccountPath, "utf-8"));

async function test() {
  try {
    const client = new GoogleAdsApi({
      client_id: serviceAccount.client_id,
      client_secret: serviceAccount.private_key_id,
      developer_token: process.env.GOOGLE_ADS_DEVELOPER_TOKEN || "placeholder",
    });

    console.log("📊 Testing Google Ads API connection...\n");

    // Try to authenticate and fetch data
    const result = await client.customer.listAccessibleCustomers({
      auth: {
        type: "service_account",
        keyFile: serviceAccountPath,
      },
    });

    console.log("✓ Authentication successful!");
    console.log(`✓ Accessible customers:\n`);
    result.resource_names.forEach((name) => {
      console.log(`  - ${name}`);
    });

    console.log("\n✅ Google Ads API is working!");
  } catch (error) {
    console.error("❌ Error:", error.message);
    console.log("\nℹ️  Check:");
    console.log("  1. Service account invited to Google Ads with Standard Access");
    console.log("  2. GOOGLE_ADS_DEVELOPER_TOKEN env var set");
    console.log("  3. Google Ads API enabled in GCP project");
    process.exit(1);
  }
}

test();
