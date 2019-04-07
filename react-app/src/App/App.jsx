import ReactGA from 'react-ga';
import React from 'react';
import { Router, Route } from 'react-router-dom';
import { connect } from 'react-redux';

import { history } from '../_helpers';
import { alertActions } from '../_actions';
import { PrivateRoute, Loader } from '../_components';
import { DashboardPage } from '../DashboardPage';
import { LoginPage } from '../LoginPage';
import { RegisterPage } from '../RegisterPage';
import { DefineInputPage } from '../DefineInputPage';
import { IndexPage } from '../IndexPage';
import { TrainingPage } from '../TrainingPage';
import { GraphPage } from '../GraphPage';
import { DatasetPage } from '../DatasetPage';
import { Header } from './Header';
import './app.css'
import { MuiThemeProvider, createMuiTheme } from '@material-ui/core/styles';
import { green, indigo } from '@material-ui/core/colors'
import {Alert} from '../_components';
import Snackbar from '@material-ui/core/Snackbar';

const theme = createMuiTheme({
    typography: {
        useNextVariants: true,
        fontSize: 12,
    },
    palette: {
        primary: {
            main: '#A5C05B',
            contrastText: '#fff',
        },
        secondary: {
            main: '#A01D26',
            contrastText: '#fff',
        },
        background: {
            default: '#303030',
            paper: "#FFFFFF"
        },
        // text:{
        //     primary: "#FFFFFF",
        //     secondary: "#FFFFFF",
        //     disabled: "#FFFFFF",
        //     hint: "#FFFFFF",
        // }
    },
});


/*
type:'dark'
*/
class App extends React.Component {
    constructor(props) {
        super(props);
        ReactGA.initialize('UA-74441880-6');

        this.state = {
            alert: false,
        };

        const { dispatch } = this.props;
        history.listen((location, action) => {
            // clear alert on location change
            dispatch(alertActions.clear());
        });
    }

    componentWillReceiveProps(nextProps) {
        let {alert} = this.props;

        if (alert != nextProps.alert) {
            if (nextProps.alert.message) this.setState({alert: true})
        }
    }


    render(){
        const { alert, loader } = this.props;
        return (
            <div>
                <MuiThemeProvider theme={theme}>
                    <Router history={history}>
                        <div>
                        <Header />
                         <div className="container">
                                    {/*alert.message &&
                                        <div className={`alert ${alert.type}`}>
                                            <a href="#" className="close" data-dismiss="alert" aria-label="close">×</a>
                                            {alert.message}
                                        </div>
                                    */}

                                     <Snackbar
                                         anchorOrigin={{
                                             vertical: 'bottom',
                                             horizontal: 'left',
                                         }}
                                         open={this.state.alert}
                                         autoHideDuration={6000}
                                         onClose={(e) => {this.setState({alert: false});this.props.dispatch(alertActions.clear());}}
                                     >
                                         { alert.message &&
                                             <Alert
                                                 onClose={(e) => {
                                                     this.setState({alert: false});
                                                     this.props.dispatch(alertActions.clear());
                                                 }}
                                                 variant={alert.type}
                                                 message={alert.message}
                                             />
                                         }
                                     </Snackbar>

                                    {loader.requesting && loader.global &&
                                        <div className="loader-container">
                                            <Loader/>
                                        </div>
                                    }
                                        <div>
                                            <PrivateRoute path="/dashboard/:id" component={DashboardPage} />
                                            <PrivateRoute path="/input/:id" component={DefineInputPage} />
                                            <Route exact path="/" component={LoginPage} />
                                            <Route path="/register" component={RegisterPage} />
                                            <Route path="/datasets" component={DatasetPage} />
                                            <PrivateRoute exact path="/dashboard" component={IndexPage} />
                                            <PrivateRoute path="/training/:id" component={TrainingPage} />
                                            <PrivateRoute path="/graph/:id" component={GraphPage} />
                                        </div>

                        </div>
                        </div>
                    </Router>
                </MuiThemeProvider>
            </div>
        );
    }
}

function mapStateToProps(state) {
    const { alert, loader } = state;
    return {
        alert,
        loader
    };
}

const connectedApp = connect(mapStateToProps)(App);
export { connectedApp as App }; 