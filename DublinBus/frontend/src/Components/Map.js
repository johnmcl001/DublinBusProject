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


class Map extends Component {
  constructor(props) {
    super(props);
    this.state = {
      //Holds markers we need to mark route/stops
      markers: this.props.markers,
      polyline: this.props.polyline
    };
    this.polyCoords = this.props.mapData;
  }
  addPolyline = props => {
    this.polyCoords.push(props);
  };

  componentWillReceiveProps({ props }) {
    this.setState({ polyline: this.props.polyline });
    this.setState({ markers: this.props.markers });
    console.log(this.props);
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
          lat: 53.3501,
          lng: -6.2661
        }}
      >
        <MarkerContainer markers={this.state.markers} />

        <Polyline
          path={this.state.polyline}
          strokeColor="#0000FF"
          strokeOpacity={0.8}
          strokeWeight={2}
        />
      </GoogleMap>
    ));

    return (
      <div id="map">
        <div className="d-none d-lg-block d-md-none">
          <div
            id="map-container-google-1 "
            className="z-depth-1-half map-container border border-primary"
          >
            <MapWithAMarker
              containerElement={
                <div
                  style={{
                    height: `100vh`
                  }}
                />
              }
              mapElement={
                <div
                  style={{
                    height: `100vh`
                  }}
                />
              }
            />
          </div>{" "}
        </div>{" "}
      </div>
    );
  }
}
export default Map;
