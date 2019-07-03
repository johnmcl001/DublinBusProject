import React, {Component} from 'react';
import Header from "./Components/Header"
import Footer from "./Components/Footer"
import Map from './Components/Map'
import SearchByStop from './Components/SearchByStop'
import SearchbyDestination from './Components/SearchbyDestination'
import SearchByRoute from './Components/SearchByRoute'
class App extends Component {
    render() {
        return (
            <div className="App">
                <Header/>
                <div className='container-fluid position-relative'>


                    <Map/>
                    <SearchbyDestination/>
                    {/*<SearchByRoute/>*/}
                    {/*<SearchByStop/>*/}
                    {/*<AppView/>*/}

                </div>
                <Footer/>
            </div>
        );
    }

}

// const x = {
//     position: 'relative'
// }
export default App;
