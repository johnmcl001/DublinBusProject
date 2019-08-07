import React, { Component, setState } from "react";
import {
  withGoogleMap,
  GoogleMap,
  Marker,
  InfoWindow,
  Polyline
} from "react-google-maps";
import "../Static/StyleSheet/Map.css";
import MarkerContainer from "./MarkerContainer.js";
import * as stationkeys from "./frontEndBusInfo.json";
import ls from "local-storage";

class Map extends Component {
  constructor(props) {
    super(props);
    this.state = {
      //Holds markers we need to mark route/stops
      polyline: []
    };
    this.polyCoords = this.props.polyline;

  }
  addPolyline = props => {
    this.polyCoords.push(props.polyline);
  };

  componentWillReceiveProps() {
    this.setState({ polyline: this.props.polyline });
    console.log(this.props.markers)
  }

  onClick(route, stopNumber){
    console.log("here")
    console.log(route)
    console.log(stopNumber)
  }

  render() {
    {
      /* Creates the marker if it is in the markers array(state)
               We only want this to update when markers state is updated.*/
    }
    const MapWithAMarker = withGoogleMap(props => (
      <GoogleMap
        defaultZoom={11}
        defaultCenter={{
          lat: 53.309418194004,
          lng: -6.21877482979353
        }}

            defaultOptions={{

            disableDefaultUI: true,

          }}
      >
        <Polyline
          path={this.props.polyline}
          strokeColor="#0000FF"
          strokeOpacity={0.8}
          strokeWeight={2}
        />
          {this.props.markers.map((x, y) => (
            <Marker
          position={{
            lat: x.lat,
            lng: x.lng
          }}
        />
          ))}


      </GoogleMap>
    ));

    return (
      <div id="map">
        <div className="d-none d-lg-block d-md-none">
          <div
            id="map-container-google-1 "

            /*Deyan comment out below line to Make map full screen , Just ensure It is ok to be removed */
            // className="z-depth-1-half map-container border border-primary"
          >
       <MapWithAMarker
     containerElement={<div style={{ height: `100vh`,width:'100%'}} />}
     mapElement={<div style={{ height: `100%` }} />}
   />
          </div>{" "}
        </div>{" "}
      </div>
    );
  }
}
export default Map;
