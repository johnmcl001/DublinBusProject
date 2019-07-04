import React, { Component } from 'react';
import Result from './Result';

class Results extends Component {
    render() {
        return (
            <div >
                <h1>Search by route</h1>
                <h3>Stop number 1947</h3>
                <Result Bus="39A" Arrival="5 minutes" />
                <Result Bus="46A" Arrival="7 minutes" />
                <Result Bus="145" Arrival="8 minutes" />
                <Result Bus="155" Arrival="8 minutes" />
                <Result Bus="46A" Arrival="10 minutes" />
            </div>
        )
    }
}
    

    

export default Results;