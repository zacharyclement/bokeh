import React, { Component } from 'react';
import './App.css';
import CongressionalDistricts from './components/CongressionalDistricts';
import Test from './components/Test';
import Scatter from './components/Scatter';
import Line from './components/Line';
import Sunburst from './components/Sunburst';

class App extends Component {
  render() {
    return (
      <div className="App">

        <p className="App-intro">
          D3 visualization examples
        </p>

        <div id='sunburst'>
          <Sunburst />
        </div>

        <svg width="960" height="600">
          <Line />
        </svg>

        <div id='scatter'>
          <Scatter />
        </div>

        <svg width="960" height="600">
          <CongressionalDistricts width={960} height={600} />
        </svg>

        <svg width="960" height="600">
          {/* <Test width={960} height={600} /> */}
        </svg>


      </div>
    );
  }
}

export default App;
