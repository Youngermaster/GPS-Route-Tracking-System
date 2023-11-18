import React, { useState, useEffect, useRef } from 'react';
import { StyleSheet, View, Text, TouchableOpacity, Alert, PermissionsAndroid, Platform } from 'react-native';
import Geolocation from '@react-native-community/geolocation';
import { Client, Message } from 'react-native-paho-mqtt';  // MQTT client for react-native

// Define the data structure for each driver
interface DriverData {
  driverId: string;
  driverLocation: {
    latitude: number;
    longitude: number;
  };
  route: any[];
  registerId: string;
  colorVehicle: boolean;
  indexDriver: number;
  iconMetro: boolean;
  timestamp: number;
}

// In-memory storage object for MQTT client
const myStorage = {
  setItem: (key: string, item: string) => {
    myStorage[key] = item;
  },
  getItem: (key: string) => myStorage[key],
  removeItem: (key: string) => {
    delete myStorage[key];
  },
};

const App: React.FC = () => {
  const [isSharing, setIsSharing] = useState(false);
  const [mqttClient, setMqttClient] = useState<Client | null>(null);
  const watchId = useRef<number | null>(null); // Ref to store the watch ID

  useEffect(() => {
    // Create a client instance
    // ! 10.0.2.2 is the bridge to the localhost connection on the emulator
    // ! 10.0.2.2 -> Special alias to your host loopback interface (127.0.0.1 on your development machine)
    // const client = new Client({ uri: 'ws://10.0.2.2:8083/mqtt', clientId: 'rn-client', storage: myStorage });
    const client = new Client({ uri: 'ws://cpu-liability-tons-supposed.trycloudflare.com/mqtt', clientId: 'rn-client', storage: myStorage });
    setMqttClient(client);

    client.on('connectionLost', responseObject => {
      if (responseObject.errorCode !== 0) {
        console.log('Connection lost:', responseObject.errorMessage);
      }
    });

    client.connect()
      .then(() => {
        console.log('Connected to MQTT broker');
      })
      .catch(error => {
        console.log('Could not connect to MQTT broker:', error);
      });

    return () => {
      if (client) {
        client.disconnect();
      }
    };
  }, []);

  const requestLocationPermission = async () => {
    if (Platform.OS === 'ios') {
      Geolocation.requestAuthorization('whenInUse');
      return true;
    } else {
      try {
        const granted = await PermissionsAndroid.request(
          PermissionsAndroid.PERMISSIONS.ACCESS_FINE_LOCATION,
          {
            title: "Location Access Required",
            message: "This app needs to access your location.",
            buttonPositive: "OK"
          }
        );
        return granted === PermissionsAndroid.RESULTS.GRANTED;
      } catch (err) {
        console.warn(err);
        return false;
      }
    }
  };

  const sendLocation = (position: Geolocation.GeoPosition) => {
    if (mqttClient && mqttClient.isConnected()) {
      const driverData: DriverData = {
        driverId: 'driver-123', // Example driver ID, replace with actual
        driverLocation: {
          latitude: position.coords.latitude,
          longitude: position.coords.longitude,
        },
        route: [], // Populate as needed
        registerId: 'reg-123', // Example register ID, replace with actual
        colorVehicle: true, // Example value, replace with actual
        indexDriver: 1, // Example value, replace with actual
        iconMetro: false, // Example value, replace with actual
        timestamp: Date.now(),
      };

      const message = new Message(JSON.stringify(driverData));
      message.destinationName = 'location/rn-client';
      console.log(message);
      mqttClient.send(message);
    }
  };

  const startLocationTracking = async () => {
    const hasPermission = await requestLocationPermission();
    if (hasPermission) {
      watchId.current = Geolocation.watchPosition(sendLocation, error =>
        Alert.alert('Error', JSON.stringify(error)),
        { enableHighAccuracy: true, distanceFilter: 1, interval: 1000 }
      );
      setIsSharing(true);
    } else {
      Alert.alert('Permission Denied', 'Location permission is required to use this feature');
    }
  };

  const stopLocationTracking = () => {
    if (watchId.current !== null) {
      Geolocation.clearWatch(watchId.current);
      watchId.current = null;
    }
    setIsSharing(false);
  };

  const toggleSharing = () => {
    if (isSharing) {
      stopLocationTracking();
    } else {
      startLocationTracking();
    }
  };

  return (
    <View style={styles.container}>
      <TouchableOpacity style={styles.button} onPress={toggleSharing}>
        <Text style={styles.buttonText}>{isSharing ? 'Stop Sharing' : 'Share Location'}</Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  button: {
    backgroundColor: 'blue',
    padding: 20,
    borderRadius: 5,
  },
  buttonText: {
    color: 'white',
    fontSize: 20,
  },
});

export default App;