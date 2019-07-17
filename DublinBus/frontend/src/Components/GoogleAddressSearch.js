import React from "react";

//npm install --save react-google-maps
// import LocationSearchInput from "./GoogleAutoComplete";

const { compose, withProps, lifecycle } = require("recompose");
const {
  StandaloneSearchBox
} = require("react-google-maps/lib/components/places/StandaloneSearchBox");

const PlacesWithStandaloneSearchBox = compose(
  withProps({
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
)(props => (
  <div data-standalone-searchbox="">
    <StandaloneSearchBox
      ref={props.onSearchBoxMounted}
      bounds={props.bounds}
      onPlacesChanged={props.onPlacesChanged}
    >
      <input type="text" placeholder={props.comment} />
    </StandaloneSearchBox>
  </div>
));

export default PlacesWithStandaloneSearchBox;
