import React, { useState, useEffect } from 'react';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';


import "./TrackingControl.css"


function TrackingControl() {
    const [userAccount, setUserAccount] = useState([
        { order_number: '12345', date: '2024-05-10', prix: '100.00', status: 'Processing' },
        { order_number: '67890', date: '2024-05-08', prix: '50.50', status: 'Shipped' },
        { order_number: '24680', date: '2024-05-07', prix: '22.99', status: 'Delivered' },
        // ... add more objects for additional tracking information
      ]);
 
  return (
    <>
    <div className='liste_commande'>
         <h1 className='liste_commande-titre'>  tracking control :</h1>
        
         <DataTable value={userAccount} paginator rows={7}  tableStyle={{ minWidth: '50rem'}}>
        
           <Column field="order_number" header="order number" style={{ width: '15%' }}></Column>
           <Column field="date" header="date " style={{ width: '15%' }}></Column>
           <Column field="prix" header="prix_total" style={{ width: '15%' }}></Column>
           <Column field="status" header="delivery_status"style={{ width: '15%' }} ></Column>
         </DataTable>
           
         
       </div>
 
    </>
  )
}

export default TrackingControl