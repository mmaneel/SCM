import React from 'react';
import Modal from 'react-modal';
import "./ListCommande.css";

function PopupValidate({ isOpen, onClose, selectedRow, notification }) {
  return (
    <Modal
      isOpen={isOpen}
      onRequestClose={onClose}
      style={{
        overlay: {
          backgroundColor: 'rgba(0, 0, 0, 0.5)', // Semi-transparent background
          backdropFilter: 'blur(5px)', // Add blur filter for the background
        },
        content: {
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          width: '400px',
          padding: '20px',
          border: '1px solid #ccc',
          backgroundColor: '#fff',
        },
      }}
    >
      <div className="popup-content1">
        <h2>Order Status Update</h2>
        <p style={{color:'white'}}>{notification}</p>
        <div className="modal-buttons">
          <button onClick={onClose}>Close</button> {/* Utilisez la fonction pour fermer le modal */}
        </div>
      </div>
    </Modal>
  );
}

export default PopupValidate;
