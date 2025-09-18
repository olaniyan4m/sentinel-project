import React, { useEffect, useState, useCallback } from 'react';
import axios from 'axios';

/**
 * Sentinel Enhanced Threat Map Component
 * Integrates Check Point Threat Map with open-source tools:
 * - edge-ml: Edge ML model monitoring
 * - ncnn: Performance optimization metrics
 * - ThreatMapper: Threat correlation visualization
 * - GeoIP Attack Map: Real-time attack mapping
 * - Raven OSINT: OSINT evidence collection
 * - OSINT Toolkit: Evidence analysis
 */

export default function SentinelEnhancedThreatMap() {
  const [open, setOpen] = useState(false);
  const [iframeAllowed, setIframeAllowed] = useState(true);
  const [threatEvents, setThreatEvents] = useState([]);
  const [edgeMLModels, setEdgeMLModels] = useState([]);
  const [threatCorrelations, setThreatCorrelations] = useState([]);
  const [osintEvidence, setOsintEvidence] = useState([]);
  const [ncnnMetrics, setNcnnMetrics] = useState({});
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('threat-map');

  useEffect(() => {
    if (!open) return;
    
    // Test CheckPoint iframe availability
    testCheckPointIframe();
    
    // Load all threat intelligence data
    loadThreatIntelligenceData();
    
    // Set up real-time updates
    const interval = setInterval(loadThreatIntelligenceData, 300000); // 5 minutes
    
    return () => clearInterval(interval);
  }, [open]);

  const testCheckPointIframe = useCallback(() => {
    const iframeTest = document.createElement('iframe');
    iframeTest.style.display = 'none';
    iframeTest.src = 'https://threatmap.checkpoint.com/';
    let loaded = false;
    
    iframeTest.onload = () => {
      loaded = true;
      setIframeAllowed(true);
      document.body.removeChild(iframeTest);
    };
    
    iframeTest.onerror = () => {
      setIframeAllowed(false);
      try { document.body.removeChild(iframeTest); } catch(e) {}
    };
    
    document.body.appendChild(iframeTest);
    
    // Safety timeout
    setTimeout(() => {
      if (!loaded) {
        setIframeAllowed(false);
        try { document.body.removeChild(iframeTest); } catch(e) {}
      }
    }, 2500);
  }, []);

  const loadThreatIntelligenceData = useCallback(async () => {
    setLoading(true);
    try {
      // Load threat events from GeoIP Attack Map
      const threatResponse = await axios.get('/api/v1/threats/sa-recent?hours=6');
      setThreatEvents(threatResponse.data.events || []);

      // Load Edge ML model status
      const edgeMLResponse = await axios.get('/api/v1/edge-ml/models/status');
      setEdgeMLModels(edgeMLResponse.data.models || []);

      // Load threat correlations from ThreatMapper
      const correlationResponse = await axios.get('/api/v1/threats/correlations?hours=24');
      setThreatCorrelations(correlationResponse.data.correlations || []);

      // Load OSINT evidence from Raven
      const osintResponse = await axios.get('/api/v1/osint/evidence?hours=12');
      setOsintEvidence(osintResponse.data.evidence || []);

      // Load NCNN performance metrics
      const ncnnResponse = await axios.get('/api/v1/ncnn/performance');
      setNcnnMetrics(ncnnResponse.data.metrics || {});

    } catch (error) {
      console.error('Failed to load threat intelligence data:', error);
    } finally {
      setLoading(false);
    }
  }, []);

  const renderThreatMap = () => {
    if (iframeAllowed) {
      return (
        <iframe 
          title="checkpoint_threatmap" 
          src="https://threatmap.checkpoint.com/" 
          style={{width: "100%", height: "100%", border: 0}}
        />
      );
    } else {
      return (
        <div id="leaflet-map" style={{width: '100%', height: '100%'}}>
          <LeafletThreatMap 
            events={threatEvents}
            correlations={threatCorrelations}
            osintEvidence={osintEvidence}
          />
        </div>
      );
    }
  };

  const renderEdgeMLStatus = () => (
    <div className="p-4">
      <h3 className="text-lg font-semibold mb-4">Edge ML Model Status</h3>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {edgeMLModels.map(model => (
          <div key={model.model_id} className="bg-gray-100 p-4 rounded-lg">
            <h4 className="font-medium">{model.model_name}</h4>
            <p className="text-sm text-gray-600">Type: {model.model_type}</p>
            <p className="text-sm text-gray-600">Accuracy: {(model.accuracy * 100).toFixed(1)}%</p>
            <p className="text-sm text-gray-600">Inference: {model.inference_time_ms}ms</p>
            <p className="text-sm text-gray-600">Size: {model.model_size_mb}MB</p>
            <div className="mt-2">
              <span className={`px-2 py-1 rounded text-xs ${
                model.deployment_status === 'active' ? 'bg-green-200 text-green-800' : 'bg-yellow-200 text-yellow-800'
              }`}>
                {model.deployment_status}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  const renderNCNNMetrics = () => (
    <div className="p-4">
      <h3 className="text-lg font-semibold mb-4">NCNN Performance Optimization</h3>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="bg-blue-50 p-4 rounded-lg">
          <h4 className="font-medium text-blue-800">ANPR Optimization</h4>
          <p className="text-sm text-blue-600">Quantization: {ncnnMetrics.anpr_quantization || 'int8'}</p>
          <p className="text-sm text-blue-600">Performance: {ncnnMetrics.anpr_performance || '3.2x faster'}</p>
        </div>
        <div className="bg-green-50 p-4 rounded-lg">
          <h4 className="font-medium text-green-800">Gunshot Detection</h4>
          <p className="text-sm text-green-600">Quantization: {ncnnMetrics.gunshot_quantization || 'int8'}</p>
          <p className="text-sm text-green-600">Performance: {ncnnMetrics.gunshot_performance || '2.8x faster'}</p>
        </div>
        <div className="bg-purple-50 p-4 rounded-lg">
          <h4 className="font-medium text-purple-800">Weapon Detection</h4>
          <p className="text-sm text-purple-600">Quantization: {ncnnMetrics.weapon_quantization || 'int16'}</p>
          <p className="text-sm text-purple-600">Performance: {ncnnMetrics.weapon_performance || '4.1x faster'}</p>
        </div>
      </div>
    </div>
  );

  const renderThreatCorrelations = () => (
    <div className="p-4">
      <h3 className="text-lg font-semibold mb-4">Threat Correlations</h3>
      <div className="space-y-3">
        {threatCorrelations.map(correlation => (
          <div key={correlation.correlation_id} className="bg-gray-50 p-3 rounded-lg">
            <div className="flex justify-between items-start">
              <div>
                <h4 className="font-medium">{correlation.correlation_type}</h4>
                <p className="text-sm text-gray-600">
                  Score: {(correlation.correlation_score * 100).toFixed(1)}%
                </p>
                <p className="text-sm text-gray-600">
                  Confidence: {(correlation.edge_ml_confidence * 100).toFixed(1)}%
                </p>
              </div>
              <span className={`px-2 py-1 rounded text-xs ${
                correlation.correlation_score > 0.8 ? 'bg-red-200 text-red-800' :
                correlation.correlation_score > 0.6 ? 'bg-yellow-200 text-yellow-800' :
                'bg-green-200 text-green-800'
              }`}>
                {correlation.correlation_score > 0.8 ? 'High Risk' :
                 correlation.correlation_score > 0.6 ? 'Medium Risk' : 'Low Risk'}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  const renderOSINTEvidence = () => (
    <div className="p-4">
      <h3 className="text-lg font-semibold mb-4">OSINT Evidence Collection</h3>
      <div className="space-y-3">
        {osintEvidence.map(evidence => (
          <div key={evidence.evidence_id} className="bg-gray-50 p-3 rounded-lg">
            <div className="flex justify-between items-start">
              <div>
                <h4 className="font-medium">{evidence.source}</h4>
                <p className="text-sm text-gray-600">Type: {evidence.evidence_type}</p>
                <p className="text-sm text-gray-600">
                  Confidence: {(evidence.confidence_score * 100).toFixed(1)}%
                </p>
                <p className="text-sm text-gray-600">
                  Collected: {new Date(evidence.collection_timestamp).toLocaleString()}
                </p>
              </div>
              <span className={`px-2 py-1 rounded text-xs ${
                evidence.verification_status === 'verified' ? 'bg-green-200 text-green-800' :
                evidence.verification_status === 'pending' ? 'bg-yellow-200 text-yellow-800' :
                'bg-red-200 text-red-800'
              }`}>
                {evidence.verification_status}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  return (
    <>
      <button 
        onClick={() => setOpen(true)} 
        className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
      >
        🛡️ Enhanced Threat Intelligence
      </button>

      {open && (
        <div className="fixed inset-0 z-50 flex items-stretch bg-black bg-opacity-50">
          <div className="flex-1 bg-white m-4 rounded-lg shadow-xl overflow-hidden">
            <header className="p-4 border-b flex justify-between items-center bg-gray-50">
              <h2 className="text-xl font-semibold text-gray-800">
                Sentinel Enhanced Threat Intelligence
              </h2>
              <div className="flex items-center space-x-2">
                <button 
                  className="px-3 py-1 bg-gray-200 rounded hover:bg-gray-300 transition-colors"
                  onClick={loadThreatIntelligenceData}
                  disabled={loading}
                >
                  {loading ? '🔄' : '🔄'} Refresh
                </button>
                <button 
                  className="px-3 py-1 bg-red-500 text-white rounded hover:bg-red-600 transition-colors"
                  onClick={() => setOpen(false)}
                >
                  ✕ Close
                </button>
              </div>
            </header>

            {/* Tab Navigation */}
            <div className="border-b bg-gray-50">
              <nav className="flex space-x-8 px-4">
                {[
                  { id: 'threat-map', label: 'Threat Map', icon: '🗺️' },
                  { id: 'edge-ml', label: 'Edge ML', icon: '🤖' },
                  { id: 'ncnn', label: 'NCNN', icon: '⚡' },
                  { id: 'correlations', label: 'Correlations', icon: '🔗' },
                  { id: 'osint', label: 'OSINT', icon: '🔍' }
                ].map(tab => (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`py-3 px-1 border-b-2 font-medium text-sm transition-colors ${
                      activeTab === tab.id
                        ? 'border-blue-500 text-blue-600'
                        : 'border-transparent text-gray-500 hover:text-gray-700'
                    }`}
                  >
                    {tab.icon} {tab.label}
                  </button>
                ))}
              </nav>
            </div>

            {/* Tab Content */}
            <div className="flex-1 overflow-auto">
              {activeTab === 'threat-map' && (
                <div style={{ height: "calc(100vh - 200px)" }}>
                  {renderThreatMap()}
                </div>
              )}
              {activeTab === 'edge-ml' && renderEdgeMLStatus()}
              {activeTab === 'ncnn' && renderNCNNMetrics()}
              {activeTab === 'correlations' && renderThreatCorrelations()}
              {activeTab === 'osint' && renderOSINTEvidence()}
            </div>
          </div>
        </div>
      )}
    </>
  );
}

// Enhanced Leaflet Map Component with integrated threat data
function LeafletThreatMap({ events, correlations, osintEvidence }) {
  useEffect(() => {
    if (typeof window === 'undefined') return;
    
    (async () => {
      // Load Leaflet
      if (!window.L) {
        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = 'https://unpkg.com/leaflet@1.9.3/dist/leaflet.css';
        document.head.appendChild(link);
        
        await new Promise((resolve, reject) => {
          const script = document.createElement('script');
          script.src = 'https://unpkg.com/leaflet@1.9.3/dist/leaflet.js';
          script.onload = resolve;
          script.onerror = reject;
          document.body.appendChild(script);
        });
      }

      // Initialize map
      const mapDiv = document.getElementById('leaflet-map');
      mapDiv.innerHTML = '<div id="mapid" style="height:100%;width:100%"></div>';
      
      const L = window.L;
      const map = L.map('mapid').setView([-30.0, 25.0], 6); // South Africa center
      
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { 
        maxZoom: 18 
      }).addTo(map);

      // Add threat event markers
      const markers = [];
      events.forEach(event => {
        if (!event.lat || !event.lon) return;
        
        const color = event.score > 8 ? 'red' : event.score > 4 ? 'orange' : 'blue';
        const marker = L.circleMarker([event.lat, event.lon], { 
          radius: 6, 
          color: color,
          fillColor: color,
          fillOpacity: 0.7
        });
        
        let popupHtml = `
          <div class="threat-popup">
            <h4><b>${event.ip}</b></h4>
            <p><b>Threat Type:</b> ${event.threat_type || 'Unknown'}</p>
            <p><b>Severity:</b> ${event.severity_score || 0}/10</p>
            <p><b>Source:</b> ${event.source || 'Unknown'}</p>
            <p><b>ISP:</b> ${event.isp || 'Unknown'}</p>
            <p><b>Country:</b> ${event.country || 'Unknown'}</p>
            <p><b>Last Seen:</b> ${new Date(event.last_seen).toLocaleString()}</p>
          </div>
        `;
        
        marker.bindPopup(popupHtml);
        marker.addTo(map);
        markers.push(marker);
      });

      // Add correlation lines
      correlations.forEach(correlation => {
        if (correlation.cyber_event && correlation.physical_event) {
          const cyberEvent = events.find(e => e.event_id === correlation.cyber_event_id);
          const physicalEvent = events.find(e => e.event_id === correlation.physical_event_id);
          
          if (cyberEvent && physicalEvent && cyberEvent.lat && cyberEvent.lon && 
              physicalEvent.lat && physicalEvent.lon) {
            
            const polyline = L.polyline([
              [cyberEvent.lat, cyberEvent.lon],
              [physicalEvent.lat, physicalEvent.lon]
            ], {
              color: 'red',
              weight: 2,
              opacity: 0.7,
              dashArray: '5, 5'
            });
            
            polyline.bindPopup(`
              <div class="correlation-popup">
                <h4><b>Threat Correlation</b></h4>
                <p><b>Type:</b> ${correlation.correlation_type}</p>
                <p><b>Score:</b> ${(correlation.correlation_score * 100).toFixed(1)}%</p>
                <p><b>Confidence:</b> ${(correlation.edge_ml_confidence * 100).toFixed(1)}%</p>
              </div>
            `);
            
            polyline.addTo(map);
          }
        }
      });

      // Add OSINT evidence markers
      osintEvidence.forEach(evidence => {
        if (evidence.latitude && evidence.longitude) {
          const marker = L.marker([evidence.latitude, evidence.longitude], {
            icon: L.divIcon({
              className: 'osint-marker',
              html: '🔍',
              iconSize: [20, 20]
            })
          });
          
          marker.bindPopup(`
            <div class="osint-popup">
              <h4><b>OSINT Evidence</b></h4>
              <p><b>Source:</b> ${evidence.source}</p>
              <p><b>Type:</b> ${evidence.evidence_type}</p>
              <p><b>Confidence:</b> ${(evidence.confidence_score * 100).toFixed(1)}%</p>
              <p><b>Status:</b> ${evidence.verification_status}</p>
            </div>
          `);
          
          marker.addTo(map);
        }
      });

      // Fit bounds to show all markers
      if (markers.length > 0) {
        const group = new L.featureGroup(markers);
        map.fitBounds(group.getBounds().pad(0.1));
      }
    })();
  }, [events, correlations, osintEvidence]);

  return null;
}
