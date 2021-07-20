import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Card from '@material-ui/core/Card';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';
import TextField from '@material-ui/core/TextField';
import FormLabel from '@material-ui/core/FormLabel';
import FormControl from '@material-ui/core/FormControl';
import FormGroup from '@material-ui/core/FormGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import FormHelperText from '@material-ui/core/FormHelperText';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import Switch from '@material-ui/core/Switch';
import Grid from '@material-ui/core/Grid';
import axios from 'axios'
const useStyles = makeStyles({
    card: {
        width: 500,
        padding: 20
    },
    listitem: {
        padding: 15
    },
    title: {
        fontSize: 25,
        marginLeft: 25
    },
    pos: {
        marginBottom: 12,
    },
    button: {
        marginLeft: 25
    },
    textfield: {
        width: 400,
        justifyContent: 'center'
    }
});

export default function RunTest(props) {
    const [state, setState] = React.useState({
        xss: false,
        sqli: false,
        cj: false,
        sdt: false,
        csrf: false

    });

    const handleChange = (event) => {
        setState({ ...state, [event.target.name]: event.target.checked });
    };
    const classes = useStyles();
    const clear=()=>{
        setState({
            xss: false,
            sqli: false,
            cj: false,
            sdt: false,
            csrf: false
        })
    }
    const handleSubmit = async () => {
        // console.log(document.getElementById("standard-basic").value)
        props.setActiveTab("Results")
        try {
            let res = await axios({
                method: 'post',
                headers: { "Content-Type": "application/json" },
                url: 'http://localhost:5000/testpost',
                data: {
                    url: document.getElementById("standard-basic").value,
                    vulnerabilities: state
                }
            });
            clear()
            console.log(res)
            

        } catch (error) {
            console.log(error)
        }
    }

    return (
        <Grid
            container
            spacing={0}
            direction="column"
            alignItems="center"
        >
            <Grid item>
                <Card className={classes.card} variant="outlined">
                    <CardContent>
                        <Typography className={classes.title} color="textSecondary" gutterBottom>
                            Enter URL
                        </Typography>
                        <div>
                            <List>
                                <ListItem className={classes.listitem}>

                                    <TextField className={classes.textfield} id="standard-basic" label="domain or subdomain" />
                                </ListItem>
                                <ListItem className={classes.listitem}>

                                    <FormControl component="fieldset">
                                        <FormLabel component="legend">Select Vulnerability</FormLabel>
                                        <FormGroup>
                                            <FormControlLabel
                                                control={<Switch checked={state.xss} onChange={handleChange} name="xss" />}
                                                label="Cross Site Scripting"
                                            />
                                            <FormControlLabel
                                                control={<Switch checked={state.sqli} onChange={handleChange} name="sqli" />}
                                                label="SQL Injection"
                                            />
                                            <FormControlLabel
                                                control={<Switch checked={state.cj} onChange={handleChange} name="cj" />}
                                                label="Click Jacking"
                                            />
                                            <FormControlLabel
                                                control={<Switch checked={state.sdt} onChange={handleChange} name="sdt" />}
                                                label="Sub Domain Takeover"
                                            />
                                            <FormControlLabel
                                                control={<Switch checked={state.csrf} onChange={handleChange} name="csrf" />}
                                                label="Cross Site Request Forgery"
                                            />
                                        </FormGroup>
                                        <FormHelperText>choose all that are to be checked</FormHelperText>
                                    </FormControl>
                                </ListItem>
                            </List>

                        </div>

                    </CardContent>
                    <CardActions>
                        <Button className={classes.button} onClick={handleSubmit} variant="contained" color="primary" size="small">Send</Button>
                    </CardActions>
                </Card>

            </Grid>
        </Grid>
    );
}
