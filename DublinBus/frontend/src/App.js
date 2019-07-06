import React from "react";
import ReactDOM from "react-dom";
import DataProvider from "./Components/DataProvider";
import Table from "./Components/Table";

const App = () => (
  <DataProvider endpoint="stop" render={data => <Table data={data} />} />
);
const wrapper = document.getElementById("root");
wrapper ? ReactDOM.render(<App />, wrapper) : null;
