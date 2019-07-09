import React from "react";
import key from "weak-key";
import "../Static/StyleSheet/ResultPage_Stop_Route.css";

const Table = props => {
  const { data } = props;

  return (
    <div>
      <table>
        <thead>
          <tr>
            {Object.entries(data[0]).map(elem => (
              <th key={key(elem)}>{elem[0]}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map(elem => (
            <tr key={elem.id}>
              {Object.entries(elem).map(elem => (
                <td key={key(elem)}>{elem[1]}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Table;
