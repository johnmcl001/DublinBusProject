import { createContext } from "react";

const MapContext = createContext({
  polyLine: [],
  updatePolyline: pl => {
    MapContext.polyLine = pl;
  }
});

export default MapContext;
