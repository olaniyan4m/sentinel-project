#!/bin/bash
# Sentinel Enhanced Threat Intelligence Deployment Script
# Integrates: edge-ml, ncnn, ThreatMapper, GeoIP Attack Map, Raven OSINT, OSINT Toolkit

set -e

echo "🚀 Deploying Sentinel Enhanced Threat Intelligence System..."

# Create deployment directory
mkdir -p sentinel_threat_intelligence
cd sentinel_threat_intelligence

# Clone required repositories
echo "📥 Cloning open-source tools..."

# Edge ML for model training and deployment
git clone https://github.com/edge-ml/edge-ml.git
cd edge-ml
docker-compose build
docker-compose up -d
cd ..

# NCNN for optimized inference
git clone https://github.com/Bisonai/ncnn.git
cd ncnn
mkdir build && cd build
cmake ..
make -j$(nproc)
cd ../..

# ThreatMapper for threat visualization
git clone https://github.com/deepfence/ThreatMapper.git
cd ThreatMapper
docker-compose up -d
cd ..

# GeoIP Attack Map
git clone https://github.com/MatthewClarkMay/geoip-attack-map.git
cd geoip-attack-map
npm install
npm run build
cd ..

# Raven OSINT
git clone https://github.com/qeeqbox/raven.git
cd raven
pip install -r requirements.txt
cd ..

# OSINT Toolkit
git clone https://github.com/dev-lu/osint_toolkit.git
cd osint_toolkit
pip install -r requirements.txt
cd ..

echo "✅ All tools cloned and configured successfully!"

# Set up environment variables
echo "🔧 Setting up environment variables..."
cat > .env << EOF
# Threat Intelligence API Keys
ABUSEIPDB_KEY=your_abuseipdb_key_here
SHODAN_KEY=your_shodan_key_here
VIRUSTOTAL_KEY=your_virustotal_key_here

# Edge ML Configuration
EDGE_ML_API_URL=http://localhost:8000
EDGE_ML_MODEL_PATH=/models

# NCNN Configuration
NCNN_MODEL_PATH=/models/ncnn
NCNN_OPTIMIZATION_LEVEL=high

# ThreatMapper Configuration
THREATMAPPER_API_URL=http://localhost:8080
THREATMAPPER_DB_URL=postgresql://user:pass@localhost:5432/threatmapper

# GeoIP Attack Map Configuration
GEOIP_MAP_CENTER_LAT=-30.0
GEOIP_MAP_CENTER_LON=25.0
GEOIP_MAP_ZOOM=6

# Raven OSINT Configuration
RAVEN_OSINT_SCHEDULE=*/15 * * * *
RAVEN_OSINT_OUTPUT_DIR=/data/osint

# OSINT Toolkit Configuration
OSINT_TOOLKIT_OUTPUT_DIR=/data/osint
OSINT_TOOLKIT_AUTO_ANALYSIS=true
EOF

echo "📋 Environment variables configured!"
echo "⚠️  Please update the API keys in .env file before running the system"

# Create Docker Compose for integrated deployment
cat > docker-compose-integrated.yml << EOF
version: '3.8'

services:
  sentinel-threat-intelligence:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
    volumes:
      - ./data:/app/data
      - ./models:/app/models
    depends_on:
      - edge-ml
      - threatmapper
      - geoip-map

  edge-ml:
    build: ./edge-ml
    ports:
      - "8000:8000"
    volumes:
      - ./models:/models
    environment:
      - EDGE_ML_MODEL_PATH=/models

  threatmapper:
    build: ./ThreatMapper
    ports:
      - "8080:8080"
    environment:
      - THREATMAPPER_DB_URL=postgresql://user:pass@postgres:5432/threatmapper
    depends_on:
      - postgres

  geoip-map:
    build: ./geoip-attack-map
    ports:
      - "3001:3001"
    environment:
      - GEOIP_MAP_CENTER_LAT=-30.0
      - GEOIP_MAP_CENTER_LON=25.0

  postgres:
    image: postgres:13
    environment:
      - POSTGRES_DB=threatmapper
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data

  raven-osint:
    build: ./raven
    volumes:
      - ./data/osint:/data/osint
    environment:
      - RAVEN_OSINT_OUTPUT_DIR=/data/osint

  osint-toolkit:
    build: ./osint_toolkit
    volumes:
      - ./data/osint:/data/osint
    environment:
      - OSINT_TOOLKIT_OUTPUT_DIR=/data/osint

volumes:
  postgres_data:
EOF

echo "🐳 Docker Compose configuration created!"

# Create startup script
cat > start-sentinel-threat-intelligence.sh << EOF
#!/bin/bash
echo "🚀 Starting Sentinel Enhanced Threat Intelligence System..."

# Start all services
docker-compose -f docker-compose-integrated.yml up -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 30

# Check service health
echo "🔍 Checking service health..."
curl -f http://localhost:3000/health || echo "❌ Sentinel service not ready"
curl -f http://localhost:8000/health || echo "❌ Edge ML service not ready"
curl -f http://localhost:8080/health || echo "❌ ThreatMapper service not ready"
curl -f http://localhost:3001/health || echo "❌ GeoIP Map service not ready"

echo "✅ Sentinel Enhanced Threat Intelligence System is running!"
echo "🌐 Access the dashboard at: http://localhost:3000"
echo "🗺️  Access the threat map at: http://localhost:3001"
echo "📊 Access ThreatMapper at: http://localhost:8080"
echo "🤖 Access Edge ML at: http://localhost:8000"
EOF

chmod +x start-sentinel-threat-intelligence.sh

echo "🎉 Deployment script generated successfully!"
echo "📝 Next steps:"
echo "1. Update API keys in .env file"
echo "2. Run: ./start-sentinel-threat-intelligence.sh"
echo "3. Access the integrated dashboard at http://localhost:3000"
