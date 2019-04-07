import React from 'react';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import { userActions } from '../_actions';
import * as Yup from 'yup';
import Avatar from '@material-ui/core/Avatar';
import Button from '@material-ui/core/Button';
import CssBaseline from '@material-ui/core/CssBaseline';
import FormControl from '@material-ui/core/FormControl';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Checkbox from '@material-ui/core/Checkbox';
import Input from '@material-ui/core/Input';
import InputLabel from '@material-ui/core/InputLabel';
import Paper from '@material-ui/core/Paper';
import Typography from '@material-ui/core/Typography';
import withStyles from '@material-ui/core/styles/withStyles';

import logo from '../images/logo.png';

const styles = theme => ({
    main: {
        width: 'auto',
        display: 'block', // Fix IE 11 issue.
        marginLeft: theme.spacing.unit * 3,
        marginRight: theme.spacing.unit * 3,
        marginBottom: '3rem',
        [theme.breakpoints.up(400 + theme.spacing.unit * 3 * 2)]: {
            width: 500,
            marginLeft: 'auto',
            marginRight: 'auto',
        },
    },
    paper: {
        marginTop: theme.spacing.unit * 8,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        padding: `${theme.spacing.unit * 2}px ${theme.spacing.unit * 3}px ${theme.spacing.unit * 3}px`,
        backgroundColor: '#1F1D1E',
        "& > *":{
            color: '#FFF',
        }
    },
    avatar: {
        margin: theme.spacing.unit,
        backgroundColor: theme.palette.secondary.main,
    },
    form: {
        width: '100%', // Fix IE 11 issue.
        marginTop: theme.spacing.unit,
    },
    submit: {
        marginTop: theme.spacing.unit * 3,
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

class RegisterPage extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            user: {
                full_name: '',
                email: '',
                phone: '',
                address: '',
                password1: '',
                password2: ''
            },
            submitted: false
        };

        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleChange(event) {
        const { name, value } = event.target;
        const { user } = this.state;
        this.setState({
            user: {
                ...user,
                [name]: value
            }
        });
    }

    // handleSubmit(event) {
    //     event.preventDefault();
    //
    //     this.setState({ submitted: true });
    //     const { user } = this.state;
    //     const { dispatch } = this.props;
    //     if (user.full_name && user.email && user.phone && user.address && user.password1 && user.password2) {
    //         dispatch(userActions.register(user));
    //     }
    // }


    handleSubmit(values, { setSubmitting }) {
        const { dispatch } = this.props;
        dispatch(userActions.register(values));
        setSubmitting(false)
    }

    render() {
        const { registering, classes } = this.props;
        const { user, submitted } = this.state;
        const signupValidationSchema = Yup.object().shape({
            first_name: Yup.string()
                .required('First name is required'),
            last_name: Yup.string()
                .required('Last name is required'),
            company_name: Yup.string()
                .required('Company name is required'),
            email: Yup.string()
                .email('Invalid email format')
                .required('Email address is required'),
            password: Yup.string()
                .required('Password is required'),
            confirm: Yup.string()
                .oneOf([Yup.ref('password')], 'Passwords do not match')
                .required('Confirm password is required'),
        });


        const form = <Formik
            initialValues={{ first_name: '', last_name: '', company_name: '', email: '', password: '', confirm:'' }}
            validationSchema={signupValidationSchema}
            onSubmit={this.handleSubmit}
        >
            {({  isSubmitting, values, errors, touched, handleChange }) => (
                <Form>

                    <FormControl margin="normal" required fullWidth>
                        <InputLabel htmlFor="first_name" className={classes.inputLabel}>First name</InputLabel>
                        <Input id="first_name" name="first_name" className={classes.inputField} autoFocus value={values.first_name} onChange={handleChange} />
                        {errors.first_name && touched.first_name &&
                            <div className="help-block">{errors.first_name}</div>
                        }
                    </FormControl>

                    <FormControl margin="normal" required fullWidth>
                        <InputLabel htmlFor="last_name" className={classes.inputLabel}>Last name</InputLabel>
                        <Input id="last_name" name="last_name" className={classes.inputField} value={values.last_name} onChange={handleChange} />
                        {errors.last_name && touched.last_name &&
                        <div className="help-block">{errors.last_name}</div>
                        }
                    </FormControl>

                    <FormControl margin="normal" required fullWidth>
                        <InputLabel htmlFor="company_name" className={classes.inputLabel}>Company name</InputLabel>
                        <Input id="company_name" name="company_name" className={classes.inputField} value={values.company_name} onChange={handleChange} />
                        {errors.company_name && touched.company_name &&
                        <div className="help-block">{errors.company_name}</div>
                        }
                    </FormControl>

                    <FormControl margin="normal" required fullWidth>
                        <InputLabel htmlFor="email" className={classes.inputLabel}>Email</InputLabel>
                        <Input id="email" name="email" className={classes.inputField} value={values.email} onChange={handleChange} />
                        {errors.email && touched.email &&
                        <div className="help-block">{errors.email}</div>
                        }
                    </FormControl>

                    <FormControl margin="normal" required fullWidth>
                        <InputLabel htmlFor="email" className={classes.inputLabel}>Password</InputLabel>
                        <Input id="password" type="password" className={classes.inputField} name="password" value={values.password} onChange={handleChange} />
                        {errors.password && touched.password &&
                        <div className="help-block">{errors.password}</div>
                        }
                    </FormControl>

                    <FormControl margin="normal" required fullWidth>
                        <InputLabel htmlFor="confirm" className={classes.inputLabel}>Confirm password</InputLabel>
                        <Input id="confirm" type="password" className={classes.inputField} name="confirm" value={values.confirm} onChange={handleChange} />
                        {errors.confirm && touched.confirm &&
                        <div className="help-block">{errors.confirm}</div>
                        }
                    </FormControl>


                    <Button
                        type="submit"
                        fullWidth
                        variant="contained"
                        color="primary"
                        className={classes.submit}
                    >
                        Submit
                    </Button>

                    <Typography variant="subtitle2" className={classes.customColor} gutterBottom style={{'paddingTop': '10px'}}>
                        Already registered? <Link to="/">Login</Link>
                    </Typography>
                </Form>
            )}
        </Formik>;


        return (
            <main className={classes.main}>
                <CssBaseline />
                <Paper className={classes.paper}>
                    <img width={125} src={logo} alt="logo"/>
                    <Typography component="h1" variant="h5">
                        Sign up
                    </Typography>
                    {
                        form
                    }
                </Paper>
            </main>
        );
    }
}

function mapStateToProps(state) {
    const { registering } = state.registration;
    return {
        registering
    };
}

const connectedRegisterPage = withStyles(styles)(connect(mapStateToProps)(RegisterPage));
export { connectedRegisterPage as RegisterPage };