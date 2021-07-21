import React, { useEffect } from 'react';
import { Card, CardContent, makeStyles } from "@material-ui/core"
import Grid from "@material-ui/core/Grid"
import CircularProgress from '@material-ui/core/CircularProgress';
import CardActions from '@material-ui/core/CardActions';
import FormLabel from '@material-ui/core/FormLabel';
import FormControl from '@material-ui/core/FormControl';
import FormGroup from '@material-ui/core/FormGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import FormHelperText from '@material-ui/core/FormHelperText';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import Switch from '@material-ui/core/Switch';
import Button from '@material-ui/core/Button';
import axios from 'axios'

const useStyles = makeStyles(() => ({
    sdcard:{
        marginBottom:10
    },
    errormessage: {
        color: "red"
    },
    divstyle: {
        marginLeft: 25
    },
    card: {
        width: 500,
        padding: 20
    },
    listitem: {
        padding: 15
    },
    title: {
        fontSize: 25,
        marginLeft: 150
    },
    pos: {
        marginBottom: 12,
    },
    button: {
        marginBottom:10,
        marginLeft: 25,
    },
    textfield: {
        width: 400,
        justifyContent: 'center'
    }
}))




export default function Links(props) {
    const classes = useStyles();
    const [sd, putsd] = React.useState([])
    const [l, putl] = React.useState([])
    const [error, puterror] = React.useState("")
    const [state, setState] = React.useState({
        xss: false,
        cors: false,
        cj: false,
        sdt: false,
        csrf: false

    });

    const handleChange = (event) => {
        setState({ ...state, [event.target.name]: event.target.checked });
    };
    const handleSnapshot = async () => {
        try {
            const res = await axios({
                method: 'get',
                url: 'http://localhost:5000/test',
            })
            if (res.status === 200) {
                console.log(res.data)
                putsd(res.data.subdomains)
                putl(res.data.links)
            }

        } catch (error) {
            console.log(error)
            puterror("Something went wrong please restart the test")
        }
    }

    useEffect(() => {
        if (props.links === "true") {
            handleSnapshot()
        }
    }, [props.links])

    // const classes = useStyles()
    return (
        <div>
            {error && <Grid container justifyContent={"center"}>
                <h3 className={classes.errormessage}>{error}</h3>

            </Grid>}
            <Grid container spacing={1} justifyContent={"center"}>
                <Grid item xs={1}>
                    {props.links === "false" && <CircularProgress />}
                </Grid>
                <Grid item xs={3}>
                    <h4 hidden={props.links === "false" ? true : false}> Subdomains </h4>

                    <Card className={classes.sdcard}>
                        <CardContent>
                            {sd.map((d) => {
                                return (<div>
                                    {d}
                                </div>)
                            })}
                        </CardContent>
                    </Card>
                    {props.links === "true" && <Card>
                        <CardContent>
                            <List>
                                <ListItem className={classes.listitem}>

                                    <FormControl component="fieldset">
                                        <FormLabel component="legend">Select Vulnerability</FormLabel>
                                        <FormGroup>
                                            <FormControlLabel
                                                control={<Switch checked={state.xss} onChange={handleChange} name="xss" />}
                                                label="Cross Site Scripting"
                                            />
                                            <FormControlLabel
                                                control={<Switch checked={state.sqli} onChange={handleChange} name="cors" />}
                                                label="CORS"
                                            />
                                            <FormControlLabel
                                                control={<Switch checked={state.cj} onChange={handleChange} name="cj" />}
                                                label="Click Jacking"
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
                        </CardContent>
                        <CardActions>
                            <Button variant="contained" color="primary" size="small" className={classes.button}>Scan</Button>
                        </CardActions>

                    </Card>}

                </Grid>
                <Grid item xs={6}>
                    <h4 hidden={props.links === "false" ? true : false}> Links </h4>

                    <Card>
                        <CardContent>
                            {l.map((link) => {
                                return (
                                    <div>{link !== "#" ? link : <p></p>}</div>
                                )
                            })}
                        </CardContent>
                    </Card>

                </Grid>

            </Grid>
        </div>
    )
}