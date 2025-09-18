# 🔥 Firebase Deployment Guide

## 🎯 **Deploy Sentinel to Firebase Hosting**

### **Your Firebase URLs:**
- **Main App**: `https://vigilo-fight-crime.web.app/`
- **Custom Domain**: `https://vigilo.mozdev.co.za` (if configured)

## 📋 **Deployment Steps:**

### **Step 1: Install Firebase CLI**
```bash
npm install -g firebase-tools
```

### **Step 2: Login to Firebase**
```bash
firebase login
```

### **Step 3: Initialize Firebase Project**
```bash
firebase init hosting
```
- Select existing project: `vigilo-fight-crime`
- Public directory: `public`
- Single-page app: `Yes`
- Overwrite index.html: `No`

### **Step 4: Deploy to Firebase**
```bash
firebase deploy
```

## 🌐 **Firebase Hosting Features:**
- ✅ **Global CDN** - Fast loading worldwide
- ✅ **SSL Certificate** - Automatic HTTPS
- ✅ **Custom Domain** - Support for vigilo.mozdev.co.za
- ✅ **Version History** - Easy rollbacks
- ✅ **Analytics** - Built-in performance monitoring

## 🔧 **Configuration Files:**

### **firebase.json** (already created)
```json
{
  "hosting": {
    "public": "public",
    "rewrites": [
      {
        "source": "**",
        "destination": "/index.html"
      }
    ]
  }
}
```

### **public/index.html** (already created)
- Landing page with app access
- Professional design
- Links to main application

## 🚀 **Quick Deploy Command:**
```bash
firebase deploy --only hosting
```

## 📱 **Access Your Platform:**
1. **Landing Page**: `https://vigilo-fight-crime.web.app/`
2. **Main App**: Links to the Streamlit application
3. **Mobile Friendly**: Responsive design

## 🔒 **Security Features:**
- HTTPS by default
- Firebase Authentication ready
- Secure hosting infrastructure
- Global edge locations

## 📊 **Analytics & Monitoring:**
- Firebase Analytics integration
- Performance monitoring
- Error tracking
- Usage statistics
