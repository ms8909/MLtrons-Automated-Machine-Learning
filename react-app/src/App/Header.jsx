import ReactGA from 'react-ga';
import React, { Component } from 'react';
import { connect } from 'react-redux';
import { withStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
import IconButton from '@material-ui/core/IconButton';
import MenuIcon from '@material-ui/icons/Menu';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import { Link, withRouter } from 'react-router-dom';
import Grid from '@material-ui/core/Grid';

import logo from '../images/logo.png';

const styles = theme => ({
    appBar: {
        position: 'relative',
        backgroundColor: '#000',
        color: '#fff',
        '& > div':{
            minHeight: '48px'
        }
    },
    root: {
        flexGrow: 1,
    },
    inline: {
        display: 'inline'
    },
    flex: {
        display: 'flex',
        justifyContent: 'space-between',
        [theme.breakpoints.down('sm')]: {
            display: 'flex',
            justifyContent: 'space-evenly',
            alignItems: 'center'
        }
    },
    link: {
        textDecoration: 'none',
        color: 'inherit',
        position: 'absolute',
        top: '0'
    },
    tabContainer: {
        marginLeft: '150px',
        [theme.breakpoints.down('sm')]: {
            // display: 'none'
            marginLeft: '0',
        }
    },
    logoContainer: {
        [theme.breakpoints.down('sm')]: {
            display: 'none'
        }
    },
    tabItem: {
        paddingTop: 10,
        paddingBottom: 10,
        minWidth: 'auto',
        color: '#FFF',
    },
    btn_light: {
        color: '#FFF'
    }
});

const defaultProps = {};


class Header extends Component {
    constructor(props) {
        super(props);
        this.state = {
            value: 0,
            menuDrawer: false
        };
        this.handleChange = this.handleChange.bind(this);
        this.current = this.current.bind(this);
    }

    handleChange(event, value){
        this.setState({ value });
    };

    componentDidUpdate(prevProps) {
        if (this.props.location !== prevProps.location) {
            console.log('route updated here', this.props.location.pathname);
            ReactGA.pageview(this.props.location.pathname);
        }
    }

    componentDidMount() {
        window.scrollTo(0, 0);
    }

    current(){
        if(this.props.location.pathname == '/dashboard') {
            return 0
        }
        if(this.props.location.pathname == '/datasets') {
            return 1
        }
    }

    render() {

    const { authentication, classes } = this.props;

    const isLoggedIn = authentication && authentication.loggedIn;

    let button;

    if (isLoggedIn) {
        button = <Link to='/'><Button className={classes.btn_light}>Logout</Button></Link>;
    } else {
        button = <Link to='/'><Button className={classes.btn_light}>Login</Button></Link>;
    }

    const menu = [
        {
            label: "Dashboard",
            pathname: "/dashboard"
        },
        {
            label: "Datasets",
            pathname: "/datasets"
        },

    ];

    console.log('props test here', this.props);

    return (
        <div className={classes.root}>
            {isLoggedIn &&
            <AppBar position="static" className={classes.appBar}>
                <Toolbar>
                    <Grid container spacing={24} alignItems="baseline">
                        <Grid item xs={12} alignItems='baseline' className={classes.flex}>
                            <div>
                                <Typography variant="h6" color="inherit" className={classes.logoContainer}>
                                    <Link to='/dashboard' className={classes.link}>
                                        <img width={100} src={logo} alt="logo"/>
                                    </Link>
                                </Typography>
                                {isLoggedIn &&
                                <div className={classes.tabContainer}>
                                    <Tabs
                                        value={this.current()}
                                        indicatorColor="primary"
                                        textColor="primary"
                                        onChange={this.handleChange}>
                                        {menu.map((item, index) => (
                                            <Tab key={index} component={Link}
                                                 to={{pathname: item.pathname, search: this.props.location.search}}
                                                 classes={{root: classes.tabItem}} label={item.label}/>
                                        ))}
                                    </Tabs>
                                </div>
                                }
                            </div>
                            {button}
                        </Grid>
                    </Grid>
                </Toolbar>
            </AppBar>
            }
        </div>
    );
  }
}

/*
<React.Fragment>
    <nav className="navbar navbar-inverse">
        <div className="container-fluid">
            <div className="navbar-header">
                <a className="navbar-brand" href="/">Mltrons</a>
            </div>
            <ul className="nav navbar-nav navbar-right">
                {button}
            </ul>
        </div>
    </nav>
</React.Fragment>
*/

function mapStateToProps(state) {
    const { authentication } = state;
    return {
        authentication
    };
}

const connectedHeader = withRouter(withStyles(styles)(connect(mapStateToProps)(Header)));
export { connectedHeader as Header };
