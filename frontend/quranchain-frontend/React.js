import React, { useState } from "react";
import axios from "axios";

const GeoMining = () => {
  const [location, setLocation] = useState(null);
  const [message, setMessage] = useState("");

  const checkIn = () => {
    if (!navigator.geolocation) {
      setMessage("Geolocation is not supported by your browser.");
      return;
    }

    navigator.geolocation.getCurrentPosition(
      (position) => {
        const userLocation = {
          latitude: position.coords.latitude,
          longitude: position.coords.longitude,
        };

        setLocation(userLocation);

        // Send location to backend
        axios
          .post("http://127.0.0.1:5000/geo_checkin", {
            location: userLocation,
            miner: "miner_wallet_address", // Replace with actual miner wallet
            prayer_count: 1, // Example: 1 prayer
          })
          .then((response) => setMessage(response.data.message))
          .catch((error) =>
            setMessage("Error during check-in: " + error.response.data.error)
          );
      },
      () => setMessage("Unable to retrieve your location.")
    );
  };

  return (
    <div>
      <h2>Geo-Mining: Check-In</h2>
      <button onClick={checkIn}>Check-In at Masjid</button>
      {location && (
        <p>
          Location: Latitude {location.latitude}, Longitude {location.longitude}
        </p>
      )}
      {message && <p>{message}</p>}
    </div>
  );
};

export default GeoMining;
