import React, { Component } from "react";
import {
  withGoogleMap,
  GoogleMap,
  Marker,
  InfoWindow,
  Polyline
} from "react-google-maps";
import "../Static/StyleSheet/Map.css";
import * as stationkeys from "./frontEndBusInfo.json";

class MarkerContainer extends Component {
  constructor(props) {
    super(props);
    this.state = {
      markers: this.props.markers,
      openInfoWindowMarkerId: ""
    };
    //Holds coordinates to draw route on map
    this.polyCoords = [];
  }
  //adds coordinates from markers to polyline array
  addPolyline = props => {
    this.polyCoords.push(props);
  };

  handleToggleOpen = id => {
    this.setState({
      openInfoWindowMarkerId: ""
    });
    this.setState({
      openInfoWindowMarkerId: id
    });
  };

  render() {
    let markers;
    if (this.state.markers !== null) {
      return this.state.markers.map(station => {
        //console.log(stationkeys[station]['name']);
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
            onClick={() => this.handleToggleOpen(station)}
          >
            {this.state.openInfoWindowMarkerId == station && (
              <InfoWindow
                onCloseClick={() =>
                  this.setState({ openInfoWindowMarkerId: "" })
                }
              >
                <div>
                  <span>{stationkeys[station]["name"]}</span>
                </div>
              </InfoWindow>
            )}{" "}
          </Marker>
        );
      });
    }
  }
}

export default MarkerContainer;
