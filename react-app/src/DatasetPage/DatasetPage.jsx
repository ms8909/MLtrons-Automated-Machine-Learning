import React from 'react';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';
import './index.css';
import Paper from '@material-ui/core/Paper';
import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid';
import Button from '@material-ui/core/Button';
import Avatar from '@material-ui/core/Avatar';
import {projectActions, userActions, loaderActions} from '../_actions';
import withStyles from '@material-ui/core/styles/withStyles';
import { withRouter } from "react-router";
import ExpansionPanel from '@material-ui/core/ExpansionPanel';
import ExpansionPanelDetails from '@material-ui/core/ExpansionPanelDetails';
import ExpansionPanelSummary from '@material-ui/core/ExpansionPanelSummary';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import Collapse from '@material-ui/core/Collapse';


const styles = theme => ({
    root: {
        flexGrow: 1,
        backgroundColor: theme.palette.grey['100'],
        paddingBottom: 200,
        paddingTop: 50,
        minHeight: '70vh'
    },
    heading: {
        fontSize: theme.typography.pxToRem(15),
        flexBasis: '33.33%',
        flexShrink: 0,
    },
    secondaryHeading: {
        fontSize: theme.typography.pxToRem(15),
        color: theme.palette.text.secondary,
    },
    grid: {
        width: 1200,
        justifyContent: 'start',
        margin: `0 ${theme.spacing.unit * 2}px`,
        [theme.breakpoints.down('sm')]: {
            width: 'calc(100% - 20px)'
        }
    },
    loadingState: {
        opacity: 0.05
    },
    paper: {
        padding: theme.spacing.unit * 3,
        textAlign: 'left',
        color: theme.palette.text.secondary
    },
    topBar: {
        marginTop: 50,
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center'
    },
    outlinedButtom: {
        textTransform: 'uppercase',
        margin: theme.spacing.unit
    },
    media: {
        height: 0,
        paddingTop: '56.25%', // 16:9
    },
    card: {
        maxWidth: '100%',
    },
    cardButton: {
        display: 'flex',
        justifyContent: 'start',
        width: '100%'
    },
    explore: {
        display: 'flex',
        flexDirection: 'row',
        alignItems: 'center'
    },
    error: {
        color: theme.palette.error.main
    },
    avatar: {
        backgroundColor: theme.palette.primary.main
    },
    dashboard:{
        padding: '25px'
    },
    expansionDetail: {
        padding: 0,
    },
    expansionList:{
        width: '100%'
    },
    nested: {
        paddingLeft: theme.spacing.unit * 5,
    },
    innerGrid: {
        padding: '10px 0'
    },
    expansion: {
        width: '100%',
        '&::before': {
            top: 0
        }
    },

});

class DatasetPage extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            expanded: null,
        };
        this.handleChange=this.handleChange.bind(this);
    }

    componentDidMount() {
        this.props.dispatch(projectActions.getProjects());
    }

    handleChange(expanded){
        console.log('on change', expanded);
        // this.setState({
        //     expanded: expanded,
        // });
    }

    render() {
        const { groups, classes  } = this.props;
        const { expanded } = this.state;
        return (
            <div className={classes.root}>
                <Grid container justify="center">
                    <Grid spacing={24} alignItems="start" justify="center" container className={classes.grid}>
                        <div className={classes.topBar}>
                            <div className={classes.block}>
                                <Typography variant="h6" gutterBottom>Datasets</Typography>
                            </div>
                        </div>
                        {   groups.projects && groups.projects.map((obj) =>
                                <ExpansionPanel className={classes.expansion}>
                                    <ExpansionPanelSummary expandIcon={<ExpandMoreIcon/>}>
                                        <Typography className={classes.heading}>{obj.name}</Typography>
                                    </ExpansionPanelSummary>
                                    <ExpansionPanelDetails>
                                        <List component="div" disablePadding className={classes.expansionList}>
                                            {obj.datasets.map((inner) =>
                                                <React.Fragment key={obj.id}>
                                                    <ListItem
                                                        button
                                                        className={classes.nested}
                                                        selected={this.state.selected == inner.id}
                                                        onClick={event => this.setState({selected: inner.id})}
                                                    >
                                                        <ListItemText primary={inner.name}/>
                                                    </ListItem>
                                                    <Collapse in={this.state.selected == inner.id} timeout="auto" unmountOnExit>
                                                        <Grid container justify="center" className={classes.innerGrid}>
                                                            <Grid xs={4}>
                                                                <Typography variant="subtitle2" gutterBottom>Dataset name</Typography>
                                                                <Typography variant="body2" gutterBottom>{inner.name}</Typography>
                                                            </Grid>
                                                            <Grid xs={4}>
                                                                <Typography variant="subtitle2" gutterBottom>No of rows</Typography>
                                                                <Typography variant="body2" gutterBottom>{inner.rows}</Typography>
                                                            </Grid>
                                                            <Grid xs={4}>
                                                                <Typography variant="subtitle2" gutterBottom>No of columns</Typography>
                                                                <Typography variant="body2" gutterBottom>{inner.columns}</Typography>
                                                            </Grid>
                                                        </Grid>
                                                    </Collapse>
                                                </React.Fragment>
                                            )}
                                        </List>
                                    </ExpansionPanelDetails>
                                </ExpansionPanel>)
                        }
                    </Grid>
                </Grid>
            </div>

        );
    }
}

function mapStateToProps(state) {
    const { groups } = state;
    return {
        groups
    };
}

const connectedHomePage = withRouter(withStyles(styles)(connect(mapStateToProps)(DatasetPage)));
export { connectedHomePage as DatasetPage };