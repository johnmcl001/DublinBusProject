import { Map, GoogleApiWrapper, mapStyles } from 'google-maps-react';
import React, { Component } from 'react';

export class MapContainer extends Component {
render() {
    return (
        <Map
          google={this.props.google}
          zoom={8}
          style={mapStyles}
          initialCenter={{ lat: 53.3501, lng: -6.2661}}
        />
    );
  }
}
export default GoogleApiWrapper({
    apiKey: 'AIzaSyDBnVde8R4LpYQapr6-zbAHPD5Xcva9H_c'
  })(MapContainer);