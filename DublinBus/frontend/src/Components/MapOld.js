import {
  Map,
  GoogleApiWrapper,
  Marker,
  InfoWindow,
  Polyline
} from "google-maps-react";
import React, { Component } from "react";
import "../Static/StyleSheet/Map.css";
//import * as stationData from "./stop_info.json";
import * as stationkeys from "./frontEndBusInfo.json";
import * as markerslist from "./oneRoute.json";

class MapContainer extends Component {
  constructor(props) {
    super(props);
    this.state = {
      //Holds InfoWindow Information
      showingInfoWindow: false,
      activeMarker: {},
      selectedPlace: {},
      //Holds markers we need to mark route/stops
      markers: markerslist[0][0]
    };
    //Holds coordinates to draw route on map
    this.polyCoords = [];
  }

  //only update if route/stop is updated
  shouldComponentUpdate(nextProps, nextState) {
    return nextState.markers != this.markers;
  }

  //sets state, opend infowindow when marker is clicked
  onMarkerClick = (props, marker, e) => {
    this.setState({
      selectedPlace: props,
      activeMarker: marker,
      showingInfoWindow: true
    });
  };
  //closes info window if map is clicked
  onMapClicked = props => {
    if (this.state.showingInfoWindow) {
      this.setState({
        showingInfoWindow: false,
        activeMarker: null
      });
    }
  };

  //adds coordinates from markers to polyline array
  addPolyline = props => {
    this.polyCoords.push(props);
  };

  render() {
    return (
      <div id="map">
        <div className="d-none d-lg-block d-md-none">
          <div
            id="map-container-google-1 "
            className="z-depth-1-half map-container border border-primary"
          >
            <Map
              google={this.props.google}
              zoom={11}
              initialCenter={{ lat: 53.3501, lng: -6.2661 }}
            >
              {/* Creates the marker if it is in the markers array(state)
               We only want this to update when markers state is updated.*/}
              {this.state.markers.map(station => {
                this.addPolyline({
                  lat: stationkeys[station]["lat"],
                  lng: stationkeys[station]["long"]
                });

                return (
                  <Marker
                    key={station}
                    name={stationkeys[station]["name"]}
                    position={{
                      lat: stationkeys[station]["lat"],
                      lng: stationkeys[station]["long"]
                    }}
                    onClick={this.onMarkerClick}
                  />
                );
              })}

              {/* Sets Infowindow functionality and state */}
              <InfoWindow
                marker={this.state.activeMarker}
                visible={this.state.showingInfoWindow}
              >
                <div>
                  <p>{this.state.selectedPlace.name}</p>
                </div>
              </InfoWindow>
              {/* Draws the polyline on the map based on the elements of the polCoords array*/}
              <Polyline
                path={this.polyCoords}
                strokeColor="#0000FF"
                strokeOpacity={0.8}
                strokeWeight={2}
              />
            </Map>
          </div>
        </div>
      </div>
    );
  }
}
export default GoogleApiWrapper({
  apiKey: "AIzaSyDBnVde8R4LpYQapr6-zbAHPD5Xcva9H_c"
})(MapContainer);
