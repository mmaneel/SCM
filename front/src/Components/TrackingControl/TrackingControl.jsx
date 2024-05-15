import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';


import "./TrackingControl.css"


function TrackingControl() {
   
 
  return (
    <>
     <div className='navbar'>
        <nav>
         <Link to="/"> Create commande </Link>
         <Link to="/listecommande">All Commande</Link>
         <Link to="/stock"> Stock</Link>
        </nav>
      </div>
 
    </>
  )
}

export default TrackingControl