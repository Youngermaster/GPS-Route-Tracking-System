import React, { useState, useEffect } from 'react';
import { View } from 'react-native';
import MapView, { Polyline } from 'react-native-maps';

const MapScreen = () => {
  const [polyline, setPolyline] = useState([]);
  const [initialRegion, setInitialRegion] = useState(null);

  const fetchPolyline = async () => {
    try {
      const response = await fetch('http://10.0.2.2:6969/route/route-123/polyline');
      const data = await response.json();
      setPolyline(data.polyline);

      // Set initial region to the first point of the polyline
      if (data.polyline && data.polyline.length > 0) {
        const [latitude, longitude] = data.polyline[0];
        setInitialRegion({
          latitude,
          longitude,
          latitudeDelta: 0.0922, // Adjust these values as needed
          longitudeDelta: 0.0421,
        });
      }
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    fetchPolyline();
  }, []);

  return (
    <View style={{ flex: 1 }}>
      {initialRegion && (
        <MapView
          style={{ flex: 1 }}
          initialRegion={initialRegion}
        >
          <Polyline
            coordinates={polyline.map(coord => ({ latitude: coord[0], longitude: coord[1] }))}
            strokeWidth={3}
            strokeColor='green'
          />
        </MapView>
      )}
    </View>
  );
};

export default MapScreen;
