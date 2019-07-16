import { Map, GoogleApiWrapper, Marker, InfoWindow, Polyline } from "google-maps-react";
import React, { Component } from "react";
import "../Static/StyleSheet/Map.css";
//import * as stationData from "./stop_info.json";
import * as stationkeys from "./frontEndBusInfo.json";
import * as markerslist from "./oneRoute.json";

class MapContainer extends Component {
  constructor(props) {
      super(props);
      this.state = {
        showingInfoWindow: false,
        activeMarker: {},
        selectedPlace: {},
        markers: markerslist[0][0],

      };
      this.polyCoords= [];
    }
    shouldComponentUpdate(nextProps, nextState) {
       return nextState.markers != this.markers;
        }

    onMarkerClick = (props, marker, e) =>{
        this.setState({
          selectedPlace: props,
          activeMarker: marker,
          showingInfoWindow: true
        });
    }

    onMapClicked = (props) => {
    if (this.state.showingInfoWindow) {
      this.setState({
        showingInfoWindow: false,
        activeMarker: null
      });
    }
  };
  addPolyline=(props)=>{
    this.polyCoords.push(props);
  }


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
              <InfoWindow
        marker={this.state.activeMarker}
        visible={this.state.showingInfoWindow}>
          <div>
            <p>{this.state.selectedPlace.name}</p>
          </div>
      </InfoWindow>

      <Polyline
          path={this.polyCoords}
          strokeColor="#0000FF"
          strokeOpacity={0.8}
          strokeWeight={2} />


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
