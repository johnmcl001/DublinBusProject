import React, {
  Component
} from 'react';
import {
  withGoogleMap,
  GoogleMap,
  Marker,
  InfoWindow,
  Polyline
} from 'react-google-maps';
import "../Static/StyleSheet/Map.css";
import MarkerContainer from './MarkerContainer.js';
import * as stationkeys from "./frontEndBusInfo.json";
import * as markerslist from "./oneRoute.json";

class Map extends Component {
  constructor(props) {
    super(props);
    this.state = {
      //Holds markers we need to mark route/stops
      markers: markerslist[0][0],
    };
    this.polyCoords = [];
  }
  addPolyline = (props) => {
    this.polyCoords.push(props);
  }
  //only update if route/stop is updated
  shouldComponentUpdate(nextProps, nextState) {
    return nextState.markers != this.markers;
  }



  render() {

      {
        /* Creates the marker if it is in the markers array(state)
               We only want this to update when markers state is updated.*/
      }
    this.state.markers.map((station) => {
     //console.log(stationkeys[station]['name']);
     this.addPolyline({ lat: stationkeys[station]['lat'], lng: stationkeys[station]['long']});})
      const MapWithAMarker = withGoogleMap(props =>
        <
        GoogleMap defaultZoom = {
          11
        }
        defaultCenter = {
          {
            lat: 53.3501,
            lng: -6.2661
          }
        } >
        <
        MarkerContainer markers = {
          this.state.markers
        }
        />
        <Polyline
        path={this.polyCoords}
        strokeColor="#0000FF"
        strokeOpacity={0.8}
        strokeWeight={2} />
        <



        /GoogleMap>
      );

      return ( <
        div id = "map" >
        <
        div className = "d-none d-lg-block d-md-none" >
        <
        div id = "map-container-google-1 "
        className = "z-depth-1-half map-container border border-primary" >
        <
        MapWithAMarker containerElement = {
          < div style = {
            {
              height: `100vh`
            }
          }
          />}
          mapElement = {
            < div style = {
              {
                height: `100vh`
              }
            }
            />} /
            >
            <
            /div> <
            /div> <
            /div>
          );
        }
      };
      export default Map;

