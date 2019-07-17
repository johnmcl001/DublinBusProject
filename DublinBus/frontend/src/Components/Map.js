import React, { Component } from 'react';
import { withGoogleMap, GoogleMap, Marker } from 'react-google-maps';
import "../Static/StyleSheet/Map.css";
//import * as stationData from "./stop_info.json";
import * as stationkeys from "./frontEndBusInfo.json";
import * as markerslist from "./oneRoute.json";

class Map extends Component {
  constructor(props) {
      super(props);
      this.state = {
        //Holds InfoWindow Information
        showingInfoWindow: false,
        activeMarker: {},
        selectedPlace: {},
        //Holds markers we need to mark route/stops
        markers: markerslist[0][0],

      };
      //Holds coordinates to draw route on map
      this.polyCoords= [];
    }
    //adds coordinates from markers to polyline array
    addPolyline=(props)=>{
      this.polyCoords.push(props);
    }
   render() {
   const MapWithAMarker = withGoogleMap(props => (

     <GoogleMap
       defaultZoom={11}
       defaultCenter={{ lat: 53.3501, lng: -6.2661 }}
     >
     {/* Creates the marker if it is in the markers array(state)
       We only want this to update when markers state is updated.*/}
    {this.state.markers.map((station) => {
      //console.log(stationkeys[station]['name']);
      this.addPolyline({ lat: stationkeys[station]['lat'], lng: stationkeys[station]['long']});

      return <Marker
        key={station}
        name={stationkeys[station]['name']}
        position={{ lat: stationkeys[station]['lat'], lng: stationkeys[station]['long']}}
        onClick={this.onMarkerClick}
        />
      })}
     </GoogleMap>
   ));

   return(
     <MapWithAMarker
     containerElement={<div style={{ height: `400px` }} />}
     mapElement={<div style={{ height: `100%` }} />}
   />
   );
   }
};
export default Map;
