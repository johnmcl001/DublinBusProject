import React, {Component} from 'react';
import '../static/frontend/stylesheet/AppViewHeader.css'

class AppViewHeader extends Component {
    render() {
        return (

            <div className='container AppViewHeader'>

                <div className="row ">

                    <div className="col-2">
                        <a id='returnButton'><i className="fas fa-arrow-left"></i></a>
                    </div>

                    <div className="col-8 border border-danger ">

                        <h5>Search By Stop Number </h5>
                    </div>

                    <div className="col-2 border border-danger position-relative ">
                        {/*// <!--Navbar-->*/}
                        <nav className="navbar navbar-light light-blue lighten-4 ">


                            {/*// <!-- Collapse button -->*/}
                            <button className="navbar-toggler toggler-example d-block d-sm-none" type="button"
                                    data-toggle="collapse"
                                    data-target="#navbarSupportedContent1"
                                    aria-controls="navbarSupportedContent1" aria-expanded="false"
                                    aria-label="Toggle navigation"><span class="dark-blue-text"><i
                                class="fas fa-bars fa-1x"></i></span></button>

                            {/*// <!-- Dropdown Contents-->*/}
                            <div className="collapse navbar-collapse dropdown-menu dropdown-menu-right"
                                 id="navbarSupportedContent1">

                                {/*// <!-- Links -->*/}
                                <a className="dropdown-item  " href="#">Action</a>
                                <a className="dropdown-item" href="#">Another action</a>
                                <a className="dropdown-item" href="#">Something else here</a>
                                <div className="dropdown-divider"></div>
                                <a className="dropdown-item" href="#">Separated link</a>
                                {/*// <!-- Links -->*/}

                            </div>
                            {/*https://codedaily.io/tutorials/63/Create-a-Dropdown-in-React-that-Closes-When-the-Body-is-Clicked*/}
                        </nav>




                </div>
            </div>
            </div>
        );
    }

}


export default AppViewHeader;
