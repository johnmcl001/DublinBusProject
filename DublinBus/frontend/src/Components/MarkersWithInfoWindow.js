import React, {Component} from 'react'; import { Marker, InfoWindow } from "react-google-maps";

class InfoWindowMap extends Component {

constructor(props){
    super(props);

    this.state = {
        isOpen: false
    }

}

handleToggleOpen = () => {

    this.setState({
        isOpen: true
    });
}

handleToggleClose = () => {
    this.setState({
        isOpen: false
    });
}
render() {

return (
        <Marker
            key={this.props[station]['name']}
            position={{ lat: this.props[station]['lat'], lng: this.props[station]['long']}}
            label={this.props[station]['name']}
            onClick={() => this.handleToggleOpen()}
        >

        {
            this.state.isOpen &&
         <InfoWindow onCloseClick={this.props.handleCloseCall}>
             <span>Something</span>
         </InfoWindow>
        }
        </Marker>

    )
} }

export default InfoWindowMap;
