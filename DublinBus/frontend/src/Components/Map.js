import React, { Component } from 'react';
import { withGoogleMap, GoogleMap, Marker, InfoWindow, Polyline } from 'react-google-maps';
import "../Static/StyleSheet/Map.css";
import InfoWindowMap from './InfoWindow.js';
import * as stationkeys from "./frontEndBusInfo.json";
import * as markerslist from "./oneRoute.json";

class Map extends Component {
  constructor(props) {
      super(props);
      this.state = {
        //Holds InfoWindow Information
        //openInfoWindowMarkerId: '',
        //Holds markers we need to mark route/stops
        markers: markerslist[0][0],
        openInfoWindowMarkerId: '',
      };
      //Holds coordinates to draw route on map
      this.polyCoords= [];
    }

    //adds coordinates from markers to polyline array
    addPolyline=(props)=>{
      this.polyCoords.push(props);
    }
    //only update if route/stop is updated
    shouldComponentUpdate(nextProps, nextState) {
       return nextState.markers != this.markers;
        }


   render() {

     {/* Creates the marker if it is in the markers array(state)
       We only want this to update when markers state is updated.*/}


       //const markersList = markerslist[0][0];
       let markers;
       if (this.state.markers !== null) {
       markers=this.state.markers.map((station) => {
      //console.log(stationkeys[station]['name']);
      this.addPolyline({ lat: stationkeys[station]['lat'], lng: stationkeys[station]['long']});
      return (

						<InfoWindowMap
							key={station}
              name={stationkeys[station]['name']}
							lat={stationkeys[station]['lat']}
							lng={stationkeys[station]['long']}
              index={station}
							/>

				)
			})
		} else {
			console.log('true');
			//markers = <Marker position={{ lat: Number(latCurrentLocation), lng: Number(lngCurrentLocation)}}/>
		}
const MapWithAMarker = withGoogleMap(props =>
        <GoogleMap
          defaultZoom={11}
          defaultCenter={{ lat: 53.3501, lng: -6.2661 }}
        >
        {markers}
        {/* Draws the polyline on the map based on the elements of the polCoords array*/}
        <Polyline
        path={this.polyCoords}
        strokeColor="#0000FF"
        strokeOpacity={0.8}
        strokeWeight={2} />
        </GoogleMap>
      );

   return(
     <div id="map">
        <div className="d-none d-lg-block d-md-none">
          <div
            id="map-container-google-1 "
            className="z-depth-1-half map-container border border-primary"
          >
     <MapWithAMarker
     containerElement={<div style={{ height: `100vh` }} />}
     mapElement={<div style={{ height: `100vh` }} />}
   />
   </div>
</div>
</div>
   );
   }
};
export default Map;
