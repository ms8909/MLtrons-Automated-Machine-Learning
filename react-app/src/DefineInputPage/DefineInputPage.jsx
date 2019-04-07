import React from 'react';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';

import {projectActions, userActions} from '../_actions';

import DateTimePicker from 'react-datetime-picker';
import {ErrorMessage, Field, Form, Formik} from "formik";
import * as Yup from "yup";

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
import InputLabel from '@material-ui/core/InputLabel';
import FormHelperText from '@material-ui/core/FormHelperText';
import FormControl from '@material-ui/core/FormControl';
import { withRouter } from "react-router";
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


const styles = theme => ({
    root: {
        flexGrow: 1,
        // backgroundColor: theme.palette.grey['100'],
        backgroundColor: '#303030',
        paddingBottom: 200,
        paddingTop: 50,
        minHeight: '70vh'
    },
    grid: {
        width: 1200,
        justifyContent: 'start',
        margin: `0 ${theme.spacing.unit * 2}px`,
        [theme.breakpoints.down('sm')]: {
            width: 'calc(100% - 20px)'
        }
    },
    paper: {
        padding: theme.spacing.unit * 3,
        textAlign: 'left',
        color: theme.palette.text.secondary,
        backgroundColor: '#1F1D1E',
        "& > *":{
            color: '#FFF',
        }
    },
    error: {
        color: theme.palette.error.main
    },
    formControl: {
        margin: `${theme.spacing.unit}px 0`,
        minWidth: '100%',
    },
    button: {
        marginTop: '2rem'
    },
    pd10:{
        paddingRight: '2rem'
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
    customColor: {
        color: "#FFF",
        '& > a': {
            color: theme.palette.primary.main,
        }
    }
});

class DefineInputPage extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            submitted: false,
        };
        this.setYVariable = this.setYVariable.bind(this);
        this.transformDataToHistogram = this.transformDataToHistogram.bind(this);
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

    componentDidMount() {
        const { id } = this.props.match.params;
        this.setState({
            project_id: id,
        });
        if(this.props.groups.selected_dataset == undefined){
            this.props.history.push('/dashboard/'+id);
            return
        }this.props.dispatch(projectActions.getDatasetMeta({id: this.props.groups.selected_dataset, name: ''}))
        this.props.dispatch(projectActions.getProblemType());
        this.props.dispatch(projectActions.getTimeType());
    }

    setYVariable(e){
        console.log('e here', e.target.value);
        for(let meta of this.props.groups.selected_metas){
            if(meta.id == e.target.value){
                this.setState({
                    distribution_graph: meta.distribution_data
                })
            }
        }

        console.log('distribution data here', this.state.distribution_graph);
    }

    render() {
        const { groups, classes  } = this.props;
        const { group, submitted } = this.state;

        const meta_options = [
            {id: 0, name: 'Sales'},
            {id: 1, name: 'Time'}
        ];

        const problem_options = [
            {id: 0, name: 'Forecast'},
            {id: 1, name: 'Prediction'}
        ];

        const DefineInputValidationSchema = Yup.object().shape({
            y_yariable: Yup.string()
                .required('Y yariable is required'),
            // time_yariable: Yup.string()
            //     .required('Time yariable is required'),
            problem_type: Yup.string()
                .required('Problem type is required'),
            // time_type: Yup.string()
            //     .required('Time type is required'),
        });

        const distribution_data = this.state.distribution_graph && this.state.distribution_graph.graph_type == 'bar_chart' &&{
            labels: this.state.distribution_graph.x,
            datasets: [
                {
                    label: 'Distribution data',
                    backgroundColor: 'rgba(165, 192, 91,0.8)',
                    borderColor: 'rgba(165, 192, 91,1)',
                    borderWidth: 1,
                    hoverBackgroundColor: 'rgba(165, 192, 91,1)',
                    hoverBorderColor: 'rgba(165, 192, 91,1)',
                    data: this.state.distribution_graph.y
                }
            ]
        };

        const form = <Formik
            initialValues={{ y_yariable: '', time_yariable: '', problem_type: '', time_type: '' }}
            validationSchema={DefineInputValidationSchema}
            validate ={(values, props /* only available when using withFormik */) => {
                    let errors = {};
                    if(values.time_yariable!='' && values.time_type==''){
                        errors.time_type = 'Time type is required';
                    }
                    return errors;
                }
            }
            onSubmit={(values, { setSubmitting }) => {
                values.project = this.state.project_id;
                values.processed_file = groups.selected_dataset;

                let selected = [];
                for(let col of this.props.groups.selected_metas){
                    selected.push(col.column_name);
                }

                if(values.time_yariable=='')delete values.time_yariable;
                if(values.time_type=='')delete values.time_type;

                values.selected = selected;
                this.props.dispatch(projectActions.createTraining(values, this.state.project_id));
                setSubmitting(false);
            }}
        >
            {({ isSubmitting, values, errors, touched, handleChange }) => (
                <Form>
                    <Grid container>
                        <Grid item xs={3} className={classes.pd10}>
                            <FormControl className={classes.formControl}>
                                <InputLabel className={classes.inputLabel} htmlFor="y_variable">What do you want to predict?</InputLabel>
                                <Select
                                    className={classes.inputField}
                                    onChange={(e) => {handleChange(e);this.setYVariable(e)}}
                                    value={values.y_yariable}
                                    inputProps={{
                                        name: 'y_yariable',
                                    }}
                                >
                                    {groups.selected_metas && groups.selected_metas.map((obj) =>
                                                <MenuItem key={obj.id} value={obj.id}>{obj.column_name}</MenuItem>

                                    )}
                                </Select>
                                {errors.y_yariable && touched.y_yariable &&
                                    <FormHelperText className={classes.error}>{errors.y_yariable}</FormHelperText>
                                }
                            </FormControl>
                        </Grid>
                        <Grid item xs={3} className={classes.pd10}>
                            <FormControl className={classes.formControl}>
                                <InputLabel className={classes.inputLabel} htmlFor="problem_type">What is the problem type?</InputLabel>
                                <Select
                                    className={classes.inputField}
                                    onChange={handleChange}
                                    value={values.problem_type}
                                    inputProps={{
                                        name: 'problem_type',
                                    }}
                                >
                                    {groups.problem_type && groups.problem_type.map((obj) =>
                                        <MenuItem key={obj.id} value={obj.id}>{obj.name}</MenuItem>
                                    )}
                                </Select>
                                {errors.problem_type && touched.problem_type &&
                                <FormHelperText className={classes.error}>{errors.problem_type}</FormHelperText>
                                }
                            </FormControl>
                        </Grid>

                        <Grid item xs={3} className={classes.pd10}>
                            <FormControl className={classes.formControl}>
                                <InputLabel className={classes.inputLabel} htmlFor="time_variable">What is your time variable</InputLabel>
                                <Select
                                    className={classes.inputField}
                                    onChange={handleChange}
                                    value={values.time_yariable}
                                    validate={(value)=>{
                                        console.log('validate value here', value);
                                    }}
                                    inputProps={{
                                        name: 'time_yariable',
                                    }}
                                >
                                    {groups.selected_metas && groups.selected_metas.map((obj) =>
                                        <MenuItem key={obj.id} value={obj.id}>{obj.column_name}</MenuItem>

                                    )}
                                </Select>
                                {errors.time_yariable && touched.time_yariable &&
                                    <FormHelperText className={classes.error}>{errors.time_yariable}</FormHelperText>
                                }
                            </FormControl>
                        </Grid>

                        <Grid item xs={3} className={classes.pd10}>
                            <FormControl className={classes.formControl}>
                                <InputLabel className={classes.inputLabel} htmlFor="time_type">What is the time type?</InputLabel>
                                <Select
                                    className={classes.inputField}
                                    onChange={handleChange}
                                    value={values.time_type}
                                    inputProps={{
                                        name: 'time_type',
                                    }}
                                >
                                    {groups.time_type && groups.time_type.map((obj) =>
                                        <MenuItem key={obj.id} value={obj.id}>{obj.format}</MenuItem>
                                    )}
                                </Select>
                                {errors.time_type && touched.time_type &&
                                    <FormHelperText className={classes.error}>{errors.time_type}</FormHelperText>
                                }
                            </FormControl>
                        </Grid>
                     </Grid>

                    {/*
                    <div className="form-group form-container">
                        <label htmlFor="first_name">What do you want to predict?</label>


                        <Field component="select" className="form-control" name="y_yariable">
                            <option>Select option</option>
                            {
                                groups.problem_type && groups.problem_type.length > 0 && groups.problem_type.map((obj) =>
                                    <option key={obj.id} value={obj.id}>{obj.column_name}</option>
                                )
                            }
                        </Field>
                        <ErrorMessage name="y_yariable" className="help-block" component="div" />
                    </div>

                    <div className="form-group form-container">
                        <label htmlFor="first_name">What is your problem type?</label>
                        <Field component="select" className="form-control" name="problem_type">
                            <option>Select option</option>
                            {
                                groups.problem_type  && groups.problem_type.map((obj) =>
                                    <option key={obj.id} value={obj.id}>{obj.name}</option>
                                )
                            }
                        </Field>
                        <ErrorMessage name="problem_type" className="help-block" component="div" />
                    </div>

                    <div className="form-group form-container">
                        <label htmlFor="first_name">What is your time yariable?</label>
                        <Field component="select" className="form-control" name="time_yariable">
                            <option>Select option</option>
                            {
                                groups.metas && groups.metas.length > 0 && groups.metas[0].meta.map((obj) =>
                                    <option key={obj.id} value={obj.id}>{obj.column_name}</option>
                                )
                            }
                        </Field>
                        <ErrorMessage name="time_yariable" className="help-block" component="div" />
                    </div>

                    */}

                    <br/>
                    <Button type="submit" variant="contained" color="primary" className={classes.button} disabled={isSubmitting}>
                        Start training
                    </Button>

                    {/*
                        <button type="submit" className="btn btn-primary" disabled={isSubmitting}>
                            Start training
                        </button>
                    */}
                </Form>
            )}
        </Formik>;



        return (

            <div className={classes.root}>
                <Grid container justify="center">
                    <Grid spacing={24} alignItems="start" justify="center" container className={classes.grid}>
                        <Grid item xs={12}>
                            <Paper className={classes.paper}>
                                <Typography variant="h6" gutterBottom>Define Inputs</Typography>
                                <br/>
                                {form}
                            </Paper>
                            <br/>
                            {   this.state.distribution_graph &&
                                <Paper className={classes.paper}>
                                    <Typography variant="h6" gutterBottom>Distribution graph</Typography>
                                    <br/>
                                    <div style={{width: '50%'}}>
                                        {
                                            this.state.distribution_graph.graph_type == 'histogram' &&
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
                                                    binnedData={this.transformDataToHistogram(this.state.distribution_graph)}
                                                    stroke={chartTheme.colors.default}
                                                    fill="url(#categorical)"
                                                    fillOpacity={0.7}
                                                />
                                                <XAxis/>
                                                <YAxis/>
                                            </ResponsiveHistogram>
                                        }
                                        {this.state.distribution_graph.graph_type == 'bar_chart' &&
                                            <Bar data={distribution_data} />
                                        }
                                    </div>
                                </Paper>
                            }
                        </Grid>
                    </Grid>
                </Grid>
            </div>
        /*
            <React.Fragment>
            <div className="col-md-6 col-md-offset-3">
                <h2>Define Inputs</h2>
                {form}
            </div>
            </React.Fragment>

            */
        );
    }
}

function mapStateToProps(state) {
    const { groups } = state;
    return {
        groups
    };
}

const connectedDefineInputPage = withRouter(withStyles(styles)(connect(mapStateToProps)(DefineInputPage)));
export { connectedDefineInputPage as DefineInputPage };