import React, {Component} from 'react';
import AppViewFavourAndLogin from "./AppViewFavourAndLogin"
import {Link} from 'react-router-dom'
import '../Static/StyleSheet/HomePage.css'
// import backgroundImg from '../Static/img/img1.jpg'
//This Component is the HomePage of the mobile view port


class HomePage extends Component {

// Both are refresh page
// window.location=document.referrer
//    ,window.location.replace("./")




    render() {

   // ,window.location.replace("./")



        return (

            <div className='EntireBox HomePage container col-md-12  position-absolute '
                 id='EntireBox_HomePage'>

                <div className='row  WeatherWidget  '>
                    <div className='container WeatherWidget ' id='WeatherWidget'>
                        <a className="weatherwidget-io" href="https://forecast7.com/en/53d35n6d26/dublin/"
                           data-label_1="DUBLIN" data-label_2="WEATHER" data-mode="Current" data-days="3">DUBLIN
                            WEATHER</a>
                    </div>
                </div>
                <div className='container HomePageContains'>
                    <AppViewFavourAndLogin/>
                    <div className='container  '>
                        <div className='row '>
                            <Link to={'/SearchByStop'} className='LinkCss '>
                                <button type="button" className="btn btn-success" >Search By Stop
                                </button>
                            </Link>
                        </div>
                        <div className='row '>
                            <Link to={'/SearchByRoute'} className='LinkCss '>
                                <button type="button" className="btn btn-success" >Search By
                                    Route
                                </button>
                            </Link>
                        </div>
                        <div className='row'>
                            <Link to={'/SearchByDestination'} className='LinkCss'>
                                <button type="button" className="btn btn-success" >Search
                                    By Destination
                                </button>
                            </Link>
                        </div>


                    </div>

                </div>

            </div>

        );
    }
}

export default HomePage;
