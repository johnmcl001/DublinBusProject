import React, {Component} from 'react';
import ReactDOM from "react-dom";
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
