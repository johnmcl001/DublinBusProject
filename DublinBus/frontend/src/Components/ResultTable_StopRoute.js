import React from "react";
import key from "weak-key";
import "../Static/StyleSheet/ResultPage_Stop_Route.css";

const ResultTable_StopRoute = props => {
  const { data } = props;

  console.log(data);

  return (
    <div>
    {console.log(data)}
      {props.data.map((x, y) => (
        //    Loop throught
        <div className="row resultRows">
          <div className="col-4 busNumber">
            <p key={y}>{x.instruction}</p>
          </div>
          <div className="col-6 busArrivalTime ">
            <p key={y}>{x.time}</p>
          </div>
        </div>
      ))}
    </div>
  );
};

export default ResultTable_StopRoute;
