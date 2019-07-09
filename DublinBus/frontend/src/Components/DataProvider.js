import React, { Component } from "react";
import PropTypes from "prop-types";
import axios from "axios";

class DataProvider extends Component {
  static propTypes = {
    render: PropTypes.func.isRequired,
    endpoint: PropTypes.string.isRequired,
    stopnumber: PropTypes.string,
    route: PropTypes.string,
    towards: PropTypes.string,
    departure: PropTypes.string,
    startpoint: PropTypes.string,
    destination: PropTypes.string,
    time: PropTypes.string,
    date: PropTypes.string
  };
  state = {
    data: [],
    loaded: false,
    placeholder: "Loading...",
    proxy: "http://localhost:8000/api/"
  };
  componentDidMount() {
    axios({
      method: "get",
      url: this.state.proxy + this.props.endpoint + "/",
      params: {
        stopnumber: this.props.stopnumber,
        route: this.props.route,
        towards: this.props.towards,
        departure: this.props.departure,
        startpoint: this.props.startpoint,
        destination: this.props.destination,
        time: this.props.time,
        date: this.props.date
      }
    })
      .then(response => {
        if (response.status !== 200) {
          return this.setState({ placeholder: "Something went wrong" });
        }
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
