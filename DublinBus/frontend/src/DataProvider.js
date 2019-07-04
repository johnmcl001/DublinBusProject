import React, { Component } from "react";
import PropTypes from "prop-types";
class DataProvider extends Component {
  static propTypes = {
    endpoint: PropTypes.string.isRequired,
    render: PropTypes.func.isRequired
  };
  state = {
    data: [],
    loaded: false,
    placeholder: "Loading..."
  };
  componentDidMount() {
<<<<<<< HEAD
    fetch(this.props.endpoint)
=======
    axios({
      method: "get",
      url: this.props.endpoint
    })
>>>>>>> Frontend stuff integrated with django for the most part, missing an img, not functional
      .then(response => {
        if (response.status !== 200) {
          return this.setState({ placeholder: "Something went wrong" });
        }
        return response.json();
      })
      .then(data => this.setState({ data: data, loaded: true }));
  }
  render() {
    const { data, loaded, placeholder } = this.state;
    return loaded ? this.props.render(data) : <p>{placeholder}</p>;
  }
}
export default DataProvider;
