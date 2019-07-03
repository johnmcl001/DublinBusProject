import React, {Component} from 'react';
import  '../static/frontend/stylesheet/AppViewFavourAndLogin.css';


class AppViewFavourAndLogin extends Component {
    render() {
        return (


                <div className="container"  id='appViewHeader'>
                    <div className="row" >
                        <div className="col-3 " id ='appViewLoginIcon' style={appViewLoginStyle}>
                            <a><i className="fa fa-user"></i></a>
                        </div>
                        <div className="col-6 ">

                        </div>
                        <div className="col-3 " >
                            <a style={favourPageStyle} id='favourPage'><i className="fa fa-heart"></i></a>
                        </div>
                    </div>
                </div>

        );
    }

}

const appViewLoginStyle={
       fontSize: '30px',

    margin:'auto',
}

const favourPageStyle={
  fontSize: '24px',
    //
    display: 'block',
    // margin:'auto',
    marginLeft:'30px',
    marginTop: '5px',
color:'red',
}


export default AppViewFavourAndLogin;
