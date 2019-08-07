import React from "react";
import GoogleAddressSearch from "./GoogleAddressSearch";
import "../Static/StyleSheet/YourLocationOrSearch.css";

import { FaCrosshairs, FaSearchLocation } from "react-icons/fa";

class YourLocationOrSearch extends React.Component {
  constructor(props) {
    super(props);
    this.state = { inputText: "From Your Current Location" };
  }

  renderInputField() {
    if (this.props.useuseSearchLocation_State == true) {
      return (
        <div>
          <GoogleAddressSearch
            comment="Set Your Start Point"
            onUpdatePosition={this.props.onUpdatePosition}
            id={this.props.id}
          />
        </div>
      );
    } else {
      return (
        <input
          id="InputBoxYourLocationOrSearch"
          value={this.state.inputText}
          disabled
        />
      );
    }
  }

  renderButton() {
    let button;

    if (this.props.useuseSearchLocation_State == true) {
      button = (
        <div>
          <a onClick={this.props.useCurrentLocation}>
            <FaCrosshairs className="icon" />
          </a>
        </div>
      );
    } else {
      button = (
        <a onClick={this.props.useSearchLocation}>
          <FaSearchLocation className="icon" />
        </a>
      );
    }

    return button;
  }

  render() {
    return (
      <div YourLocationOrSearch className="row">
        <div className="col-10 ">{this.renderInputField()}</div>
        <div className="col-2  ClickChangeInput">{this.renderButton()}</div>
      </div>
    );
  }
}

export default YourLocationOrSearch;
