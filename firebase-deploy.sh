#!/bin/bash

echo "🔥 Firebase Deployment Script for Sentinel"
echo "=========================================="

# Check if Firebase CLI is installed
if ! command -v firebase &> /dev/null; then
    echo "❌ Firebase CLI not found. Installing..."
    npm install -g firebase-tools
fi

# Check if user is logged in
if ! firebase projects:list &> /dev/null; then
    echo "🔐 Please login to Firebase..."
    firebase login
fi

echo "📁 Preparing files for deployment..."

# Ensure public directory exists
mkdir -p public

echo "🚀 Deploying to Firebase Hosting..."
firebase deploy --only hosting

echo "✅ Deployment complete!"
echo "🌐 Your app is available at: https://vigilo-fight-crime.web.app/"
echo "🔗 Custom domain: https://vigilo.mozdev.co.za (if configured)"
