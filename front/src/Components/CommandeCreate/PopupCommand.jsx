import React, { useState } from 'react';
import Modal from 'react-modal'; // Modifier l'importation ici
import "./Commande.css";

function PopupCommand({ isOpen, onClose, message }) {
  return (
    <Modal  isOpen={isOpen} onRequestClose={onClose}
    style={{
        content: {
          backgroundColor: 'transparent',
          border: 'none', // Remove default border
          padding: 0, // Remove default padding
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          textAlign:'center',
          position: 'fixed',
          top: 0,
          left: 0,
          width: '100%',
          height: '100%',
        },
        overlay: {
          backgroundColor: 'rgba(0, 0, 0, 0.5)', // Semi-transparent background
          backdropFilter: 'blur(5px)', // Add blur filter for the background
        },
      }}>
      <div className="popup-content">
        <h2>Confirmation</h2>
        <p>{message}</p>
        <button onClick={onClose}>Close</button>
      </div>
    </Modal>
  )
}

export default PopupCommand;
