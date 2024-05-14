import React, { useState, useEffect } from 'react';
import "./Commande.css"
import AddCircleOutlineIcon from '@mui/icons-material/AddCircleOutline';
import Popup from './PopupCommand'
import axios from 'axios';

function CommandeCreate() {
  const produits = [
    {
      id: 1,
      nom: 'Produit 1',
      qte: 0,
    },
    {
      id: 2,
      nom: 'Produit 2',
      qte: 0,
    },
    {
      id: 3,
      nom: 'Produit 3',
      qte: 0,
    },
    {
      id: 4,
      nom: 'Produit 4',
      qte: 0,
    },
    {
      id: 5,
      nom: 'Produit 5',
      qte: 0,
    },
    {
      id: 6,
      nom: 'Produit 6',
      qte: 0,
    },
  ];

  const [counts, setCounts] = useState(Array(produits.length).fill(0));
  const [selectedProducts, setSelectedProducts] = useState({}); // Stocker les produits sélectionnés dans un objet

  const incrementCount = (index) => {
    const newCounts = [...counts];
    newCounts[index] += 1;
    setCounts(newCounts);

    const productId = produits[index].id;
    setSelectedProducts(prevSelectedProducts => {
      // Vérifier si le produit est déjà sélectionné
      if (prevSelectedProducts.hasOwnProperty(productId)) {
        // S'il est déjà sélectionné, mettre à jour la quantité
        return {
          ...prevSelectedProducts,
          [productId]: prevSelectedProducts[productId] + 1
        };
      } else {
        // S'il n'est pas déjà sélectionné, l'ajouter avec une quantité de 1
        return {
          ...prevSelectedProducts,
          [productId]: 1
        };
      }
    });
  };

  // Fonction pour réinitialiser la quantité d'un produit à zéro
  const resetCount = (index) => {
    const newCounts = [...counts];
    newCounts[index] = 0;
    setCounts(newCounts);
  };

  const removeFromSelected = (productId, index) => {
    resetCount(index); // Réinitialiser la quantité du produit à zéro
    setSelectedProducts(prevSelectedProducts => {
      const updatedSelected = { ...prevSelectedProducts };
      delete updatedSelected[productId];
      return updatedSelected;
    });
  };

  const [p_nom_client, setFirstName] = useState('');
  const [p_prenom_client, setLastName] = useState('');
  const [p_num_tel, setPhoneNumber] = useState('');
  const [p_numero_carte, setCardNumber] = useState('');
  const [p_cvv, setCardcvv] = useState('');
  const [p_adresse, setAdresse] = useState('');
  const [p_type_i, setCardType] = useState('');
  const [p_code_postal, setCodePostal] = useState('');
  const [p_date_exp, setExpDate] = useState('');
  const [isPopupOpen, setIsPopupOpen] = useState(false); // State for popup visibility
  const [popupMessage, setPopupMessage] = useState(''); // State for popup message

  // Définir un état pour stocker les produits récupérés
  const [products, setProducts] = useState([]);

  // Fonction pour récupérer les produits depuis le backend
  const fetchProducts = () => {
    axios.get('http://127.0.0.1:5000/api/products')
      .then(response => {
        // Mettre à jour l'état des produits avec les données récupérées depuis le backend
        setProducts(response.data);
        console.log(response.data)
      })
      .catch(error => {
        // Gérer les erreurs de récupération des produits depuis le backend
        console.error('Error fetching products:', error);
      });
  };

  // Appeler la fonction pour récupérer les produits lorsque le composant est monté
  useEffect(() => {
    fetchProducts();
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();

    // Construire l'objet de données à envoyer au backend
    const data = {
      p_nom_client: p_nom_client,
      p_prenom_client: p_prenom_client,
      p_num_tel: parseInt(p_num_tel),
      p_numero_carte: p_numero_carte,
      p_cvv: parseInt(p_cvv),
      p_adresse: p_adresse,
      p_type_i: parseInt(p_type_i),
      p_code_postal: parseInt(p_code_postal),
      p_date_exp: parseInt(p_date_exp),
      product_quantity: Object.entries(selectedProducts).map(([productId, quantity]) => ({ productId: parseInt(productId), quantity }))
    };
    console.log(data)
    // Envoyer les données au backend
    axios.post('http://127.0.0.1:5000/api/create_commande', data)
      .then(response => {
        // Traiter la réponse du backend si nécessaire
        console.log(response.data);
        const message = 'Thank you for your order. We will contact you for the details.';
        setPopupMessage(message);
        setIsPopupOpen(true);
      })
      .catch(error => {
        // Gérer les erreurs
        console.error('Error:', error);
      });
    }
  const handlePopupClose = () => {
    setIsPopupOpen(false);
  };

  return (
    <>
      <div className='create_commande'>
        <h1 className='create_commande-titre'>  Add your  order :</h1>
        <div className='produit_content'>
          {products.map((produit, index) => (
            <div className='produit_item' key={index}>
              <h3>{produit.nom}</h3>
              <p>quantité : {produit.qte}</p>
              <div className='ligne'></div>
              <div className='add_produit' >
                <div style={{ display: "flex", backgroundColor: 'transparent' }}>
                  <AddCircleOutlineIcon sx={{ backgroundColor: 'transparent', color: '#FFD335', cursor: 'pointer' }} onClick={() => incrementCount(index)} />
                  <span>{counts[index]}</span>
                </div>
                <button className='add_btn' onClick={() => removeFromSelected(produit.id, index)}>Remove</button>
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
              <label htmlFor="p_nom_client">Prénom</label>
              <input type="text" id="p_nom_client" name="p_nom_client" value={p_nom_client} onChange={(e) => setFirstName(e.target.value)} />
            </div>
            <div className="input-group">
              <label htmlFor="p_prenom_client">Nom</label>
              <input type="text" id="p_prenom_client" name="p_prenom_client" value={p_prenom_client} onChange={(e) => setLastName(e.target.value)} />
            </div>
            <div className="input-group">
              <label htmlFor="p_num_tel">Numéro de téléphone</label>
              <input type="tel" id="p_num_tel" name="p_num_tel" value={p_num_tel} onChange={(e) => setPhoneNumber(e.target.value)} />
            </div>
          </div>
          <div className="input-group-container">
            <div className="input-group">
              <label htmlFor="p_numero_carte">Numéro de carte</label>
              <input type="text" id="p_numero_carte" name="p_numero_carte" value={p_numero_carte} onChange={(e) => setCardNumber(e.target.value)} />
            </div>
            <div className="input-group">
              <label htmlFor="p_cvv">P Cvv</label>
              <input type="text" id="p_cvv" name="p_cvv" value={p_cvv} onChange={(e) => setCardcvv(e.target.value)} />
            </div>
            <div className="input-group">
              <label htmlFor="p_type_i">Type de carte</label>
              <input type="text" id="p_type_i" name="p_type_i" value={p_type_i} onChange={(e) => setCardType(e.target.value)} />
            </div>
            <div className="input-group">
              <label htmlFor="p_date_exp">Date d'expiration</label>
              <input type="text" id="p_date_exp" name="p_date_exp" value={p_date_exp} onChange={(e) => setExpDate(e.target.value)} />
            </div>
          </div>
          <div className="input-group-container">
            <div className="input-group">
              <label htmlFor="p_adresse">Adresse</label>
              <input type="text" id="p_adresse" name="p_adresse" value={p_adresse} onChange={(e) => setAdresse(e.target.value)} />
            </div>
            <div className="input-group">
              <label htmlFor="p_code_postal">Code postal</label>
              <input type="text" id="p_code_postal" name="p_code_postal" value={p_code_postal} onChange={(e) => setCodePostal(e.target.value)} />
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
