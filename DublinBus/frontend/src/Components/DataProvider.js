import React, { Component } from "react";
import PropTypes from "prop-types";
import axios from "axios";
import decodePolyline from "decode-google-map-polyline";
import loading from "../Static/img/loading.gif"

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
    placeholder: <img
                  src={loading}
                  alt="loading..."
                  width="120"
                  height="120"
                  />,
    proxy: "http://localhost:8000/api/"
  };

    componentDidMount() {
        console.log(this.props)
    axios({
      method: "get",
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
        home:this.props.home
      }
    })
      .then(response => {
        /*
        let polyline = [];
        let arr = [];
        console.log(response.data)
        for (var i = 0; i < response.data.polylines.length; i++) {
          arr = decodePolyline(response.data.polylines[i]);
          console.log(arr);
          for (var j = 0; j < arr.length; j++) {
            polyline.push(arr[j]);
          }
        }
        this.props.updateMap(polyline, response.data.markers);
        */
        if (response.status !== 200) {
          return this.setState({ placeholder: "Something went wrong" });
        }
          console.log(response.data)
        return response.data;
      })
      .then(data => this.setState({ data: data, loaded: true }));
  }
  render() {
    const { data, loaded, placeholder } = this.state;
    return loaded ? this.props.render(data) : <p>{placeholder}</p>;
  }
}
export default DataProvider;
