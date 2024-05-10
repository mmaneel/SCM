import React from 'react';
import './App.css';

import CommandeCreate from './Components/CommandeCreate/CommandeCreate';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import ListCommande from './Components/ListeCommande/ListCommande';
import TrackingControl from './Components/TrackingControl/TrackingControl';
import Stock from './Components/Stok/Stock';


function App() {
  return (
    <div className="App">
     
        <Routes>
          <Route path="/" element={<CommandeCreate />} />
          <Route path="/listecommande" element={<ListCommande />} />
          <Route path="/trackingcontrol" element={<TrackingControl />} />
          <Route path="/stock" element={<Stock />} />
        </Routes>
      
    </div>
  );
}


export default App;
