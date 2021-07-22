import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Card from '@material-ui/core/Card';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';
import TextField from '@material-ui/core/TextField';
import Grid from '@material-ui/core/Grid';
import axios from 'axios'

const useStyles = makeStyles({
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
        marginLeft: 25
    },
    textfield: {
        width: 400,
        justifyContent: 'center'
    }
});

export default function RunTest(props) {


    const classes = useStyles();

    const handleSubmit = async () => {
        // console.log(document.getElementById("standard-basic").value)
        props.setActiveTab("Links")

        try {

            props.linksArrive("false")
            let res = await axios({
                method: 'post',
                headers: { "Content-Type": "application/json" },
                url: 'http://localhost:5000/test',
                data: {
                    url: document.getElementById("standard-basic").value,
                }
            });

            // console.log(res.status)
            if (res.status === 200) {
                props.linksArrive("true")
            }


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

                        <TextField className={classes.textfield} id="standard-basic" label="domain or subdomain" />

                    </CardContent>
                    <CardActions>
                        <Grid
                            container
                            spacing={3}
                            direction="row">
                            <Grid item xs={3}>
                                <Button className={classes.button} disabled={props.links === "false"} onClick={handleSubmit} variant="contained" color="primary" size="small">Send</Button>
                            </Grid>

                        </Grid>
                    </CardActions>
                    {props.links === "false" && <div className={classes.divstyle}>
                        <p>Processing...      </p>
                    </div>}
                </Card>

            </Grid>
        </Grid>
    );
}
