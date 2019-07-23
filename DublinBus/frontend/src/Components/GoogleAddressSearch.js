import React from "react";

//npm install --save react-google-maps
// import LocationSearchInput from "./GoogleAutoComplete";

const { compose, withProps, lifecycle } = require("recompose");
const { withScriptjs } = require("react-google-maps");
const {
  StandaloneSearchBox
} = require("react-google-maps/lib/components/places/StandaloneSearchBox");

const PlacesWithStandaloneSearchBox = compose(
  withProps({
    googleMapURL:
      "https://maps.googleapis.com/maps/api/js?key=AIzaSyDBnVde8R4LpYQapr6-zbAHPD5Xcva9H_c&v=3.exp&libraries=geometry,drawing,places",
    loadingElement: <div style={{ height: `100%` }} />,
    containerElement: <div style={{ height: `400px` }} />
  }),
  lifecycle({
    componentWillMount() {
      const refs = {};

      this.setState({
        places: [],
        onSearchBoxMounted: ref => {
          refs.searchBox = ref;
        },
        onPlacesChanged: () => {
          const places = refs.searchBox.getPlaces();

          this.setState({
            places
          });

          //pass geolocation via lat & long back to Search by Destination
          this.props.onUpdatePosition({
            latitude: this.state.places[0].geometry.location.lat(),
            longitude: this.state.places[0].geometry.location.lng()
          });
        }
      });
    }
  }),
  withScriptjs
)(props => (
  <div data-standalone-searchbox="">
    <StandaloneSearchBox
      ref={props.onSearchBoxMounted}
      bounds={props.bounds}
      onPlacesChanged={props.onPlacesChanged}
    >
      <input type="text" placeholder={props.comment} style={style}/>
    </StandaloneSearchBox>
  </div>
));

const style={
    width:'220px'
}
export default PlacesWithStandaloneSearchBox;
