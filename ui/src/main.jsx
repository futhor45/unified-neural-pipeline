
import React from "react";
import { createRoot } from "react-dom/client";
import UploadForm from "./components/UploadForm";

function App(){
  return <div style={{padding:20}}><h1>Unified Neural Pipeline UI (React)</h1><UploadForm/></div>
}

createRoot(document.getElementById('root')).render(<App />);
