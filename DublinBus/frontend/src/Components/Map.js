import { Map, GoogleApiWrapper, mapStyles } from "google-maps-react";
import React, { Component } from "react";

class MapContainer extends Component {
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
              zoom={8}
              style={mapStyles}
              initialCenter={{ lat: 53.3501, lng: -6.2661 }}
            />
          </div>
        </div>
      </div>
    );
  }
}
export default GoogleApiWrapper({
  apiKey: "AIzaSyDBnVde8R4LpYQapr6-zbAHPD5Xcva9H_c"
})(MapContainer);
