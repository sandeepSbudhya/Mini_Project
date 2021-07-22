import React, { useEffect } from 'react';
import { Card, CardContent, makeStyles } from "@material-ui/core"
import Grid from "@material-ui/core/Grid"
import CircularProgress from '@material-ui/core/CircularProgress'

const useStyles = makeStyles(() => ({
    sdcard: {
        marginBottom: 10
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
        marginBottom: 10,
        marginLeft: 25,
    },
    textfield: {
        width: 400,
        justifyContent: 'center'
    }
}))




export default function Results(props) {
    const classes = useStyles();
    const [l, putl] = React.useState([])
    const [error, puterror] = React.useState("")

    const handleSnapshot = async () => {
        putl(props.vulns)
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
                <Grid item xs={6}>
                    <h4 hidden={props.results === "false" ? true : false}> Results </h4>

                    <Card>
                        <CardContent>
                            {Object.keys(l).map((link,value) => {
                                return (
                                    <div >{link !== "#" ? <p>{link}</p> : <p></p>}</div>
                                )
                            })}
                        </CardContent>
                    </Card>

                </Grid>

            </Grid>
        </div>
    )
}