# 🌐 Domain Setup: vigilo.mozdev.co.za

## 🎯 **Your Sentinel Project Domain**

**Primary URL**: `https://vigilo.mozdev.co.za`

## 📋 **Setup Instructions**

### **Step 1: Render Configuration**
1. Go to your Render service settings
2. Add custom domain: `vigilo.mozdev.co.za`
3. Render will provide DNS instructions

### **Step 2: DNS Configuration**
Add these DNS records to your domain provider:

**CNAME Record (Recommended):**
```
Type: CNAME
Name: vigilo
Value: [Render will provide - e.g., sentinel-fight-crime.onrender.com]
TTL: 300
```

**Alternative A Record:**
```
Type: A
Name: vigilo
Value: [Render will provide IP address]
TTL: 300
```

### **Step 3: SSL Certificate**
- Render automatically provisions SSL
- Your site will be accessible via HTTPS
- Certificate will be valid for `vigilo.mozdev.co.za`

## 🚀 **Access Points**

### **Main Application**
- **URL**: `https://vigilo.mozdev.co.za`
- **Description**: Sentinel Crime Detection & Threat Intelligence Platform

### **Role-Based Access**
- **Police Officers**: Full access including Threat Map
- **Private Security**: Security operations dashboard
- **Bank Representatives**: Financial crime prevention + Threat Map
- **Insurance**: Risk assessment and claims analysis

## 🔧 **Troubleshooting**

### **If Domain Not Working:**
1. Check DNS propagation (can take 24-48 hours)
2. Verify DNS records are correct
3. Check Render service logs
4. Ensure SSL certificate is provisioned

### **Fallback URLs:**
- **Render Default**: `https://sentinel-fight-crime.onrender.com`
- **Local Development**: `http://localhost:8501`

## 📱 **Mobile Access**
The application is fully responsive and works on:
- Desktop computers
- Tablets
- Mobile phones
- All modern browsers

## 🔒 **Security Features**
- HTTPS encryption
- Role-based access control
- Secure Firebase integration
- Privacy-first data processing
