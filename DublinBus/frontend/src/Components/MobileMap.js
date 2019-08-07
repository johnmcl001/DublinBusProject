import React from "react";
import Map from "./Map";

class mobileMap extends React.Component {
  render() {
    return (
      <div className="container col-12 position-relative ">
        <Map markers={this.props.markers} polyline={this.props.polyline}/>

        {/*<div className="slideShowMapFooter">*/}

        {/*</div>*/}
      </div>
    );
  }
}

export default mobileMap;
