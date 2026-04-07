import { useState } from 'react'

const API_BASE_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

function App() {
  const [connectionStatus, setConnectionStatus] = useState("Click the button to check the connection...");

  const checkApi = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/test-connection`);
      if (!response.ok) {
        throw new Error(`API returned HTTP ${response.status}`);
      }
      const data = await response.json();
      setConnectionStatus(data.message);
    } catch (error) {
      setConnectionStatus("Error connecting to Python API");
      console.error(error);
    }
  };

  return (
    <div style={{ textAlign: 'center', marginTop: '50px' }}>
      <h1>teLLMach Test Hub</h1>
      <button onClick={checkApi} style={{ padding: '10px 20px', fontSize: '16px' }}>
        Check Connection with Python API
      </button>
      <p style={{ marginTop: '20px', fontWeight: 'bold' }}>{connectionStatus}</p>
    </div>
  )
}

export default App