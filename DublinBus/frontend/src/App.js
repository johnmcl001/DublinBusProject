import React, {Component} from 'react';
import ReactDOM from "react-dom";
<<<<<<< HEAD
import DataProvider from "./DataProvider";
import Table from "./Table";
const App = () => (
  <DataProvider endpoint="api/stop/" render={data => <Table data={data} />} />
);
const wrapper = document.getElementById("app");
wrapper ? ReactDOM.render(<App />, wrapper) : null;
=======
import Header from "./Components/Header"
import Footer from "./Components/Footer"
import Map from './Components/Map'
import SearchByStop from './Components/SearchByStop'
import SearchbyDestination from './Components/SearchbyDestination'
import SearchByRoute from './Components/SearchByRoute'

 const App = () => {
        return (
            <div className="App">
                <Header/>
                <div className='container-fluid position-relative'>


                    <Map/>
                    {/*<SearchbyDestination/>*/}
                    {/*<SearchByRoute/>*/}
                    <SearchByStop/>
                    {/*<AppView/>*/}

                </div>
                <Footer/>
            </div>
        );

}

// const x = {
//     position: 'relative'
// }
ReactDOM.render(<App />, document.getElementById("app"));
>>>>>>> Frontend stuff integrated with django for the most part, missing an img, not functional
