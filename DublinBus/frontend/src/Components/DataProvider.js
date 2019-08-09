import React, {Component} from "react";
import PropTypes from "prop-types";
import axios from "axios";
import decodePolyline from "decode-google-map-polyline";
import loading from "../Static/img/loading.gif";

const imgStyle = {
    leftMargin: "auto",
    rightMargin: "auto"
};

class DataProvider extends Component {
    static propTypes = {
        render: PropTypes.func.isRequired,
        endpoint: PropTypes.string.isRequired,
        stopnumber: PropTypes.string,
        route: PropTypes.string,
        towards: PropTypes.string,
        destinationLat: PropTypes.string,
        destinationLon: PropTypes.string,
        startLat: PropTypes.string,
        startLon: PropTypes.string,
        destination: PropTypes.string,
        time: PropTypes.string,
        date: PropTypes.string,
        attractions: PropTypes.string,
        home: PropTypes.string
    };
    state = {
        data: [],
        loaded: false,
        placeholder: (
            <img src={loading} alt="loading..." width="120" height="120"/>
        ),
        proxy: "http://localhost:8000/api/"
    };

    componentDidMount() {
        axios({
            method: "get",
            // url: "http://csi420-01-vm9.ucd.ie/api/" + this.props.endpoint + "/",

            url: "http://localhost:8000/api/" + this.props.endpoint + "/",
            params: {
                stopnumber: this.props.stopnumber,
                route: this.props.route,
                towards: this.props.towards,
                destinationLat: this.props.destinationLat,
                destinationLon: this.props.destinationLon,
                startLat: this.props.startLat,
                startLon: this.props.startLon,
                time: this.props.time,
                date: this.props.date,
                attractions: this.props.attractions,
                home: this.props.home
            }
        })
            .then(response => {
                if (response.data.length == 0) {
                    console.log("empty array");
                    this.setState({placeholder: "No routes possible at this time"});
                    return;
                } else {
                    this.props.updateMap(response.data);
                    console.log("yy");
                    this.setState({data: response.data, loaded: true});
                    return;
                }
            })
            .catch(error => {
                if (error.response) {
                    this.setState({placeholder: "No routes possible at this time"});
                } else if (error.request) {
                    this.setState({placeholder: "Server down, try again later"});
                }
            });
    }

    render() {
        const {data, loaded, placeholder} = this.state;
        return loaded ? this.props.render(data) : <p>{placeholder}</p>;
    }
}

export default DataProvider;
