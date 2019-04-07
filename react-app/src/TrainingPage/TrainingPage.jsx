import React from 'react';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';
import './index.css';
import {alertActions, projectActions, userActions} from '../_actions';
import Steps, { Step } from 'rc-steps';
import CircularProgressbar from 'react-circular-progressbar';
import 'react-circular-progressbar/dist/styles.css';
import {Line} from 'react-chartjs-2';
import {HorizontalBar} from 'react-chartjs-2';
import {TreeViewer} from "../_components";
import Paper from '@material-ui/core/Paper';
import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid';
import withStyles from '@material-ui/core/styles/withStyles';
import Button from '@material-ui/core/Button';
import DoneIcon from '@material-ui/icons/Done';
import CircularProgress from '@material-ui/core/CircularProgress';
import Chip from '@material-ui/core/Chip';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import Select from '@material-ui/core/Select';
import MenuItem from '@material-ui/core/MenuItem';
import Pusher from "pusher-js";
import { withRouter } from "react-router";
import * as zoom from 'chartjs-plugin-zoom';

var options={
    pan:{
        enabled:true,
        mode:'x'
    },
    zoom:{
        enabled:true,
        mode:'x',
    }
}

/*
backgroundColor: theme.palette.grey['100'],
*/

const styles = theme => ({
    root: {
        flexGrow: 1,
        // backgroundColor: theme.palette.grey['100'],
        backgroundColor: '#303030',
        paddingBottom: 200,
        paddingTop: 50,

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
        color: '#FFF',
        backgroundColor: '#1F1D1E',
        "& > *":{
            color: '#FFF',
        }
    },
    customPaper: {
        padding: theme.spacing.unit * 3,
        color: '#FFF',
        backgroundColor: '#303030',
        "& > *":{
            color: '#FFF',
        },
        marginLeft: '4rem'
    },
    statusItem: {
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
    },
    customColor: {
        color: "#FFF",
        '& > *':{
            color: "#FFF",
        }
    },
    inputLabel: {
        color: "#FFF"
    },
    inputField:{
        color: '#FFF',
        '&::before':{
            borderBottom: '1px solid #FFF!important'
        },
    },

});

let channelSubscriber;

class TrainingPage extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            submitted: false,
            active: -1,
            tab: 0,
            progress: {step: 0},
            ETR: '00:00:00',
            completed: 5,
            deployable: false,
            rank:-1
        }
        this.metricChange = this.metricChange.bind(this);
        this.modelClick = this.modelClick.bind(this);
        this.deployModel = this.deployModel.bind(this);
        this.interruptTraining = this.interruptTraining.bind(this);
    }

    componentWillUnmount() {
        channelSubscriber.unbind();
    }

    componentWillReceiveProps(nextProps) {
        let {groups, authenticating} = this.props;
        let nextGroups = nextProps.groups;
        if(groups.task!=nextGroups.task){
            if(nextGroups.task.result.event == 'train_csv') {
                if (nextGroups.task.result.step != 6) {
                    if(nextGroups.task.result.completed!=100) {
                        this.setState({
                            progress: nextGroups.task.result
                        })
                    }
                    else{
                        this.setState({
                            progress: {
                                step: 5,
                            },
                            completed: 100,
                            ETR: '00:00:00'
                        })
                    }
                } else {
                    setTimeout(()=>{
                        this.props.dispatch(alertActions.error('Error training in task.'));
                    },1000);
                    this.props.history.push('/dashboard/'+this.state.project_id);
                }
            }
        }
        if (groups.project != nextGroups.project) {
            this.props.dispatch(projectActions.clearState());
            var sets = [];
            if (nextGroups.project.status == 'Completed' || nextGroups.project.status == 'Deployed') {
                this.setState({
                    progress: {
                        step: 5
                    },
                    completed: 100,
                    ETR: '00:00:00'
                })
            }
        }
    }

    componentDidMount() {
        const { id } = this.props.match.params;
        this.setState({
            project_id: id,
        });

        const pusher = new Pusher('469a4013ee4603be5010', {
            cluster: 'ap2',
            forceTLS: true
        });

        const channel = pusher.subscribe(this.props.authentication.user.id.toString());

        channelSubscriber = channel;

        let context = this;
        channel.bind('train_csv', data => {
            console.log('progress train here', data);
            context.setState({
                progress: data.message
            })
            if(data.message.step == 3){
                console.log('progress here');
                context.setState({
                    ETR: data.message.ETR,
                    completed: data.message.completed,
                })
                if(context.state.rank == -1)
                    context.props.dispatch(projectActions.geTrainingModels(context.props.groups.training_detail[0].id))
                else
                    context.props.dispatch(projectActions.filterTrainingModels(context.props.groups.training_detail[0].id, context.state.rank));
            }
            else if(data.message.step == 5){
                context.setState({
                    deployable: true,
                    ETA: '00:00:00',
                    completed: 100,
                })
            }
            else if(data.message.step == 6) {
                setTimeout(()=>{
                    this.props.dispatch(alertActions.error('Error occured during training task.'));
                },1000);
                context.props.history.push('/dashboard/'+context.state.project_id);
            }
        });

        this.props.dispatch(projectActions.getProject(id));
        this.props.dispatch(projectActions.geTrainingDetail(id));
        this.props.dispatch(projectActions.geTrainingMetric());
        this.props.dispatch(projectActions.getTaskProgress(id));
    }

    metricChange(event){
        let metric_id = event.target.value;
        this.setState({
            rank: metric_id
        })
        this.props.dispatch(projectActions.filterTrainingModels(this.props.groups.training_detail[0].id, metric_id));
    }

    interruptTraining(){
        var r = confirm("Are you sure you want to cancel training?");
        if (r == true) {
            this.props.dispatch(projectActions.interruptTraining(this.state.project_id));
        }
    }

    modelClick(e, id){
        this.setState({'active': id});
        let { dispatch } = this.props;
        dispatch(projectActions.getAccuracy(id, this.state.project_id));
        // dispatch(projectActions.getROC(id, this.state.project_id));
        // dispatch(projectActions.getBluePrint(id, this.state.project_id));
        dispatch(projectActions.getLossInteraction(id, this.state.project_id));
        dispatch(projectActions.getFeatureImportance(id, this.state.project_id));
        dispatch(projectActions.getActualPrediction(id, this.state.project_id));
    }

    deployModel(){
        console.log('deploy model here', this.state.active);
        var r = confirm("Are you sure you want to deploy model!");
        if (r == true) {
            let request = {
                model: this.state.active,
                project: this.state.project_id
            }
            this.props.dispatch(projectActions.deployModel(JSON.stringify(request), this.state.project_id));
        }
    }

    render() {
        const { groups, classes  } = this.props;
        const { authentication } = this.props;
        const { submitted  } = this.state;
        const percentage = 66;
        const models = [{id: 0, name: "Simple Neural Network"},
            {id: 1, name: "XGBoost Extreme"},
            {id: 2, name: "Logistic Regression"},
            {id: 3, name: "Basic Linear Regression"},
        ];

        const statusSteps = [
            {step: 0, text: 'Loading data'},
            {step: 1, text: 'Transforming data'},
            {step: 2, text: 'Training multiple models'},
            {step: 3, text: 'Finalizing best models'},
            {step: 4, text: 'Ready for deployment'},
        ];


        const list = groups.models && groups.models.map((obj) =>
            <li className={this.state.active == obj.id ? 'active': ''} key={obj.id} onClick={(e) => this.modelClick(e, obj.id)}><Typography variant="subtitle2" className={classes.customColor} gutterBottom>{obj.name}</Typography></li>
        );

        const roc_data = {
            labels: ['0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7'],
            datasets: [
                {
                    label: 'Roc',
                    fill: false,
                    lineTension: 0.1,
                    backgroundColor: 'rgba(165, 192, 91,0.8)',
                    borderColor: 'rgba(165, 192, 91,1)',
                    borderCapStyle: 'butt',
                    borderDash: [],
                    borderDashOffset: 0.0,
                    borderJoinStyle: 'miter',
                    pointBorderColor: 'rgba(75,192,192,1)',
                    pointBackgroundColor: '#fff',
                    pointBorderWidth: 1,
                    pointHoverRadius: 5,
                    pointHoverBackgroundColor: 'rgba(165, 192, 91,1)',
                    pointHoverBorderColor: 'rgba(165, 192, 91,1)',
                    pointHoverBorderWidth: 2,
                    pointRadius: 1,
                    pointHitRadius: 0.01,
                    data: [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]
                }
            ]
        };

        const features_data = groups.feature_importance && {
            labels: Object.keys(groups.feature_importance),
            datasets: [
                {
                    label: 'Feature Importance',
                    backgroundColor: 'rgba(165, 192, 91,0.8)',
                    borderColor: 'rgba(165, 192, 91,1)',
                    borderWidth: 1,
                    hoverBackgroundColor: 'rgba(165, 192, 91,1)',
                    hoverBorderColor: 'rgba(165, 192, 91,1)',
                    data: Object.values(groups.feature_importance)
                }
            ]
        };

        const loss_data = groups.loss_interaction && {
            labels: groups.loss_interaction.data.x,
            datasets: [
                {
                    label: 'Loss on training',
                    fill: false,
                    lineTension: 0.1,
                    backgroundColor: 'rgba(165, 192, 91,0.8)',
                    borderColor: 'rgba(165, 192, 91,1)',
                    borderCapStyle: 'butt',
                    borderDash: [],
                    borderDashOffset: 0.0,
                    borderJoinStyle: 'miter',
                    pointBorderColor: 'rgba(75,192,192,1)',
                    pointBackgroundColor: '#fff',
                    pointBorderWidth: 1,
                    pointHoverRadius: 5,
                    pointHoverBackgroundColor: 'rgba(165, 192, 91,1)',
                    pointHoverBorderColor: 'rgba(165, 192, 91,1)',
                    pointHoverBorderWidth: 2,
                    pointRadius: 1,
                    pointHitRadius: 0.01,
                    data: groups.loss_interaction.data.y_training
                },
                {
                    label: 'Loss on validation',
                    fill: false,
                    lineTension: 0.1,
                    backgroundColor: 'rgba(255,99,132,0.2)',
                    borderColor: 'rgba(255,99,132,1)',
                    borderCapStyle: 'butt',
                    borderDash: [],
                    borderDashOffset: 0.0,
                    borderJoinStyle: 'miter',
                    pointBorderColor: 'rgba(75,192,192,1)',
                    pointBackgroundColor: '#fff',
                    pointBorderWidth: 1,
                    pointHoverRadius: 5,
                    pointHoverBackgroundColor: 'rgba(75,192,192,1)',
                    pointHoverBorderColor: 'rgba(220,220,220,1)',
                    pointHoverBorderWidth: 2,
                    pointRadius: 1,
                    pointHitRadius: 0.01,
                    data: groups.loss_interaction.data.y_validation
                },

            ]
        };

        const prediction_data = groups.actual_prediction && {
            labels: groups.actual_prediction.data.x,
            datasets: [
                {
                    label: 'Actual',
                    fill: false,
                    lineTension: 0.1,
                    backgroundColor: 'rgba(165, 192, 91,0.8)',
                    borderColor: 'rgba(165, 192, 91,1)',
                    borderCapStyle: 'butt',
                    borderDash: [],
                    borderDashOffset: 0.0,
                    borderJoinStyle: 'miter',
                    pointBorderColor: 'rgba(75,192,192,1)',
                    pointBackgroundColor: '#fff',
                    pointBorderWidth: 1,
                    pointHoverRadius: 5,
                    pointHoverBackgroundColor: 'rgba(165, 192, 91,1)',
                    pointHoverBorderColor: 'rgba(220,165, 192, 91,1)',
                    pointHoverBorderWidth: 2,
                    pointRadius: 1,
                    pointHitRadius: 0.01,
                    data: groups.actual_prediction.data.y_actual
                },
                {
                    label: 'Prediction',
                    fill: false,
                    lineTension: 0.1,
                    backgroundColor: 'rgba(75,192,192,0.4)',
                    borderColor: 'rgba(75,192,192,1)',
                    borderCapStyle: 'butt',
                    borderDash: [],
                    borderDashOffset: 0.0,
                    borderJoinStyle: 'miter',
                    pointBorderColor: 'rgba(75,192,192,1)',
                    pointBackgroundColor: '#fff',
                    pointBorderWidth: 1,
                    pointHoverRadius: 5,
                    pointHoverBackgroundColor: 'rgba(75,192,192,1)',
                    pointHoverBorderColor: 'rgba(220,220,220,1)',
                    pointHoverBorderWidth: 2,
                    pointRadius: 1,
                    pointHitRadius: 0.01,
                    data: groups.actual_prediction.data.y_prediction
                }
            ]
        };


        const tree_data = [{key: 'Step1', name: 'Step1'}, {key: 'Step2', name: 'Step2', parent: 'Step1'}, {key: 'Step3', name: 'Step3', parent: 'Step1'}]

        const status = <Paper className={classes.paper}>
            <Typography variant="h6" gutterBottom>Status</Typography>
            <Grid container>
                {statusSteps.map((obj) => (
                    <Grid item sm={12} className={classes.statusItem}>
                        <div className={classes.customColor}>
                            <Typography variant="subtitle2" gutterBottom>
                                {obj.step+1}. {obj.text}
                            </Typography>
                            <Chip
                                label={this.state.progress.step > obj.step ? "100%" : '0%'}
                                color={this.state.progress.step > obj.step ? "primary" : this.state.progress.step == obj.step ? 'secondary': ''}
                            />
                        </div>
                        {
                            this.state.progress.step > obj.step &&
                            <DoneIcon color="primary"/>
                        }
                        {
                            this.state.progress.step == obj.step &&
                            <CircularProgress color="secondary" />
                        }
                    </Grid>
                ))}
            </Grid>
        </Paper>;

        return (

            <div className={classes.root}>
                <Grid container justify="center">
                    <Grid spacing={24} alignItems="start" justify="center" container className={classes.grid}>
                        <Grid item xs={9}>
                            <Paper className={classes.paper}>
                                <Grid container justify="center">
                                    <Grid item xs={5} className={classes.customColor}>
                                        <Typography variant="subtitle2" gutterBottom>Name</Typography>
                                        <Typography variant="body2" gutterBottom>{groups.training_detail && groups.training_detail.length > 0 && groups.training_detail[0].processed_file_d.name.split('.')[0]}</Typography>
                                        <br/>
                                        <Typography variant="subtitle2" gutterBottom>Target column</Typography>
                                        <Typography variant="body2" gutterBottom>{groups.training_detail && groups.training_detail.length > 0 && groups.training_detail[0].y_yariable_d.column_name}</Typography>
                                        <br/>
                                        <Grid container justify="center">
                                            <Grid item xs={6} className={classes.customColor}>
                                                <Typography variant="subtitle2" gutterBottom>Time variable</Typography>
                                                <Typography variant="body2" gutterBottom>{groups.training_detail && groups.training_detail.length > 0 && groups.training_detail[0].time_yariable ? groups.training_detail && groups.training_detail.length > 0 && groups.training_detail[0].time_yariable_d.column_name: 'N/A'}</Typography>
                                                <br/>
                                                <Typography variant="subtitle2" gutterBottom>Problem type</Typography>
                                                <Typography variant="body2" gutterBottom>{groups.training_detail && groups.training_detail.length > 0 && groups.training_detail[0].problem_type_d.name}</Typography>
                                            </Grid>
                                            <Grid item xs={6} className={classes.customColor}>
                                                <Typography variant="subtitle2" gutterBottom>Rows</Typography>
                                                <Typography variant="body2" gutterBottom>{groups.training_detail && groups.training_detail.length > 0 && groups.training_detail[0].processed_file_d.rows}</Typography>
                                                <br/>
                                                <Typography variant="subtitle2" gutterBottom>Columns</Typography>
                                                <Typography variant="body2" gutterBottom>7</Typography>
                                            </Grid>
                                        </Grid>
                                    </Grid>
                                    <Grid item xs={7}>
                                        <Grid container justify="center">
                                            <Grid item xs={5}>
                                                <CircularProgressbar
                                                    initialAnimation='true'
                                                    percentage={this.state.completed}
                                                    text={`${this.state.completed}%`}
                                                    styles={{
                                                        path: { stroke: `#A5C05B` },
                                                        text: { fill: '#A5C05B', fontSize: '16px', fontFamily: 'roboto' },
                                                    }}
                                                />
                                            </Grid>
                                            <Grid item xs={7} style={{textAlign: 'right'}}>
                                                <Paper className={classes.customPaper}>
                                                    <Typography variant="subtitle2" gutterBottom>Time Elasped</Typography>
                                                    <Typography variant="body2" gutterBottom>00:00:00</Typography>
                                                    <br/>
                                                    <Typography variant="subtitle2" gutterBottom>Time Remaining</Typography>
                                                    <Typography variant="body2" gutterBottom>{this.state.ETR}</Typography>
                                                    <br/>
                                                    { this.state.progress.step == 3 && this.state.completed >=20 && this.state.completed <=100 &&
                                                        <Button onClick={this.interruptTraining} variant="contained"
                                                                color="primary" className={classes.button}>
                                                            Interrupt
                                                        </Button>
                                                    }
                                                </Paper>
                                            </Grid>
                                        </Grid>
                                    </Grid>
                                </Grid>
                            </Paper>
                            <br/>
                            <Paper className={classes.paper}>

                                <Grid container>
                                    <Grid item sm={6} className={classes.customColor}>
                                        <Typography variant="h6" gutterBottom>Model name</Typography>
                                        <Typography variant="body2" gutterBottom>
                                            {
                                                groups.models && groups.models.map((obj) =>
                                                    this.state.active === obj.id && obj.name
                                                )
                                            }
                                        </Typography>
                                    </Grid>
                                    {
                                        this.state.completed == 100 && this.state.active!=-1 &&
                                        <Grid item sm={6} style={{textAlign: 'right'}}>
                                            <Button onClick={this.deployModel} variant="outlined" color="primary">
                                                Deploy model
                                            </Button>
                                        </Grid>
                                    }
                                </Grid>

                                <br/>
                                <Tabs
                                    value={this.state.tab}
                                    onChange={(e, value)=>{this.setState({tab: value})}}
                                    indicatorColor="primary"
                                    textColor="primary"
                                >
                                    <Tab className={classes.customColor} label="Accuracy" />
                                    {/*<Tab label="ROC" />*/}
                                    {/*<Tab label="BluePrint" />*/}
                                    <Tab className={classes.customColor} label="Feature Importance" />
                                    <Tab className={classes.customColor} label="Loss vs Time" />
                                    <Tab className={classes.customColor} label="Actual vs prediction" />
                                </Tabs>

                                <br/>

                                {this.state.tab === 0 &&
                                <React.Fragment>
                                <Typography variant="h6" gutterBottom>Metric</Typography>
                                    {
                                        groups.accuracy ?
                                        <table border="0" width="75%">
                                            {
                                                groups.accuracy.map((obj) =>
                                                    <tr key={obj.metric.id}>
                                                        <td className={classes.customColor}><Typography variant="subtitle2" gutterBottom>{obj.metric.name}</Typography></td>
                                                        <td className={classes.customColor}><Typography variant="body2" gutterBottom>{parseFloat(obj.value).toFixed(2)}</Typography></td>
                                                    </tr>
                                                )
                                            }

                                        </table>:
                                        <Typography variant="body2" gutterBottom>No data available</Typography>
                                    }
                                </React.Fragment>
                                }
                                {/*{this.state.tab === 1 &&*/}
                                    {/*<Line data={roc_data} />*/}
                                {/*}*/}
                                {/*{this.state.tab === 2 &&*/}
                                    {/*<TreeViewer treeData={tree_data}/>*/}
                                {/*}*/}
                                {this.state.tab === 1 &&
                                    (groups.feature_importance ?
                                            <HorizontalBar data={features_data} options={options}/>:
                                            <Typography variant="body2" gutterBottom>No data available</Typography>)
                                }
                                {this.state.tab === 2 &&
                                    (groups.loss_interaction ?
                                            <Line data={loss_data} options={options}/>:
                                            <Typography variant="body2" gutterBottom>No data available</Typography>)
                                }
                                {this.state.tab === 3 &&
                                    (groups.actual_prediction ?
                                            <Line data={prediction_data} options={options}/>:
                                            <Typography variant="body2" gutterBottom>No data available</Typography>)
                                }
                            </Paper>
                        </Grid>

                        <Grid item xs={3}>
                            {status}
                            <br/>
                            <Paper className={classes.paper}>
                                <Typography variant="subtitle2" gutterBottom>Model: {groups.models ? groups.models.length: '0'}/20</Typography>
                                <br/>
                                <Typography variant="subtitle2" gutterBottom>Rank by:</Typography>
                                <Select
                                    className={classes.inputField}
                                    style={{width: '100%'}}
                                    onChange={this.metricChange}
                                    value={this.state.rank}
                                    inputProps={{
                                        name: 'metric',
                                    }}
                                >
                                    {groups.metric && groups.metric.map(
                                        (obj) =>
                                        <MenuItem key={obj.id} value={obj.id}>{obj.name}</MenuItem>
                                    )}
                                </Select>
                                <ul className="list-container">
                                    {list}
                                </ul>
                            </Paper>
                        </Grid>
                    </Grid>
                </Grid>
            </div>

            /*   <React.Fragment>
                <div className="row">
                    <div className="col sm-8 col-md-9">
                        <div className="card-container h-50" style={{padding: '20px'}}>
                            <div className="row">
                                <div className="col-md-5 data-container">
                                    <div className="data-inner-container">
                                        <h4>Name</h4>
                                        <p>{groups.training_detail && groups.training_detail.length > 0 && groups.training_detail[0].processed_file_d.name}</p>
                                    </div>
                                    <div className="data-inner-container">
                                        <h4>Target column</h4>
                                        <p>{groups.training_detail && groups.training_detail.length > 0 && groups.training_detail[0].y_yariable_d.column_name}</p>
                                    </div>
                                    <div className="data-inner-container">
                                        <h4>Time Variable</h4>
                                        <p>{groups.training_detail && groups.training_detail.length > 0 && groups.training_detail[0].time_yariable_d.column_name}</p>
                                    </div>
                                    <div className="data-inner-container">
                                        <h4>Problem Type</h4>
                                        <p>{groups.training_detail && groups.training_detail.length > 0 && groups.training_detail[0].problem_type_d.name}</p>
                                    </div>
                                    <div className="data-inner-container">
                                        <h4>Rows</h4>
                                        <p>{groups.training_detail && groups.training_detail.length > 0 && groups.training_detail[0].processed_file_d.rows}</p>
                                    </div>
                                    <div className="data-inner-container">
                                        <h4>Column</h4>
                                        <p>0</p>
                                    </div>
                                </div>
                                <div className="col-md-7">
                                    <div className="progress-container">
                                        <div className="time-container">
                                            <h4>Elapsed time</h4>
                                            <p>00:01:00</p>
                                        </div>
                                        <div className="progress-bar-container">
                                            <CircularProgressbar
                                                initialAnimation='true'
                                                percentage={percentage}
                                                text={`${percentage}%`}
                                            />
                                        </div>
                                        <div className="time-container">
                                            <h4>Remaining time</h4>
                                            <p>00:20:00</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div className="col sm-4 col-md-3">
                        <div className="card-container" style={{'padding': '15px'}}>
                            <Steps direction="vertical">
                                <Step title="Loading data" />
                                <Step title="Transforming data" />
                                <Step title="Training multiple models" />
                                <Step title="Tuning parameters" />
                                <Step title="Finalizing best models" />
                                <Step title="Ready for deployment" />
                            </Steps>
                        </div>
                    </div>
                </div>
                <div className="row">
                    <div className="col sm-8 col-md-9">
                        <div className="card-container">
                        <div className="data-inner-container">
                            <h4>Model Name</h4>
                            <p>
                                {
                                    models && models.map((obj) =>
                                        this.state.active === obj.id && obj.name
                                    )
                                }
                            </p>
                        </div>

                        <div className="card">
                            <ul className="nav nav-tabs" role="tablist">
                                <li className="active"><a onClick={(e) => this.setState({'tab': 1})} data-target="#accuracy" role="tab" data-toggle="tab">Accuracy</a></li>
                                <li ><a onClick={(e) => this.setState({'tab': 2})}data-target="#roc" role="tab" data-toggle="tab">Roc</a></li>
                                <li ><a onClick={(e) => this.setState({'tab': 3})} data-target="#blue" role="tab" data-toggle="tab">Blue print</a></li>
                                <li ><a onClick={(e) => this.setState({'tab': 4})} data-target="#feature" role="tab" data-toggle="tab">Feature Importance</a></li>
                                <li ><a onClick={(e) => this.setState({'tab': 5})} data-target="#loss" role="tab" data-toggle="tab">Loss vs iterations</a></li>
                                <li ><a onClick={(e) => this.setState({'tab': 6})} data-target="#actual" role="tab" data-toggle="tab">Actual vs prediction</a></li>

                            </ul>
                            <div className="tab-content">
                                <div role="tabpanel" className="tab-pane active" id="accuracy">
                                    <div className="data-inner-container">
                                        <h4>Metrics</h4>
                                    </div>
                                    <table border="0" width="75%">
                                        <tr>
                                            <td>Mean Absolute Error</td>
                                            <td>98.33</td>
                                        </tr>
                                        <tr>
                                            <td>Root Mean Squared Error</td>
                                            <td>33.45</td>
                                        </tr>
                                        <tr>
                                            <td>R-squared</td>
                                            <td>0.987</td>
                                        </tr>
                                        <tr>
                                            <td>Log-loss accuracy</td>
                                            <td>0.045</td>
                                        </tr>
                                    </table>
                                </div>

                                <div role="tabpanel" className="tab-pane" id="roc">
                                    <Line data={roc_data} />
                                </div>
                                <div role="tabpanel" className="tab-pane h-40" id="blue">
                                    {this.state.tab == 3 && <TreeViewer treeData={tree_data}/>}
                                </div>
                                <div role="tabpanel" className="tab-pane" id="feature">
                                    <HorizontalBar data={features_data} />
                                </div>
                                <div role="tabpanel" className="tab-pane" id="loss">
                                    <Line data={loss_data} />
                                </div>
                                <div role="tabpanel" className="tab-pane" id="actual">
                                    <Line data={prediction_data} />
                                </div>
                            </div>
                        </div>
                    </div>
                    </div>
                    <div className="col sm-4 col-md-3">
                        <div className="card-container">
                            <div>
                                <div><span>Models:</span> 0/4</div>
                                <div>
                                    Rank by:
                                    <select className="form-control" onChange={this.metricChange}>
                                        {
                                            groups.metric && groups.metric.map(
                                                (obj) =>
                                                    <option key={obj.id} value={obj.id}>{obj.name}</option>
                                            )
                                        }
                                    </select>
                                </div>
                                <ul className="list-container">
                                    {list}
                                </ul>

                            </div>
                        </div>
                    </div>
                </div>
            </React.Fragment>*/

        );
    }
}

function mapStateToProps(state) {
    const { groups } = state;
    const { authentication } = state;
    return {
        groups,
        authentication
    };
}

const connectedTrainingPage = withRouter(withStyles(styles)(connect(mapStateToProps)(TrainingPage)));
export { connectedTrainingPage as TrainingPage };