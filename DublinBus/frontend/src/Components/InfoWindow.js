import React, {Component} from 'react';
import {Marker, InfoWindow} from "react-google-maps";
import {connect} from 'react-redux';

class InfoWindowMap extends Component {

  constructor(props) {
    super(props);

    this.state = {
      openInfoWindowMarkerId: "",
    }

  }

  handleToggleOpen = (id) => {
    this.setState({openInfoWindowMarkerId: id});
  }


  render() {

  return (

	      <Marker key={this.props.index} position={{
	          lat: this.props.lat,
	          lng: this.props.lng
	        }} name={this.props.name}
					onClick={() => this.handleToggleOpen(this.props.index)}
					>

	        {(this.state.openInfoWindowMarkerId==this.props.index)&&

						<InfoWindow
            onCloseClick={() => this.setState({openInfoWindowMarkerId: ""})}
            >
	              <div>
	                 <span>{this.props.name} {this.props.index}</span>
	              </div>
	            </InfoWindow>

	        }

	      </Marker>


	)
  }
}

export default (InfoWindowMap);
