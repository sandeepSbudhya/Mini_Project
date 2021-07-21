import React, { useEffect } from 'react';
import { Card, CardContent, makeStyles } from "@material-ui/core"
import Grid from "@material-ui/core/Grid"
// import { useEffect } from "react"
import CircularProgress from '@material-ui/core/CircularProgress';
import Button from '@material-ui/core/Button';
import axios from 'axios'

const useStyles = makeStyles(() => ({
    errormessage: {
        color: "red"
    }
}))




export default function Results(props) {
    const classes = useStyles();
    const [sd, putsd] = React.useState([])
    const [l, putl] = React.useState([])
    const [error, puterror] = React.useState("")
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
        if (props.results === "true") {
            handleSnapshot()
        }
    }, [props.results])

    // const classes = useStyles()
    return (
        <div>
            {error && <Grid container justifyContent={"center"}>
                <h3 className={classes.errormessage}>{error}</h3>

            </Grid>}
            <Grid container spacing={1} justifyContent={"center"}>
                <Grid item xs={1}>
                    {props.results === "false" && <CircularProgress />}
                </Grid>
                {/* <Grid item xs={3}>
                    <Button onClick={handleSnapshot}>Show</Button>
                </Grid> */}
                <Grid item xs={3}>
                    <h4 hidden={props.results === "false" ? true : false}> Subdomains </h4>

                    <Card>
                        <CardContent>
                            {sd.map((d) => {
                                return (<div>
                                    {d}
                                </div>)
                            })}
                        </CardContent>
                    </Card>

                </Grid>
                <Grid item xs={6}>
                    <h4 hidden={props.results === "false" ? true : false}> Links </h4>

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