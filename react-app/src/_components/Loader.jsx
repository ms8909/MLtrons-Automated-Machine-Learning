import React, { Component } from 'react';
import './loader.css'
const defaultProps = {};

class Loader extends Component {
    constructor(props) {
        super(props);
    }

    render() {

    return (
      <React.Fragment>

          <div className="lds-css ng-scope">
              <div style={{width:'100%',height:'100%'}} className="lds-ripple">
                  <div></div>
                  <div></div>
              </div>
          </div>
      </React.Fragment>
    );
  }
}

export { Loader };
