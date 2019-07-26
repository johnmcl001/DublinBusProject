
import React from "react";
import Map from "./Map";
import "../Static/StyleSheet/MobileMap.css";

class mobileMap extends React.Component {
  render() {
    return (
      <div className="container col-12 position-relative ">
        <Map />

        {/*<div className="slideShowMapFooter">*/}

        {/*</div>*/}
      </div>
    );
  }
}

export default mobileMap;
