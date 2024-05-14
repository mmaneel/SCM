import React, { useState, useEffect } from 'react';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import AccountCircleOutlinedIcon from '@mui/icons-material/AccountCircleOutlined';
import { Select, MenuItem } from '@mui/material';
import PopupValidate from './PopupValidate';
import axios from 'axios';
import "./ListCommande.css";

function ListCommande() {
  const [userAccount, setUserAccount] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [selectedRow, setSelectedRow] = useState(null);
  const [notification, setNotification] = useState('');
  const [notification1, setNotification1] = useState('');
  const [notification2, setNotification2] = useState('');

  const handleOpenModal = (rowData) => {
    setSelectedRow(rowData);
    setShowModal(true);
  };

  const handleCloseModal = () => {
    setShowModal(false);
    setNotification('');
  };

  const fetchOrders = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5000/api/orders');
      setUserAccount(response.data);
    } catch (error) {
      console.error('Error fetching orders:', error);
    }
  };

  useEffect(() => {
    fetchOrders();
  }, []);

  const renderIcon = () => {
    return <AccountCircleOutlinedIcon />;
  };

  const handleChangeStatus = async (event, rowData) => {
    const newStatus = event.target.value;
    const updateData = {
      p_commande_id: rowData.id,
      p_nouveau_statut: newStatus,
    };

    try {
      const response = await axios.post('http://127.0.0.1:5000/api/maj_status', updateData);
      const result = response.data;

      // Update the local state to reflect the status change
      setUserAccount(prevState =>
        prevState.map(order =>
          order.id === rowData.id ? { ...order, status: newStatus } : order
        )
      );
console.log(result[0]['result'])
      // Display the notification from the backend response
      setNotification(result[0]['result']);
      console.log(notification)
      handleOpenModal(rowData);
      //console.log(`Statut de la commande ${rowData.id} mis à jour avec succès.`);
    } catch (error) {
      console.error('Erreur lors de la mise à jour du statut:', error);
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 2:
        return '#FFFF00';
      case 3:
        return '#FFA500';
      case 4:
        return '#32CD32';
      case 5:
        return '#FF0000';
      case 6:
        return '#0000FF';
      case 7:
        return '#800080';
      case 8:
        return '#FF1493';
      default:
        return '#000000';
    }
  };

  const getStatusLabel = (status) => {
    switch (status) {
      case 2:
        return 'Validée';
      case 3:
        return 'En transit';
      case 4:
        return 'Livraison réussie';
      case 5:
        return 'Annulée';
      case 6:
        return 'En attente de stock';
      case 7:
        return 'Retardée';
      case 8:
        return 'Remboursée';
      default:
        return '';
    }
  };

  return (
    <>
      <div className='liste_commande'>
        <h1 className='liste_commande-titre'>Liste de commandes :</h1>
        <DataTable value={userAccount} paginator rows={5} tableStyle={{ minWidth: '50rem' }}>
          <Column header="" body={renderIcon} style={{ width: '15%' }} />
          <Column field="client" header="First and Last Name" style={{ width: '15%' }} />
          <Column field="phone" header="Numéro de téléphone " style={{ width: '15%' }} />
          <Column field="id" header="Numéro_Commande" style={{ width: '15%' }} />
          <Column field="date" header="date_commande" style={{ width: '15%' }} />
          <Column field="total" header="Total" style={{ width: '15%' }} />
          <Column
            field="status"
            header=""
            body={(rowData) => (
              <div className="status-select">
                <Select
                  className={`select-opt select-bg-white`}
                  value={rowData.status}
                  onChange={(event) => handleChangeStatus(event, rowData)}
                  displayEmpty
                  inputProps={{ 'aria-label': 'Without label' }}
                  style={{
                    color: getStatusColor(rowData.status),
                  }}
                >
                  <MenuItem value={2} style={{ color: '#FFFF00' }}>
                  Validée
                  </MenuItem>
                  <MenuItem value={3} style={{ color: '#FFA500' }}>
                    En transit
                  </MenuItem>
                  <MenuItem value={4} style={{ color: '#32CD32' }}>
                    Livraison réussie
                  </MenuItem>
                  <MenuItem value={5} style={{ color: '#FF0000' }}>
                    Annulée
                  </MenuItem>
                  <MenuItem value={6} style={{ color: '#0000FF' }}>
                    En attente de stock
                  </MenuItem>
                  <MenuItem value={7} style={{ color: '#800080' }}>
                    Retardée
                  </MenuItem>
                  <MenuItem value={8} style={{ color: '#FF1493' }}>
                    Remboursée
                  </MenuItem>
                </Select>
                
              </div>
            )}
            style={{ width: '15%' }}
          />
        </DataTable>
        {notification && (
          <div className="notification">
            <pre style={{color:'white'}}>{notification}</pre>
          </div>
        )}
      </div>
      <PopupValidate isOpen={showModal} onClose={handleCloseModal} selectedRow={selectedRow} notification={notification} />
    </>
  );
}

export default ListCommande;
