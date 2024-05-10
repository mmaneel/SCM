import React from 'react';
import Modal from 'react-modal';
import "./ListCommande.css";

function PopupValidate({ isOpen, onClose, selectedRow }) { // Ajoutez les props selectedRow
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
        <h2>Validate Order</h2>
        <p>Are you sure you want to validate the order for {selectedRow?.userInfo} (Order: {selectedRow?.numCom})?</p> {/* Affichez les informations de la ligne sélectionnée */}
        <div className="modal-buttons">
          <button onClick={onClose}>Cancel</button> {/* Utilisez la fonction pour fermer le modal */}
          <button>Validate</button>
        </div>
      </div>
    </Modal>
  )
}

export default PopupValidate;
