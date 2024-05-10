import React, { useState, useEffect } from 'react';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';


import "./Stock.css"

function Stock() {
    const [userAccount, setUserAccount] = useState([
        { productname: 'T-Shirt', qte: 50, entries: 10, Outputs: 20 },
        { productname: 'Jeans', qte: 35, entries: 15, Outputs: 10 },
        { productname: 'Hat', qte: 20, entries: 5, Outputs: 8 },
        // ... add more objects for additional stock items
      ]);
      
  return (
    <>
    <div className='liste_commande'>
         <h1 className='liste_commande-titre'>  Stock status :</h1>
        
         <DataTable value={userAccount} paginator rows={7}  tableStyle={{ minWidth: '50rem'}}>
        
           <Column field="productname" header=" Product_name" style={{ width: '15%' }}></Column>
           <Column field="qte" header="quantity in the stock " style={{ width: '15%' }}></Column>
           <Column field="entries" header="entries" style={{ width: '15%' }}></Column>
           <Column field="Outputs" header="Outputs"style={{ width: '15%' }} ></Column>
         </DataTable>
           
         
       </div>
 
    </>
  )
}

export default Stock