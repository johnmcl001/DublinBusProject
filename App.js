import React, { Component } from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import { NavigationBar } from './components/NavigationBar';
import Results from './components/Results';
import './App.css';
import Map from './components/Map'

class App extends Component {
  render() {
  return (
    <React.Fragment>
      <Router>
        <NavigationBar />
        <Results />
        <Map />
      </Router>
    </React.Fragment>
  );
}
}
export default App;
