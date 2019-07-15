import { Map, GoogleApiWrapper, Marker } from "google-maps-react";
import React, { Component } from "react";
import "../Static/StyleSheet/Map.css";
import * as stationData from "./stop_info.json";

class MapContainer extends Component {
  render() {
    //{ console.log([stationData][0]) }
    return (
      <div id="map">
        <div className="d-none d-lg-block d-md-none">
          <div
            id="map-container-google-1 "
            className="z-depth-1-half map-container border border-primary"
          >
            <Map
              google={this.props.google}
              zoom={8}
              initialCenter={{ lat: 53.3501, lng: -6.2661 }}
            >
            {Object.keys([stationData][0]).map((station) => (
              //console.log(stationData[station].lat);
              //console.log(stationData[station].long);
              <Marker
                key={stationData[station].stop}
                position={{ lat: stationData[station].lat, lng: stationData[station].long}}/>
              ))}

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
