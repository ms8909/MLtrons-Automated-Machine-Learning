import React from 'react';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';
import './dashboard.css'
import Dropzone from 'react-dropzone'
import {alertActions, projectActions} from '../_actions';
import classNames from 'classnames'
import './steps/assets/index.less';
import './steps/assets/iconfont.less';
import { RecordMapper } from "../_components";
import Paper from '@material-ui/core/Paper';
import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid';
import withStyles from '@material-ui/core/styles/withStyles';
import Chip from '@material-ui/core/Chip';
import CloudUploadIcon from '@material-ui/icons/CloudUpload';
import DoneIcon from '@material-ui/icons/Done';
import CircularProgress from '@material-ui/core/CircularProgress';
import Button from '@material-ui/core/Button';
import AppBar from '@material-ui/core/AppBar';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Select from '@material-ui/core/Select';
import MenuItem from '@material-ui/core/MenuItem';
import ReactPaginate from 'react-paginate';
import Pusher from 'pusher-js';
import { withRouter } from "react-router";
import ExpansionPanel from '@material-ui/core/ExpansionPanel';
import ExpansionPanelSummary from '@material-ui/core/ExpansionPanelSummary';
import ExpansionPanelDetails from '@material-ui/core/ExpansionPanelDetails';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import Checkbox from '@material-ui/core/Checkbox';
import HeatMap from 'react-heatmap-grid';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';
import {Bar, HorizontalBar} from 'react-chartjs-2';

import {
    Histogram,
    BarSeries,
    DensitySeries,
    XAxis,
    YAxis,
    PatternLines,
    LinearGradient,
    withParentSize,
} from '@data-ui/histogram';
import { chartTheme } from '@data-ui/theme';


const ResponsiveHistogram = withParentSize(({ parentWidth, parentHeight, children, ...rest }) => (
    <Histogram
        width={parentWidth}
        height={parentWidth}
        theme={chartTheme}
        {...rest}
    >
        {children}
    </Histogram>
));

var EventEmitter = require('events');

const styles = theme => ({
    root: {
        flexGrow: 1,
        backgroundColor: theme.palette.grey['100'],
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
        color: theme.palette.text.secondary
    },
    statusItem: {
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        paddingRight: 50
    },
    treeView: {
        width: '100%',
        border: 0,
        height: 150,
        backgroundColor: '#FFF',
        color: 'rgba(0, 0, 0, 0.87)',
        fontSize: '0.875rem',
        fontFamily: "Roboto"
    },
    mapper:{
        height: 400,
        width: '100%'
    },
    delete: {
        color: 'red',
        marginLeft: '8px'
    },
    upload: {
        fontSize: '3.5rem',
        color: '#A5C05B',
    },
    tabContainer:{
        marginTop: 30,
        overflowX: 'scroll',
        paddingBottom: 30
    },
    bold: {
        fontWeight: '500'
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
    heatMap: {
        '& > div': {
            fontSize: '13px',
            fontFamily: 'roboto',
            fontWeight: 'bold',
            '& > div:first-child':{
                '& > div':{
                    transform: 'rotate(-40deg)',
                }
            }
        }
    },
    tabOuterContainer:{
        '& > div':{
            '& > div':{
                '& > div':{
                    overflowX: 'scroll'
                }
            }
        }
    },
    status: {
        padding: '12px'
    },
    uploadContainer: {
        display: 'contents',
        '& > span':{
            marginLeft: '12px'
        }
    },
    uploadPaper: {
        padding: '0 12px',
        height: '100%'
    },
    relationshipContainer:{
        boxShadow: '0px 1px 5px 0px rgba(0,0,0,0.2), 0px 2px 2px 0px rgba(0,0,0,0.14), 0px 3px 1px -2px rgba(0,0,0,0.12)',
        borderRadius: '4px',
        margin: 0
    },
    distributionContainer: {
        '& > div':{
            '& > div':{
                maxWidth: '60vw'
            }
        }
    }
});

let channelSubscriber;
let ee = new EventEmitter();

class DashboardPage extends React.Component {
    constructor(props){
        super(props);
        this.onDrop = this.onDrop.bind(this);
        this.onLinkChange = this.onLinkChange.bind(this);
        this.onSelectDataset = this.onSelectDataset.bind(this);
        this.mergeLinks = this.mergeLinks.bind(this);
        this.proceedTraining = this.proceedTraining.bind(this);
        this.handleChecked = this.handleChecked.bind(this);
        this.transformDataToHistogram = this.transformDataToHistogram.bind(this);
        this.state = {
            selected : -1,
            tab: 0,
            dataset: 0,
            progress: {step: -1},
            dirty: false,
            current: 0,
            checked: [],
            all: false,
            graph_modal: false
        }
    }

    componentWillUnmount() {
        channelSubscriber.unbind();
        ee.removeAllListeners('error');
    }

    componentDidMount() {
        const { id } = this.props.match.params;
        this.setState({
            project_id: id,
        });
        this.props.dispatch(projectActions.getProject(id));
        this.props.dispatch(projectActions.getType());
        this.props.dispatch(projectActions.getRole());
        this.props.dispatch(projectActions.getImputation());
        this.props.dispatch(projectActions.getConnections(id));
        this.props.dispatch(projectActions.getTaskProgress(id));

        const pusher = new Pusher('469a4013ee4603be5010', {
            cluster: 'ap2',
            forceTLS: true
        });
        const channel = pusher.subscribe(this.props.authentication.user.id.toString());
        channelSubscriber = channel;
        let context = this;
        channel.bind('read_csv', data => {
            console.log('progress csv here', data);
            if(data.message.step == 4) {
                context.props.dispatch(projectActions.getProject(context.state.project_id));
                context.setState({
                    progress: data.message
                })
            }
            else if(data.message.step == 5){
                context.setState({
                    progress: {step: -1}
                })
                context.props.dispatch(alertActions.error('Error uploading dataset.'));
            }
            else{
                context.setState({
                    progress: data.message
                })
            }
        });
        channel.bind('merge_csv', data => {
            console.log('progress merge here', data);
            if(data.message.step == 4){
                context.props.dispatch(projectActions.getProject(context.state.project_id));
                context.setState({
                    progress: data.message
                })
            }
            else if(data.message.step == 5){
                context.setState({
                    progress: {step: -1}
                })
                context.props.dispatch(alertActions.error('Error merging dataset.'));
            }
            else{
                context.setState({
                    progress: data.message
                })
            }
        });
        ee.on('error', function (text) {
            context.setState({
                progress: {step: -1}
            })
        })
    }

    handleDeleteUser(id) {
        return (e) => this.props.dispatch(userActions.delete(id));
    }


    mergeLinks(){
        console.log('merge links', this.state.connections);
        var r = confirm("Are you sure you want to merge datasets!");
        if (r == true) {
            this.setState({current: 1, progress: {step: 0}});
            this.props.dispatch(projectActions.mergeConnection(this.state.project_id, JSON.stringify(this.state.connections)))
        }
    }

    proceedTraining(){
        if(this.state.checked.length == 0){
            this.props.dispatch(alertActions.error('Select meta columns to proceed for training'));
            return;
        }
        let li = [];
        for(let meta of this.props.groups.metas[this.state.dataset].meta){
            if(this.state.checked.indexOf(meta.id)!=-1)li.push(meta)
        }
        this.props.dispatch(projectActions.setDataset(this.props.groups.metas[this.state.dataset].dataset.id, li));
        this.props.history.push('/input/'+this.state.project_id)
    }

    setTab(value){
        this.setState({tab: value});
        if(value==1){
            this.props.dispatch(projectActions.getDatasetData(this.props.groups.metas[this.state.dataset].dataset.id));
        }
    }


    getDataByPage(page){
        let limit = 10;
        let offset = (page.selected) * limit;
        this.props.dispatch(projectActions.getDatasetData(this.props.groups.metas[this.state.dataset].dataset.id, offset));
    }

    onDrop(files){
       for(let file of files) {
           var data = new FormData();
           data.append('file_url', file);
           data.append('project', this.state.project_id);
           this.setState({
               current: 0,
               progress: {
                   step: 0
               }
           });
           this.props.dispatch(projectActions.addDataset(data, this.state.project_id));
       }
    }

    onMetaChange(event, meta_id){
        const { name, value } = event.target;
        let data = new FormData();
        data.append(name, value);
        this.props.dispatch(projectActions.updateMeta(meta_id, data));
    }

    addConnections(nodes) {
        let {groups} = this.props;
        for (let node of nodes) {
            let exist = false;
            if(groups.connections!=undefined) {
                for (let connection of groups.connections) {
                    if (node.from_column == connection.from_column && node.to_column == connection.to_column) exist = true;
                }
            }
            if(!exist){
                node.project = this.state.project_id;
                this.props.dispatch(projectActions.addConnection(this.state.project_id, JSON.stringify(node)))
            }
        }
    }

    deleteConnection(nodes) {
        let {groups} = this.props;
        for (let connection of groups.connections) {
            let exist = false;
            for (let node of nodes) {
               if (node.from_column == connection.from_column && node.to_column == connection.to_column) exist = true;
            }
            if(!exist){
                this.props.dispatch(projectActions.deleteConnection(connection.id, this.state.project_id))
            }
        }
    }

    onLinkChange(value){
        console.log('on link change value here', value.nodeDataArray);
        let nodes_location = [];
        for (let node of value.nodeDataArray){
            nodes_location.push(
                {
                    dataset_id: node.id,
                    loc: node.loc
                }
            )
        }
        this.props.dispatch(projectActions.updateLocation(nodes_location));
        console.log('node locations', nodes_location);
        let links = value.linkDataArray;
        let { groups } = this.props;
        let nodes = [];
        for(let link of links){
            let {from, fromPort, to, toPort} = link;
            let from_id;
            let to_id;
            for(let set of groups.metas) {
                if (set.dataset.name.indexOf(from)!=-1) {
                    for(let column of set.meta){
                        if(column.column_name==fromPort)from_id = column.id;
                    }
                }
                if (set.dataset.name.indexOf(to)!=-1) {
                    for(let column of set.meta){
                        if(column.column_name==toPort)to_id = column.id;
                    }
                }
            }

            nodes.push({from_column: from_id, to_column: to_id})
        }
        // this.addConnections(nodes);
        // this.deleteConnection(nodes);
        console.log('nodes here', nodes);
        this.setState({
            connections: nodes,
            dirty: true,
        })
    }

    onSelectDataset(e){
        if(this.state.selected != e.id)
                this.setState({
                    selected: e.id
                });
    }


    componentWillReceiveProps(nextProps) {
        let {groups, authenticating} = this.props;
        let nextGroups = nextProps.groups;
            if (groups.task != nextGroups.task) {
                if(nextGroups.task.result.event == 'read_csv' || nextGroups.task.result.event == 'merge_csv') {
                    if (nextGroups.task.result.step != 5) {
                        this.setState({
                            progress: nextGroups.task.result
                        })
                    } else {
                        this.props.dispatch(alertActions.error('Error in task.'));
                    }
                    if(nextGroups.task.result.event == 'read_csv'){
                        let progress = this.state.progress;
                        progress.current = 0;
                        this.setState({
                            progress: progress
                        })
                    }
                    else{
                        let progress = this.state.progress;
                        progress.current = 1;
                        this.setState({
                            progress: progress
                        })
                    }
                }
            }
        if (groups.project != nextGroups.project) {
            this.props.dispatch(projectActions.clearState());
            var sets = [];
            if(nextGroups.project.datasets.length > 0){
                this.setState({
                    progress: {
                        step: 4
                    }
                })
            }
            for (let set of nextGroups.project.datasets) {
                sets.push({
                    id: set.id,
                    text: set.name,
                    isLeaf: true
                })
                this.props.dispatch(projectActions.getDatasetMeta({id: set.id, name: set.name, status: set.status, rows: set.rows, heat: set.grid_map, loc: set.loc, columns: set.columns}))
                this.props.dispatch(projectActions.getDatasetData(set.id))
            }
        }
    }

    deleteDataset(e, id){
        var r = confirm("Are you sure you want to delete dataset!");
        if (r == true){
            if(this.props.groups.project.datasets.length == 1){
                this.setState({
                    progress: {
                        step: -1
                    }
                })
            }
            this.props.dispatch(projectActions.deleteDataset(id, this.state.project_id));
        }
    }

    handleChecked(e){
        let checked = e.target.checked;
        let id = e.target.value;
        let li = this.state.checked;
        if(checked)li.push(parseInt(id));
        else{
            let index = li.indexOf(parseInt(id));
            li.splice(index, 1);
        }
        this.setState({checked: li});
    }

    handleAllChecked(checked){
        let li = [];
        if(checked){
            for(let meta of this.props.groups.metas[this.state.dataset].meta){
                li.push(meta.id)
            }
            this.setState({'checked': li, 'all': true})
        }
        else
            this.setState({'checked': [], 'all': false})
    }

    handleAll(e){
        let checked = e.target.checked;
        this.handleAllChecked(checked)
    }


    transformDataToHistogram(distribution_data){
        let data = []
        let x = distribution_data.x;
        let y = distribution_data.y;
        for(let i = 0; i < x.length -1 ;i++){
            data.push(
                { bin0: x[i], bin1: x[i+1], count: y[i], id: i },
            )
        }
        return data;
    }


    render() {
        const { groups, classes, authentication } = this.props;

        const xLabels = new Array(24).fill(0).map((_, i) => `${i}`);
        const yLabels = ['Sun', 'Mon', 'Tue'];
        const data = new Array(yLabels.length)
            .fill(0)
            .map(() => new Array(xLabels.length).fill(0).map(() => Math.floor(Math.random() * 100)));


        const statusSteps = [
            {step: 0, text: 'Uploading data'},
            {step: 1, text: 'Reading raw data'},
            {step: 2, text: 'Exploratory data analysis'},
            {step: 3, text: 'Displaying data'},
        ];

        const mergeSteps = [
            {step: 0, text: 'Loading datasets'},
            {step: 1, text: 'Merging data frames'},
            {step: 2, text: 'Analyzing & saving dataset'},
            {step: 3, text: 'Displaying data'},
        ];

        const distribution_data = this.state.selected_meta && this.state.selected_meta.distribution_data && this.state.selected_meta.distribution_data.graph_type == 'bar_chart' &&{
            labels: this.state.selected_meta.distribution_data.x,
            datasets: [
                {
                    label: 'Distribution data',
                    backgroundColor: 'rgba(165, 192, 91,0.8)',
                    borderColor: 'rgba(165, 192, 91 ,1)',
                    borderWidth: 1,
                    hoverBackgroundColor: 'rgba(165, 192, 91 ,0.1)',
                    hoverBorderColor: 'rgba(165, 192, 91 ,1)',
                    data: this.state.selected_meta.distribution_data.y
                }
            ]
        };

        const steps = this.state.current == 0 ? statusSteps : mergeSteps;

        const status = <Paper className={[classes.paper, classes.status]}>
            {/*<Typography variant="h6" gutterBottom>Status</Typography>*/}
            <Grid container>
                {steps.map((obj) => (
                    <Grid item sm={3} className={classes.statusItem}>
                        <div>
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
                {/*
                <Grid item sm={3} className={classes.statusItem}>
                    <div>
                        <Typography variant="subtitle2" gutterBottom>
                            2. Reading raw data
                        </Typography>
                        <Chip
                            label="20%"
                            color="secondary"
                        />
                    </div>
                    <CircularProgress color="secondary" />
                </Grid>
                <Grid item sm={3}>
                    <Typography variant="subtitle2" gutterBottom>
                        3. Exploratory data analysis
                    </Typography>
                    <Chip
                        label="0%"
                    />
                </Grid>
                <Grid item sm={3}>
                    <Typography variant="subtitle2" gutterBottom>
                        4. Displaying data
                    </Typography>
                    <Chip
                        label="0%"
                    />
                </Grid>
                */}
            </Grid>
        </Paper>;

        // const nodeData = [
        //     { key: "Sales",
        //         fields: [
        //             { name: "id" },
        //             { name: "sale" },
        //             { name: "time" }
        //         ],
        //         loc: "0 0" },
        //     { key: "Customers",
        //         fields: [
        //             { name: "id" },
        //             { name: "name" },
        //             { name: "address" },
        //             { name: "phone" }
        //         ],
        //         loc: "250 0" },
        // ];

        // const linkData = [
        //     { from: "Sales", fromPort: "id", to: "Customers", toPort: "id" },
        // ];

        const linkData = [];

        const binnedNumeric = [
            { bin0: 0, bin1: 5, count: 5, id: 1 },
            { bin0: 5, bin1: 10, count: 10, id: 2 },
            { bin0: 10, bin1: 20, count: 2, id: 3 },
        ]

        // const data = [
        //     {id: '1', sale: '100',time: '10th Jan, 2018', color: 'red'},
        //     {id: '2', sale: '20',time: '11th Jan, 2018', color: 'yellow'},
        //     {id: '3', sale: '50',time: '12th Jan, 2018', color: 'blue'},
        //     {id: '4', sale: '150',time: '13th Jan, 2018', color: 'green'},
        //     {id: '5', sale: '75',time: '14th Jan, 2018', color: 'white'},
        // ];

        // const meta_data = [
        //     {id: 1, column_name: 'Sale', type: {id: 1}, role: {id: 0}, imputation: {id:2}, calculations:{mean: 0, mode: 0, median: 0, min: 0, max:0, count:0, missing:0}, graph:{date:[{x:10, y:4},{x:5, y:2}]}},
        //     {id: 1, column_name: 'Time', type: {id: 0}, role: {id: 0}, imputation: {id:1}, calculations:{mean: 0, mode: 0, median: 0, min: 0, max:0, count:0, missing:0}, graph:{date:[{x:5, y:6},{x:5, y:2}]}},
        //     {id: 1, column_name: 'Color', type: {id: 2}, role: {id: 0}, imputation: {id:0}, calculations:{mean: 0, mode: 0, median: 0, min: 0, max:0, count:0, missing:0}, graph:{date:[{x:15, y:8},{x:5, y:2}]}},
        // ];


        const meta_table = <Table>
            <TableHead>
                <TableRow>
                    <TableCell>
                        <Checkbox
                            checked={this.state.all}
                            onChange={(e) => {this.handleAll(e)}}
                            color="primary"
                        />
                    </TableCell>
                    <TableCell>Column name</TableCell>
                    <TableCell>Type</TableCell>
                    <TableCell>Role</TableCell>
                    <TableCell>Imputation</TableCell>
                    <TableCell>&nbsp;</TableCell>
                </TableRow>
            </TableHead>
            <TableBody>
                {groups.metas && groups.metas.length > 0 && groups.metas[this.state.dataset].meta.map((row, index) => (
                    <TableRow key={index}>
                        <TableCell align="left">
                            <Checkbox
                                checked={this.state.checked.indexOf(row.id)!=-1}
                                onChange={this.handleChecked}
                                value={row.id}
                                color="primary"
                            />
                        </TableCell>
                        <TableCell align="left">
                            <Typography variant="subtitle2" gutterBottom>
                                {row.column_name}
                            </Typography>
                        </TableCell>
                        <TableCell align="left">
                            <Select
                                value={row.type}
                                onChange={(e)=>{this.onMetaChange(e, row.id);row.type=e.target.value}}
                                inputProps={{
                                    name: 'type',
                                }}
                            >
                                {groups.meta_type && groups.meta_type.map((obj) => (
                                    <MenuItem key={obj.id} value={obj.id}>{obj.name}</MenuItem>
                                ))}
                            </Select>
                        </TableCell>
                        <TableCell align="left">
                            <Select
                                value={row.role}
                                onChange={(e)=>{this.onMetaChange(e, row.id);row.role=e.target.value}}
                                inputProps={{
                                    name: 'role',
                                }}
                            >
                                {groups.meta_role && groups.meta_role.map((obj) => (
                                    <MenuItem key={obj.id} value={obj.id}>{obj.name}</MenuItem>
                                ))}
                            </Select>
                        </TableCell>
                        <TableCell align="left">
                            <Select
                                value={row.imputation}
                                onChange={(e)=>{this.onMetaChange(e, row.id); row.imputation=e.target.value}}
                                inputProps={{
                                    name: 'imputation',
                                }}
                            >
                                {groups.meta_imputation && groups.meta_imputation.map((obj) => (
                                    <MenuItem key={obj.id} value={obj.id}>{obj.name}</MenuItem>
                                ))}
                            </Select>
                        </TableCell>
                        <TableCell align="left">
                            {/*<Grid container style={{display:'flex',flexWrap:'wrap', width: '200px'}}>*/}
                                {/*<Typography variant="body2" gutterBottom><span className={classes.bold}>Mean: </span>{parseFloat(row.mean).toFixed(2)},&nbsp;</Typography>*/}
                                {/*<Typography variant="body2" gutterBottom><span className={classes.bold}>Stdev: </span>{parseFloat(row.stdev).toFixed(2)},&nbsp;</Typography>*/}
                                {/*<Typography variant="body2" gutterBottom><span className={classes.bold}>Min: </span>{parseFloat(row.min).toFixed(2)},&nbsp;</Typography>*/}
                                {/*<Typography variant="body2" gutterBottom><span className={classes.bold}>Max: </span>{parseFloat(row.max).toFixed(2)},&nbsp;</Typography>*/}
                                {/*<Typography variant="body2" gutterBottom><span className={classes.bold}>Count: </span>{parseFloat(row.count).toFixed(2)},&nbsp;</Typography>*/}
                                {/*<Typography variant="body2" gutterBottom><span className={classes.bold}>Missing: </span>{parseFloat(row.missing).toFixed(2)}&nbsp;</Typography>*/}
                            {/*</Grid>*/}
                            <Button onClick={(e) => {this.setState({graph_modal: true, selected_meta: row})}} size="small" color="primary">
                                View distribution
                            </Button>
                        </TableCell>
                    </TableRow>
                ))}
            </TableBody>
        </Table>;

        return (

            <div className={classes.root}>
                <Grid container justify="center">
                    <Grid spacing={24} alignItems="start" justify="center" container className={classes.grid}>
                        <Grid item xs={3}>
                            <Paper className={[classes.paper, classes.uploadPaper]}>
                                <Dropzone onDrop={this.onDrop}>
                                    {({getRootProps, getInputProps, isDragActive}) => {
                                        return (
                                            <div
                                                {...getRootProps()}
                                                className={classNames('dropzone', {'dropzone--isActive': isDragActive})}
                                                style={{display: 'flex', textAlign: 'center', alignItems: 'center', padding: '1rem'}}>
                                                <input {...getInputProps()} />
                                                {
                                                    isDragActive ?

                                                        <Typography variant="subtitle2" gutterBottom>Drop datasets here...</Typography> :
                                                        <Typography variant="subtitle2" gutterBottom className={classes.uploadContainer}>
                                                            <CloudUploadIcon className={classes.upload}/>
                                                            <span>Drop dataset here, or click to select dataset to upload.</span>
                                                        </Typography>
                                                }
                                            </div>
                                        )
                                    }}
                                </Dropzone>
                            </Paper>
                        </Grid>

                        <Grid item xs={9}>
                            {status}
                        </Grid>
                    </Grid>
                    <Grid spacing={24} alignItems="start" justify="center" container className={classes.grid}>

                        {/*<Grid item xs={3}>*/}
                            {/*/!**/}
                            {/*<Paper className={classes.paper}>*/}
                                {/*<Typography variant="h6" gutterBottom>Datasets</Typography>*/}
                                {/*<TreeView className={classes.treeView} items={ this.state.datasets } onSelectItem={this.onSelectDataset}/>*/}
                            {/*</Paper>*/}
                            {/**!/*/}
                            {/*<ExpansionPanel style={{margin: 0}}>*/}
                                {/*<ExpansionPanelSummary*/}
                                    {/*expandIcon={<ExpandMoreIcon />}*/}
                                    {/*onClick={event => this.setState({selected: -1})}*/}
                                {/*>*/}
                                    {/*<Typography variant="h6">Datasets</Typography>*/}
                                {/*</ExpansionPanelSummary>*/}
                                {/*<ExpansionPanelDetails className={classes.expansionDetail}>*/}
                                    {/*<List component="div" disablePadding className={classes.expansionList}>*/}
                                        {/*{groups.project && groups.project.datasets.map((obj) =>*/}
                                            {/*<ListItem*/}
                                                {/*key={obj.id}*/}
                                                {/*button*/}
                                                {/*className={classes.nested}*/}
                                                {/*selected={this.state.selected == obj.id}*/}
                                                {/*onClick={event => this.setState({selected: obj.id})}*/}
                                            {/*>*/}
                                                {/*<ListItemText primary={obj.name}/>*/}
                                            {/*</ListItem>*/}
                                        {/*)}*/}
                                    {/*</List>*/}
                                {/*</ExpansionPanelDetails>*/}
                            {/*</ExpansionPanel>*/}

                            {/*{*/}
                                {/*this.state.selected!=-1 &&*/}
                                {/*groups.project.datasets.map((obj) =>*/}
                                    {/*this.state.selected == obj.id &&*/}
                                    {/*<React.Fragment key={obj.id}>*/}
                                        {/*<br/>*/}
                                        {/*<Paper className={classes.paper}>*/}
                                            {/*<Typography variant="subtitle2" gutterBottom>Dataset name</Typography>*/}
                                            {/*<Typography variant="body2" gutterBottom>{obj.name}</Typography>*/}
                                            {/*<br/>*/}
                                            {/*<Grid container>*/}
                                                {/*<Grid item sm={6}>*/}
                                                    {/*<Typography variant="subtitle2" gutterBottom>No of rows</Typography>*/}
                                                    {/*<Typography variant="body2" gutterBottom>{obj.rows}</Typography>*/}
                                                {/*</Grid>*/}
                                                {/*<Grid item sm={6}>*/}
                                                    {/*<Typography variant="subtitle2" gutterBottom>No of columns</Typography>*/}
                                                    {/*<Typography variant="body2" gutterBottom>{obj.columns}</Typography>*/}
                                                {/*</Grid>*/}
                                            {/*</Grid>*/}
                                            {/*<br/>*/}
                                            {/*{ (this.state.progress.step == -1 || this.state.progress.step == 4) &&*/}
                                                {/*<Button onClick={(e) => {*/}
                                                    {/*this.deleteDataset(e, obj.id)}} size="small" className={classes.delete}>*/}
                                                    {/*Delete*/}
                                                {/*</Button>*/}
                                            {/*}*/}
                                         {/*</Paper>*/}
                                    {/*</React.Fragment>*/}
                                {/*)*/}
                            {/*}*/}
                            {/*<br/>*/}
                            {/*<Paper className={classes.paper}>*/}
                                {/*<Dropzone onDrop={this.onDrop}>*/}
                                    {/*{({getRootProps, getInputProps, isDragActive}) => {*/}
                                        {/*return (*/}
                                            {/*<div*/}
                                                {/*{...getRootProps()}*/}
                                                {/*className={classNames('dropzone', {'dropzone--isActive': isDragActive})}*/}
                                                {/*style={{display: 'flex', textAlign: 'center', alignItems: 'center', padding: '1rem'}}>*/}
                                                {/*<input {...getInputProps()} />*/}
                                                {/*{*/}
                                                    {/*isDragActive ?*/}

                                                        {/*<Typography variant="subtitle2" gutterBottom>Drop datasets here...</Typography> :*/}
                                                        {/*<Typography variant="subtitle2" gutterBottom>*/}
                                                            {/*<CloudUploadIcon className={classes.upload}/>*/}
                                                            {/*<br/>*/}
                                                            {/*Try dropping some files here, or click to select files to upload.*/}
                                                        {/*</Typography>*/}
                                                {/*}*/}
                                            {/*</div>*/}
                                        {/*)*/}
                                    {/*}}*/}
                                {/*</Dropzone>*/}
                            {/*</Paper>*/}

                        {/*</Grid>*/}

                        <Grid item xs={12}>


                            <ExpansionPanel className={classes.relationshipContainer}>
                                <ExpansionPanelSummary
                                    expandIcon={<ExpandMoreIcon />}
                                >
                                    <Typography variant="h6">Relationships</Typography>
                                </ExpansionPanelSummary>
                                <ExpansionPanelDetails className={classes.expansionDetail}>
                                    <Grid container>
                                        {this.state.dirty == true && (this.state.progress.step == -1 || this.state.progress.step == 4) && groups.project && groups.project.datasets.length > 1 &&
                                            <Grid xs={12}>
                                                <Button onClick={this.mergeLinks} variant="outlined" color="primary"
                                                        style={{margin: '0 24px', textAlign:'right'}}>
                                                    Merge datasets
                                                </Button>
                                            </Grid>
                                        }
                                    {groups.tables && groups.linkData &&  groups.tables.length == groups.project.datasets.length &&
                                    <div className={classes.mapper}>
                                        <RecordMapper nodeData={groups.tables} linkData={groups.linkData} onChange={this.onLinkChange}/>
                                    </div>
                                    }
                                    </Grid>
                                </ExpansionPanelDetails>
                            </ExpansionPanel>


                            {/*<Paper className={classes.paper}>*/}
                                {/*<Grid container>*/}
                                    {/*<Grid item sm={6}>*/}
                                        {/*<Typography variant="h6" gutterBottom>Relationships</Typography>*/}
                                    {/*</Grid>*/}
                                {/*{*/}
                                    {/*this.state.dirty == true && (this.state.progress.step == -1 || this.state.progress.step == 4) && groups.project && groups.project.datasets.length > 1 &&*/}
                                    {/*<Grid item sm={6} style={{textAlign: 'right'}}>*/}
                                        {/*<Button onClick={this.mergeLinks} size="small" color="primary">*/}
                                            {/*Merge datasets*/}
                                        {/*</Button>*/}
                                    {/*</Grid>*/}
                                {/*}*/}
                                {/*</Grid>*/}

                                {/*/!*{groups.tables && groups.linkData &&  groups.tables.length == groups.project.datasets.length &&*!/*/}
                                    {/*/!*<div className={classes.mapper}>*!/*/}
                                        {/*/!*<RecordMapper nodeData={groups.tables} linkData={groups.linkData} onChange={this.onLinkChange}/>*!/*/}
                                    {/*/!*</div>*!/*/}
                                {/*/!*}*!/*/}
                            {/*</Paper>*/}

                            <br/>
                            <div>
                                <AppBar position="static" color="default">
                                    <Tabs
                                        className={classes.tabOuterContainer}
                                        value={this.state.dataset}
                                        onChange={(e, value)=>{this.setState({dataset: value, tab: 0}); this.handleAllChecked(false)}}
                                        indicatorColor="primary"
                                        textColor="primary"
                                        variant="fullWidth"
                                    >
                                        {
                                            groups.metas && groups.metas.map(
                                                (obj) => (
                                                    <Tab key={obj.id} label={obj.dataset.name} />
                                                )
                                            )
                                        }
                                    </Tabs>
                                </AppBar>
                                <Paper className={classes.paper} style={{borderRadius: 0}}>
                                <Grid container>
                                    <Grid xs={8}>
                                        <Tabs
                                            value={this.state.tab}
                                            onChange={(e, value)=>{this.setTab(value)}}
                                            indicatorColor="primary"
                                            textColor="primary"
                                        >
                                            <Tab label="View metadata" />
                                            <Tab label="View data" />
                                            <Tab label="View graph" />
                                            <Tab label="Dataset info" />
                                        </Tabs>
                                    </Grid>
                                    { (this.state.progress.step == -1 || this.state.progress.step == 4) && groups.project && groups.project.datasets.length > 0 &&
                                        <Grid xs={4} style={{textAlign: 'right'}}>
                                            <Button onClick={this.proceedTraining} variant="outlined" color="secondary">
                                                Build models
                                            </Button>
                                        </Grid>
                                    }
                                </Grid>
                                {this.state.tab === 0 &&
                                <div className={classes.tabContainer}>
                                    {groups.metas && groups.metas.length > 0 &&
                                        meta_table
                                    }
                                </div>
                                }

                                {this.state.tab === 1 &&
                                <div className={classes.tabContainer}>
                                    {groups.dataset_data &&
                                    <div>
                                        <Table>
                                            <TableHead>
                                                <TableRow>
                                                    {groups.dataset_data_columns.map((obj, index) => (
                                                        <TableCell key={index}>{obj.Header}</TableCell>
                                                    ))}
                                                </TableRow>
                                            </TableHead>
                                            <TableBody>
                                                {groups.dataset_data.map((row, index) => (
                                                    <TableRow key={index}>
                                                        {groups.dataset_data_columns.map((obj, index1) => (
                                                            <TableCell key={index1} align="right">{row[obj.Header]}</TableCell>
                                                        ))}
                                                    </TableRow>
                                                ))}
                                            </TableBody>
                                        </Table>
                                        <ReactPaginate
                                            previousLabel={'previous'}
                                            nextLabel={'next'}
                                            breakLabel={'...'}
                                            breakClassName={'break-me'}
                                            pageCount={groups.metas[this.state.dataset].dataset.rows / 10}
                                            marginPagesDisplayed={2}
                                            pageRangeDisplayed={5}
                                            onPageChange={(page)=>{this.getDataByPage(page)}}
                                            containerClassName={'pagination'}
                                            subContainerClassName={'pages pagination'}
                                            activeClassName={'active'}
                                        />
                                    </div>

                                    }
                                </div>
                                }

                                {this.state.tab === 2 &&
                                <div className={classes.tabContainer} style={{padding: '0 8px 30px 8px'}}>
                                    <Typography variant="h6" gutterBottom>Pearson corelation</Typography>
                                    {   groups.metas[this.state.dataset].dataset.heat.pearson.x ?
                                        <div className={classes.heatMap}>
                                            <HeatMap
                                                xLabels={groups.metas[this.state.dataset].dataset.heat.pearson.x}
                                                yLabels={groups.metas[this.state.dataset].dataset.heat.pearson.y}
                                                data={groups.metas[this.state.dataset].dataset.heat.pearson.array}
                                                xLabelWidth={20}
                                                yLabelWidth={200}
                                                yLabelTextAlign='left'
                                                cellStyle={(background, value, min, max, data, x, y) => ({
                                                    background: `rgb(66, 86, 244, ${1 - (max - value) / (max - min)})`,
                                                    fontSize: "11px",
                                                })}
                                                cellRender={value => value && `${parseFloat(value).toFixed(2)}`}
                                            />
                                        </div>:
                                            <Typography variant="body2" gutterBottom>no graph generated</Typography>
                                    }
                                    <br/>
                                    <br/>
                                    <Typography variant="h6" gutterBottom>Spearman corelation</Typography>
                                    {  groups.metas[this.state.dataset].dataset.heat.spearman.x ?
                                        <div className={classes.heatMap}>
                                            <HeatMap
                                                xLabels={groups.metas[this.state.dataset].dataset.heat.spearman.x}
                                                yLabels={groups.metas[this.state.dataset].dataset.heat.spearman.y}
                                                data={groups.metas[this.state.dataset].dataset.heat.spearman.array}
                                                xLabelWidth={20}
                                                yLabelWidth={200}
                                                yLabelTextAlign='left'
                                                cellStyle={(background, value, min, max, data, x, y) => ({
                                                    background: `rgb(66, 86, 244, ${1 - (max - value) / (max - min)})`,
                                                    fontSize: "11px",
                                                })}
                                                cellRender={value => value && `${parseFloat(value).toFixed(2)}`}
                                            />
                                        </div>:
                                        <Typography variant="body2" gutterBottom>no graph generated</Typography>
                                    }

                                </div>
                                }
                                {this.state.tab === 3 &&
                                    <div className={classes.tabContainer}>
                                        <div style={{padding: '0 8px'}}>
                                            <Typography variant="h6" gutterBottom>Dataset name</Typography>
                                            <Typography variant="body2" gutterBottom>{groups.metas[this.state.dataset].dataset.name}</Typography>
                                            <br/>
                                            <Grid container>
                                                <Grid item sm={6}>
                                                    <Typography variant="h6" gutterBottom>No of rows</Typography>
                                                    <Typography variant="body2" gutterBottom>{groups.metas[this.state.dataset].dataset.rows}</Typography>
                                                </Grid>
                                                <Grid item sm={6}>
                                                    <Typography variant="h6" gutterBottom>No of columns</Typography>
                                                    <Typography variant="body2" gutterBottom>{groups.metas[this.state.dataset].dataset.columns}</Typography>
                                                </Grid>
                                            </Grid>
                                            <br/>
                                        </div>
                                        { (this.state.progress.step == -1 || this.state.progress.step == 4) &&
                                            <Button onClick={(e) => {
                                            this.deleteDataset(e, groups.metas[this.state.dataset].dataset.id)}} variant="outlined" className={classes.delete}>
                                                Delete
                                            </Button>
                                        }
                                    </div>
                                }

                            </Paper>
                            </div>



                        </Grid>
                    </Grid>
                </Grid>
                <Dialog
                    open={this.state.graph_modal}
                    onClose={()=>{this.setState({graph_modal: false, selected_meta: undefined})}}
                    aria-labelledby="form-dialog-title"
                    className={classes.distributionContainer}
                >
                    <DialogTitle id="form-dialog-title">Distribution data</DialogTitle>
                    {this.state.selected_meta &&
                        <DialogContent>
                        <DialogContentText>

                            <Typography variant="body2" gutterBottom>{this.state.selected_meta.column_name}</Typography>
                            <br/>

                            <Grid container style={{width: '45vw'}}>
                                <Grid item xs={4}>
                                    <Typography variant="subtitle2" gutterBottom>Mean</Typography>
                                    <Typography variant="body2" gutterBottom>{parseFloat(this.state.selected_meta.mean).toFixed(2)}</Typography>
                                    <br/>
                                    <Typography variant="subtitle2" gutterBottom>Stdev</Typography>
                                    <Typography variant="body2" gutterBottom>{parseFloat(this.state.selected_meta.stdev).toFixed(2)}</Typography>
                                    {/*<Typography variant="body2" gutterBottom><span className={classes.bold}>Mean: </span>{parseFloat(row.mean).toFixed(2)},&nbsp;</Typography>*/}
                                    {/*<Typography variant="body2" gutterBottom><span className={classes.bold}>Stdev: </span>{parseFloat(row.stdev).toFixed(2)},&nbsp;</Typography>*/}
                                    {/*<Typography variant="body2" gutterBottom><span className={classes.bold}>Min: </span>{parseFloat(row.min).toFixed(2)},&nbsp;</Typography>*/}
                                    {/*<Typography variant="body2" gutterBottom><span className={classes.bold}>Max: </span>{parseFloat(row.max).toFixed(2)},&nbsp;</Typography>*/}
                                    {/*<Typography variant="body2" gutterBottom><span className={classes.bold}>Count: </span>{parseFloat(row.count).toFixed(2)},&nbsp;</Typography>*/}
                                    {/*<Typography variant="body2" gutterBottom><span className={classes.bold}>Missing: </span>{parseFloat(row.missing).toFixed(2)}&nbsp;</Typography>*/}
                                    <br/>

                                </Grid>
                                <Grid item xs={4}>
                                    <Typography variant="subtitle2" gutterBottom>Min</Typography>
                                    <Typography variant="body2" gutterBottom>{parseFloat(this.state.selected_meta.min).toFixed(2)}</Typography>
                                    <br/>
                                    <Typography variant="subtitle2" gutterBottom>Max</Typography>
                                    <Typography variant="body2" gutterBottom>{parseFloat(this.state.selected_meta.max).toFixed(2)}</Typography>
                                    <br/>
                                </Grid>
                                <Grid item xs={4}>
                                    <Typography variant="subtitle2" gutterBottom>Count</Typography>
                                    <Typography variant="body2" gutterBottom>{parseFloat(this.state.selected_meta.count).toFixed(2)}</Typography>
                                    <br/>
                                    <Typography variant="subtitle2" gutterBottom>Missing values</Typography>
                                    <Typography variant="body2" gutterBottom>{parseFloat(this.state.selected_meta.missing).toFixed(2)}</Typography>
                                    <br/>
                                </Grid>
                            </Grid>
                        </DialogContentText>
                            {
                                this.state.selected_meta.distribution_data && this.state.selected_meta.distribution_data.graph_type == 'histogram' &&
                                <ResponsiveHistogram binType="numeric">
                                    <PatternLines
                                        id="categorical"
                                        height={8}
                                        width={8}
                                        background="#fff"
                                        stroke={chartTheme.colors.default}
                                        strokeWidth={0.5}
                                        orientation={['diagonal']}
                                    />
                                    <BarSeries
                                        binnedData={this.transformDataToHistogram(this.state.selected_meta.distribution_data)}
                                        stroke={chartTheme.colors.default}
                                        fill="url(#categorical)"
                                        fillOpacity={0.7}
                                    />
                                    <XAxis/>
                                    <YAxis/>
                                </ResponsiveHistogram>
                            }
                                {this.state.selected_meta.distribution_data && this.state.selected_meta.distribution_data.graph_type == 'bar_chart' &&
                                    <Bar data={distribution_data}/>
                                }

                    </DialogContent>
                    }
                    <DialogActions>
                        <Button  onClick={()=>{this.setState({graph_modal: false, selected_meta: undefined})}} color="primary">
                            Close
                        </Button>
                    </DialogActions>
                </Dialog>
            </div>


        /*

            <div className="row">
                <div className="col-md-2 col-sm-3">
                    <div className="card-container treeview-container h-60">
                        <TreeView style={{'height': '40vh'}} items={ this.state.datasets } onSelectItem={this.onSelectDataset}/>
                        {
                            this.state.selected!=-1 &&
                            groups.project.datasets.map((obj) =>
                                this.state.selected == obj.id &&
                                <div key={obj.id} style={{'padding': '10px'}}>
                                    <span style={{fontWeight: 'bold'}}>Dataset name:</span> {obj.name}<br/>
                                    <span style={{fontWeight: 'bold'}}>No of rows:</span> {obj.rows}<br/>
                                    <a href={obj.file_url} target="_blank">View dataset</a><br/>
                                    <a onClick={(e)=>{this.deleteDataset(e, obj.id)}} style={{'color': 'red'}}>Delete dataset</a><br/>
                                </div>
                            )
                        }
                    </div>
                    <div className="card-container h-40">
                        <Dropzone onDrop={this.onDrop}>
                            {({getRootProps, getInputProps, isDragActive}) => {
                                return (
                                    <div
                                        {...getRootProps()}
                                        className={classNames('dropzone', {'dropzone--isActive': isDragActive})}
                                        style={{display: 'flex', textAlign: 'center', alignItems: 'center'}}>
                                        <input {...getInputProps()} />
                                        {
                                            isDragActive ?

                                                <p>Drop datasets here...</p> :
                                                <p><i style={{fontSize: '40px', padding: '10px'}} className="fas fa-cloud-upload-alt"></i><br/>Try dropping some files here, or click to select files to upload.</p>
                                        }
                                    </div>
                                )
                            }}
                        </Dropzone>
                    </div>
                </div>
                <div className="col-md-10 col-sm-9">

                    <div className="row">
                        <div className="col-md-8 col-sm-8">
                            <div className="card-container h-40">
                                {groups.tables && groups.linkData &&  groups.tables.length == groups.project.datasets.length &&
                                    <RecordMapper nodeData={groups.tables} linkData={groups.linkData} onChange={this.onLinkChange}/>
                                }
                            </div>
                        </div>
                        <div className="col-md-4 col-sm-4">
                            <div className="card-container mh-40" style={{padding: '10px'}}>
                                <Steps direction="vertical">
                                    <Step title="Uploading data" />
                                    <Step title="Reading raw data" />
                                    <Step title="Exploratory data analysis" />
                                    <Step title="Displaying data" />
                                </Steps>
                                {
                                    groups.metas && groups.metas.length > 0 && groups.project.status == 'Pending' &&
                                    <div style={{width: '100%', textAlign: 'center'}}>
                                        <Link to={"/input/"+this.state.project_id} className="btn btn-primary">Proceed to training</Link>
                                    </div>
                                }
                            </div>
                        </div>
                    </div>

                    <div className="row">
                        <div className="col-sm-12">
                            <div className="card-container h-60">

                                <div className="row">
                                    <div className="col-md-12">
                                        <div className="card">
                                            <ul className="nav nav-tabs" role="tablist">
                                                <li role="presentation" className="active"><a data-target="#home"
                                                                                              aria-controls="home"
                                                                                              role="tab"
                                                                                              data-toggle="tab">Meta data</a>
                                                </li>
                                                <li role="presentation"><a data-target="#profile" aria-controls="profile"
                                                                           role="tab" data-toggle="tab">Tabular view</a></li>

                                            </ul>
                                            <div className="tab-content">
                                                <div role="tabpanel" className="tab-pane active" id="home">
                                                    {groups.metas && groups.metas.length > 0 &&
                                                        <ReactTable
                                                            data={groups.metas[0].meta}
                                                            columns={meta_columns}
                                                        />
                                                    }
                                                </div>
                                                <div role="tabpanel" className="tab-pane" id="profile">
                                                    {groups.dataset_data &&
                                                        <ReactTable
                                                            data={groups.dataset_data}
                                                            columns={groups.dataset_data_columns}
                                                        />
                                                    }
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>


                            </div>
                        </div>
                    </div>
                </div>
            </div>
            */
        );
    }
}

function mapStateToProps(state) {
    const { groups, authentication } = state;
    return {
        authentication,
        groups
    };
}

const connectedDashboardPage = withRouter(withStyles(styles)(connect(mapStateToProps)(DashboardPage)));
export { connectedDashboardPage as DashboardPage };