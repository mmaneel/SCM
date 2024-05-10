import React, { useState } from 'react';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import AccountCircleOutlinedIcon from '@mui/icons-material/AccountCircleOutlined';
import { Tag } from 'primereact/tag';
import PopupValidate from './PopupValidate'; // Importez le composant PopupValidate
import "./ListCommande.css";

function ListCommande() {
     const [userAccount, setUserAccount] = useState([

     { userProfile: 'profile1.jpg', userInfo: 'John Doe', tel: '123456789', numCom: '001', status: 'Validate' },

     { userProfile: 'profile2.jpg', userInfo: 'Jane Smith', tel: '987654321', numCom: '002', status: 'Validate' },

     { userProfile: 'profile2.jpg', userInfo: 'Jane Smith', tel: '987654321', numCom: '002', status: 'Validate' },

     { userProfile: 'profile2.jpg', userInfo: 'Jane Smith', tel: '987654321', numCom: '002', status: 'Validate' },

     { userProfile: 'profile2.jpg', userInfo: 'Jane Smith', tel: '987654321', numCom: '002', status: 'Validate' },

     { userProfile: 'profile2.jpg', userInfo: 'Jane Smith', tel: '987654321', numCom: '002', status: 'Validate' },

     { userProfile: 'profile2.jpg', userInfo: 'Jane Smith', tel: '987654321', numCom: '002', status: 'Validate' },

     { userProfile: 'profile2.jpg', userInfo: 'Jane Smith', tel: '987654321', numCom: '002', status: 'Validate' },

     { userProfile: 'profile2.jpg', userInfo: 'Jane Smith', tel: '987654321', numCom: '002', status: 'Validate' },
         ]);
  const [showModal, setShowModal] = useState(false);
  const [selectedRow, setSelectedRow] = useState(null);

  const handleOpenModal = (rowData) => {
    setSelectedRow(rowData);
    setShowModal(true);
  };

  const handleCloseModal = () => {
    setShowModal(false);
  };

  const renderIcon = () => {
    return <AccountCircleOutlinedIcon />;
  };

  return (
    <>
      <div className='liste_commande'>
        <h1 className='liste_commande-titre'>Liste de commandes :</h1>
        <DataTable value={userAccount} paginator rows={7} tableStyle={{ minWidth: '50rem' }}>
          <Column header="" body={renderIcon} style={{ width: '15%' }} />
          <Column field="userInfo" header="First and Last Name" style={{ width: '15%' }} />
          <Column field="tel" header="Numéro de téléphone " style={{ width: '15%' }} />
          <Column field="numCom" header="Numéro_Commande" style={{ width: '15%' }} />
          <Column
            field="status"
            header=""
            body={(rowData) => (
              <button  className="btn_validate"onClick={() => handleOpenModal(rowData)}> {/* Utilisez la fonction pour ouvrir le modal */}
                <Tag value={rowData.status} className="status-button" />
              </button>
            )}
            style={{ width: '15%' }}
          />
        </DataTable>
      </div>
      {/* Ajoutez le composant PopupValidate avec les props appropriées */}
      <PopupValidate isOpen={showModal} onClose={handleCloseModal} selectedRow={selectedRow} />
    </>
  );
}

export default ListCommande;
