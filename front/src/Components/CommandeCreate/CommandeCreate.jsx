import React, { useState } from 'react';
import "./Commande.css"
import AddCircleOutlineIcon from '@mui/icons-material/AddCircleOutline';
import Popup from './PopupCommand'
import axios from 'axios';

function CommandeCreate() {
  const produits = [
    {
      id: 1,
      title: 'Produit 1',
      description: 'Description du produit 1',
    },
    {
      id: 2,
      title: 'Produit 2',
      description: 'Description du produit 2',
    },
    {
      id: 3,
      title: 'Produit 3',
      description: 'Description du produit 3',
    },
    {
      id: 4,
      title: 'Produit 4',
      description: 'Description du produit 4',
    },
    {
      id: 5,
      title: 'Produit 5',
      description: 'Description du produit 5',
    },
    {
      id: 6,
      title: 'Produit 6',
      description: 'Description du produit 6',
    },
  ];

  // Tableau d'états pour suivre le nombre d'incréments pour chaque produit
  const [counts, setCounts] = useState(Array(produits.length).fill(0));

  // Fonction pour incrémenter le nombre pour un produit spécifique
  const incrementCount = (index) => {
    // Créer une copie du tableau des counts
    const newCounts = [...counts];
    // Incrémenter le compteur pour le produit à l'index donné
    newCounts[index] += 1;
    // Mettre à jour le tableau des counts
    setCounts(newCounts);
  };


  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [phoneNumber, setPhoneNumber] = useState('');
  const [cardNumber, setCardNumber] = useState('');
  const [expDate, setExpDate] = useState('');
  const [isPopupOpen, setIsPopupOpen] = useState(false); // State for popup visibility
  const [popupMessage, setPopupMessage] = useState(''); // State for popup message


  const handleSubmit = (e) => {
    e.preventDefault();

    // Construire un tableau d'objets contenant les informations de chaque produit
    const productsData = produits.map((produit, index) => {
      return {
        productId: produit.id,
        quantity: counts[index]
      };
    });

    // Construire l'objet de données à envoyer au backend
    const data = {
      firstName: firstName,
      lastName: lastName,
      phoneNumber: phoneNumber,
      cardNumber: cardNumber,
      expDate: expDate,
      products: productsData
    };

    // Envoyer les données au backend
    axios.post('/api/commande', data)
      .then(response => {
        // Traiter la réponse du backend si nécessaire
        console.log(response.data);
        const message = 'Thank you for your order We will contact you for the details.';
        setPopupMessage(message);
        setIsPopupOpen(true);
      })
      .catch(error => {
        // Gérer les erreurs
        console.error('Error:', error);
      });
  };
  
  const handlePopupClose = () => {
    setIsPopupOpen(false);
  };


  return (
    <>
      <div className='create_commande'>
        <h1 className='create_commande-titre'>  Add your  order :</h1>
        <div className='produit_content'>
          {produits.map((produit, index) => (
            <div className='produit_item' key={index}>
              <h3>{produit.title}</h3>
              <p>{produit.description}</p>
              <div className='ligne'></div>
              <div className='add_produit' >
                <div style={{ display: "flex", backgroundColor: 'transparent' }}>
                  <AddCircleOutlineIcon sx={{ backgroundColor: 'transparent', color: '#FFD335', cursor: 'pointer' }} onClick={() => incrementCount(index)} />
                  <span>{counts[index]}</span>
                </div>
                <button className='add_btn'>Add</button>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="signup-form">
      <h3>Please fill up your information:</h3>
      <form onSubmit={handleSubmit}>
        <div className="input-group-container">
          <div className="input-group">
            <label htmlFor="firstName">Prénom</label>
            <input type="text" id="firstName" name="firstName" value={firstName} onChange={(e) => setFirstName(e.target.value)} />
          </div>
          <div className="input-group">
            <label htmlFor="lastName">Nom</label>
            <input type="text" id="lastName" name="lastName" value={lastName} onChange={(e) => setLastName(e.target.value)} />
          </div>
          <div className="input-group">
            <label htmlFor="phoneNumber">Numéro de téléphone</label>
            <input type="tel" id="phoneNumber" name="phoneNumber" value={phoneNumber} onChange={(e) => setPhoneNumber(e.target.value)} />
          </div>
        </div>
        <div className="input-group-container">
          <div className="input-group">
            <label htmlFor="cardNumber">Numéro de carte</label>
            <input type="text" id="cardNumber" name="cardNumber" value={cardNumber} onChange={(e) => setCardNumber(e.target.value)} />
          </div>
          <div className="input-group">
            <label htmlFor="expDate">Date d'expiration</label>
            <input type="text" id="expDate" name="expDate" value={expDate} onChange={(e) => setExpDate(e.target.value)} />
          </div>
        </div>
        <button type="submit">Confirm your Command</button>
      </form>
      <Popup isOpen={isPopupOpen} onClose={handlePopupClose} message={popupMessage} />
    </div>
    </>
  )
}

export default CommandeCreate;
