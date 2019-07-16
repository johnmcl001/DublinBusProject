import React from "react";
import key from "weak-key";
import "../Static/StyleSheet/ResultPage_Stop_Route.css";

const ResultTable_StopRoute = props => {
  const { data } = props;

  console.log(data);

  return (
    <div>
      {props.data.map((x, y) => (
        //    Loop throught
        <div className="row resultRows">
          <div className="col-4 busNumber">
            <p key={y}>{x.route}</p>
          </div>
          <div className="col-6 busArrivalTime ">
            <p key={y}>{x.arrival_time} mins</p>
          </div>
        </div>
      ))}
    </div>
  );
};

export default ResultTable_StopRoute;
