import React, { Component } from "react";
import PropTypes from "prop-types";
import axios from "axios";

class DataProvider extends Component {
  static propTypes = {
    endpoint: PropTypes.string.isRequired,
    render: PropTypes.func.isRequired
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
        stopnumber: "2007",
        time: "14:00",
        date: "06-07-2019"
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
