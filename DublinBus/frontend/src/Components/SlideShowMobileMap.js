import React, { Component } from "react";
import SlidingPane from "react-sliding-pane";
import "react-sliding-pane/dist/react-sliding-pane.css";
import "../Static/StyleSheet/SlideShowMobileMap.css";
import MobileMap from "./MobileMap";

//This the Submit button for the Result page of the Search by Destination
class ButtonAtResultPage extends Component {
  constructor(props) {
    super(props);
    this.state = {
      isPaneOpen: false,
      isPaneOpenLeft: false
    };
  }

  render() {
    return (
      <div className="row container ShowMapAndFare position-relative ">
        <div className="col-12 d-none d-md-block">
          <button className=" btn btn-warning " style={{ width: "150px" }}>
            € Show Fare
          </button>
        </div>
        <div className="col-6 d-md-none">
          <button className=" btn btn-warning ">Show Fare</button>
        </div>
        <div className="col-6 d-md-none">
          <button
            className="btn btn-warning "
            onClick={() => this.setState({ isPaneOpenLeft: true })}
          >
            Show Map
          </button>
        </div>
        <SlidingPane
          className="d-md-none"
          closeIcon={
            <a>
              <i className="fas fa-arrow-left"></i>
            </a>
          }
          isOpen={this.state.isPaneOpenLeft}
          title="To Destination name"
          from="right"
          width="100%"
          onRequestClose={() => this.setState({ isPaneOpenLeft: false })}
        >
          <MobileMap markers={this.props.markers} polyline={this.props.polyline}/>
        </SlidingPane>
      </div>
    );
  }
}

export default ButtonAtResultPage;
