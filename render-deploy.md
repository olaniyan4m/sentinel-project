# 🚀 Deploy to Render (Easiest Option)

## Quick Steps:

1. **Go to**: https://render.com
2. **Sign up** with your GitHub account
3. **Click "New +"** → **"Web Service"**
4. **Connect Repository**: `olaniyan4m/sentinel-project`
5. **Configure**:
   - **Name**: `sentinel-fight-crime`
   - **Environment**: `Docker`
   - **Region**: `Oregon (US West)`
   - **Branch**: `main`
   - **Dockerfile Path**: `Dockerfile`
   - **Port**: `8501`

6. **Environment Variables** (Add these):
   ```
   FIREBASE_PROJECT_ID=vigilo-fight-crime
   FIREBASE_PRIVATE_KEY_ID=your_key_id_here
   FIREBASE_PRIVATE_KEY=your_private_key_here
   FIREBASE_CLIENT_EMAIL=your_client_email_here
   ```

7. **Click "Create Web Service"**
8. **Wait 5-10 minutes** for deployment
9. **Get your public URL**: `https://sentinel-fight-crime.onrender.com`

## ✅ Benefits:
- **Free tier**: 750 hours/month
- **Automatic deployments** from GitHub
- **No CLI needed**
- **5-minute setup**

## 🔗 Your Repository:
https://github.com/olaniyan4m/sentinel-project
