import React from "react";
import key from "weak-key";
import "../Static/StyleSheet/ResultPage_Stop_Route.css";

const ResultTable_StopRoute = props => {
    const {data} = props;

    console.log(data)

    return (
        <div>
            { data.map(x =>
            //    Loop throught
            <div className="row resultRows"  >

                <div className="col-4 busNumber">
                    <p>{x.route}</p>
                </div>
                <div className="col-6 busArrivalTime ">
                    <p>{x.arrival_time} mins</p>
                </div>
            </div>
            )}
        </div>

    );
};

export default ResultTable_StopRoute;
