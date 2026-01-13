import React, { useState, useEffect } from "react";

export default function Favorites() {
  const [favorites, setFavorites] = useState([]);

  useEffect(() => {
    fetch("/favorites")
      .then((r) => r.json())
      .then(setFavorites)
      .catch((err) => console.error("Failed to fetch favorites:", err));
  }, []);

  const removeFavorite = (favId) => {
    const favToRemove = favorites.find((f) => f.id === favId);
    if (!favToRemove) return;

    fetch("/favorites", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ house_id: favToRemove.house_id }),
    })
      .then(() => {
        setFavorites(favorites.filter((f) => f.id !== favId));
      })
      .catch((err) => console.error("Failed to remove favorite:", err));
  };

  return (
    <div className="container">
      <h2>My Favorites ❤️</h2>
      {favorites.length === 0 ? (
        <p>Your list is empty. Start exploring!</p>
      ) : (
        <div className="house-grid">
          {favorites.map((fav) => (
            <div key={fav.id} className="house-card" style={{ position: "relative" }}>
              <button
                className="remove-btn"
                onClick={() => removeFavorite(fav.id)}
                style={{ position: "absolute", right: "10px", top: "10px", zIndex: 1 }}
              >
                ❌
              </button>
              <img src={fav.house.image_url} alt={fav.house.location} />
              <div className="card-info">
                <h3>{fav.house.location}</h3>
                <p>★ {fav.house.average_rating}</p>
                <p>
                  <strong>${fav.house.price_per_night}</strong> / night
                </p>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
