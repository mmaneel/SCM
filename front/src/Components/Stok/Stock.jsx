import React, { useState, useEffect } from 'react';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import axios from 'axios';
import 'primereact/resources/themes/saga-blue/theme.css';  // Theme
import 'primereact/resources/primereact.min.css';  // Core CSS
import 'primeicons/primeicons.css';  // Icons
import './Stock.css';
import TrackingControl from '../TrackingControl/TrackingControl';

function Stock() {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = () => {
    axios.get('http://127.0.0.1:5000/api/products')
      .then(response => {
        setProducts(response.data);
        console.log(response.data);
      })
      .catch(error => {
        console.error('Error fetching products:', error);
      });
  };

  return (
    <>
    <TrackingControl/>
    <div className='liste_commande1'>
      <h1 className='liste_commande-titre'>Stock status:</h1>
      <DataTable value={products} paginator rows={7} tableStyle={{ minWidth: '50rem' }}>
        <Column field="nom" header="Product Name" style={{ width: '15%' }}></Column>
        <Column field="qte" header="Quantity in Stock" style={{ width: '15%' }}></Column>
       
      </DataTable>
    </div>
    </>
  );
}

export default Stock;
