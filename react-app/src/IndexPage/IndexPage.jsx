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
import * as Yup from "yup";
import {ErrorMessage, Field, Form, Formik} from "formik";
import withStyles from '@material-ui/core/styles/withStyles';
import Card from '@material-ui/core/Card';
import CardHeader from '@material-ui/core/CardHeader';
import CardMedia from '@material-ui/core/CardMedia';
import CardContent from '@material-ui/core/CardContent';
import DoneIcon from '@material-ui/icons/Done';
import IconButton from '@material-ui/core/IconButton';
import MoreVertIcon from '@material-ui/icons/MoreVert';
import ArrowForwardIcon from '@material-ui/icons/ArrowForward';
import dashboard from '../images/dashboard.png';
import ButtonBase from "@material-ui/core/ButtonBase";
import CardActionArea from '@material-ui/core/CardActionArea';
import { withRouter } from "react-router";
import PopupState, { bindTrigger, bindMenu } from 'material-ui-popup-state/index';
import Menu from '@material-ui/core/Menu';
import MenuItem from '@material-ui/core/MenuItem';
import TextField from '@material-ui/core/TextField';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';
import FormHelperText from '@material-ui/core/FormHelperText';

const styles = theme => ({
    root: {
        flexGrow: 1,
        backgroundColor: theme.palette.grey['100'],
        paddingBottom: 200,
        minHeight: '100vh'
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
        marginRight: '18px'
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
        backgroundColor: theme.palette.primary.main,
        color: '#FFF'
    },
    dashboard:{
        // padding: '12px 40px 60px 12px !important'
        padding: '30px !important'
    },
    block:{
        paddingLeft: '18px'
    },
    dashboardDialog: {
        '& > div':{
            '& > div':{
                height: '225px',
                width: '225px'
            }
        }
    },
});

class IndexPage extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            open: false,
            delete: false
        };
    }

    componentDidMount() {
        this.props.dispatch(projectActions.getProjects());
    }

    removeProject(event, id) {
        this.setState({
            delete: true,
            delete_id: id,
        })
    }

    remove(){
        this.props.dispatch(projectActions.deleteProject(this.state.delete_id));
        this.setState({delete: false})
    }


    render() {
        const projectValidationSchema = Yup.object().shape({
            project_name: Yup.string()
                .required('Project name is required'),
        });

        const form = <Formik
            initialValues={{ project_name: '' }}
            validationSchema={projectValidationSchema}
            onSubmit={(values, { setSubmitting }) => {
                var request = {
                    'name': values.project_name
                }
                this.props.dispatch(projectActions.addProject(request));
                this.setState({
                    open: false
                });
                setSubmitting(false);

            }}
        >
            {({ isSubmitting, values, errors, touched, handleChange}) => (
                <Form>

                    <DialogContent>
                        <TextField
                            autoFocus
                            margin="dense"
                            name="project_name"
                            label="Project name"
                            type="text"
                            fullWidth
                            onChange={handleChange}
                            value={values.project_name}
                        />
                        {errors.project_name && touched.project_name &&
                            <FormHelperText className={classes.error}>{errors.project_name}</FormHelperText>
                        }
                    </DialogContent>
                    <DialogActions>
                        <Button onClick={()=> (this.setState({ open: false }))} color="primary">
                            Cancel
                        </Button>
                        <Button type="submit" className="btn btn-dark" disabled={isSubmitting} color="primary">
                            Save
                        </Button>
                    </DialogActions>



                    {/*

                    <div className="modal-header">
                        <h4 className="modal-title" id="addProjectModalLabel">Add new project</h4>
                    </div>
                    <div className="form-group form-container">
                        <label htmlFor="first_name">Project name</label>
                        <Field type="text" className="form-control" name="project_name" />
                        <ErrorMessage name="project_name" className="help-block" component="div" />
                    </div>
                    <div className="modal-footer">
                        <button type="button" className="btn btn-secondary" data-dismiss="modal">Close
                        </button>
                        <button type="submit" className="btn btn-dark" disabled={isSubmitting}><i className="ti-save"></i> Save
                        </button>
                    </div>*/}
                </Form>
            )}
        </Formik>;

        const { groups, classes  } = this.props;

        const dashboards = groups.projects && groups.projects.map((obj) =>

            <Grid item xs={12} md={4} key={obj.id} className={classes.dashboard}>
                <Card className={classes.card}>
                    <CardHeader
                        avatar={
                            <Avatar aria-label="Status" className={classes.avatar}>
                                <DoneIcon />
                            </Avatar>
                        }
                        action={
                            <PopupState variant="popover" popupId="demo-popup-menu">
                                {popupState => (
                                    <React.Fragment>
                                        <IconButton  {...bindTrigger(popupState)}>
                                            <MoreVertIcon />
                                        </IconButton>
                                        <Menu {...bindMenu(popupState)}>
                                            <MenuItem onClick={(e)=>{this.removeProject(e, obj.id); popupState.close()}}>Delete</MenuItem>
                                        </Menu>
                                    </React.Fragment>
                                )}
                            </PopupState>
                        }
                        title={obj.name}
                        subheader={"Last modified: " + new Date(obj.updated_at)}
                    />
                    <CardActionArea onClick={(e)=> {this.props.history.push(obj.status=='Pending' ? '/dashboard/'+obj.id: obj.status=='Deployed' ? '/graph/'+obj.id: '/training/'+obj.id)}}>
                        <CardMedia
                            className={classes.media}
                            image={dashboard}
                            title="Go to detail"
                        />
                    </CardActionArea>
                </Card>
            </Grid>
        );

/*
        <div className="col-sm-4 col-md-3" key={obj.id}>
            <Link to={obj.status=='Pending' ? '/dashboard/'+obj.id: '/graph/'+obj.id}>
                <div className="group-container">
                    <a onClick={(e)=>this.removeProject(e, obj.id)} style={{'color': 'red', 'float': 'right'}}><i className="fa fa-trash"></i></a>
                    <h3>{obj.name}</h3>
                    <img style={{width: '100%', height: '100%'}} src="https://cdn0.iconfinder.com/data/icons/business-charts-and-diagrams-8/64/Business_graph-chart-dashboard-percentage-pie_chart_1-512.png"/>
                </div>
            </Link>
        </div>
*/

        return (
            <React.Fragment>

                <div className={classes.root}>
                    <Grid container justify="center">
                        <Grid spacing={24} alignItems="center" justify="center" container className={classes.grid}>
                            <Grid item xs={12}>
                                <div className={classes.topBar}>
                                    <div className={classes.block}>
                                        <Typography variant="h6" gutterBottom>Dashboard</Typography>
                                        {/*<Typography variant="body2">*/}
                                            {/*Manage your training dashboards*/}
                                        {/*</Typography>*/}
                                    </div>
                                    <div>
                                        <Button onClick={()=> (this.setState({ open: true }))} variant="outlined" className={classes.outlinedButtom}>
                                            Add Dashboard
                                        </Button>
                                    </div>
                                </div>
                            </Grid>

                            {dashboards}

                        </Grid>
                    </Grid>


                    <Dialog
                        open={this.state.delete}
                        onClose={()=> (this.setState({ delete: false }))}
                        aria-labelledby="alert-dialog-title"
                        aria-describedby="alert-dialog-description"
                    >
                        <DialogTitle id="alert-dialog-title">{"Delete project"}</DialogTitle>
                        <DialogContent>
                            <DialogContentText id="alert-dialog-description">
                                Are you sure you want to delete project dashboard?
                            </DialogContentText>
                        </DialogContent>
                        <DialogActions>
                            <Button onClick={()=> {this.setState({delete: false})}} color="primary">
                                Disagree
                            </Button>
                            <Button onClick={() => this.remove()} color="primary" autoFocus>
                                Agree
                            </Button>
                        </DialogActions>
                    </Dialog>

                    <Dialog
                        open={this.state.open}
                        onClose={()=> (this.setState({ open: false }))}
                        aria-labelledby="form-dialog-title"
                        className={classes.dashboardDialog}
                    >
                        <DialogTitle id="form-dialog-title">Add dashboad</DialogTitle>

                        {form}

                        {/*
                        <DialogContent>
                            <TextField
                                autoFocus
                                margin="dense"
                                id="name"
                                label="Email Address"
                                type="email"
                                fullWidth
                            />
                        </DialogContent>
                        <DialogActions>
                            <Button onClick={()=> (this.setState({ open: false }))} color="primary">
                                Cancel
                            </Button>
                            <Button onClick={()=> (this.setState({ open: false }))} color="primary">
                                Save
                            </Button>
                        </DialogActions>
                        */}
                    </Dialog>


                </div>


                {/*
                <div className="row">
                    {dashboards}
                </div>
                <div className="add-btn" onClick={this.addDashboardModal}>
                    <i className="fas fa-plus"></i>
                </div>
                <div className="modal fade" id="addProjectModal" tabIndex="-1" role="dialog"
                     aria-labelledby="addProjectModalLabel" aria-hidden="true">
                    <div className="modal-dialog" role="document">
                        <div className="modal-content">
                            {form}
                        </div>
                    </div>
                </div>
                */}
            </React.Fragment>

        );
    }
}

function mapStateToProps(state) {
    const { groups } = state;
    return {
        groups
    };
}

const connectedHomePage = withRouter(withStyles(styles)(connect(mapStateToProps)(IndexPage)));
export { connectedHomePage as IndexPage };