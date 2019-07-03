import React, {Component} from 'react';


class FavourPage extends Component {
    render() {
        return (
            <div  style={Box}>
               <a> <i className="fas fa-heart" style={favouriteIconStyle}></i></a>
            </div>
        );
    }

}

const favouriteIconStyle = {

fontSize: '2em',
margin: '1rem',
   padding:'-2em',
    color: 'red'}
const Box=
{

    marginLeft: '1em',
    padding:'1px !important'
}


export default FavourPage;
