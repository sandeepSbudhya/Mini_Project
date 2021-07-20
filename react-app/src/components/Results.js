import React from 'react';
import { Card, CardContent, makeStyles } from "@material-ui/core"
import Grid from "@material-ui/core/Grid"
// import { useEffect } from "react"
import CircularProgress from '@material-ui/core/CircularProgress';
import Button from '@material-ui/core/Button';
import axios from 'axios'
// const useStyles = makeStyles({

// })





export default function Results(props) {
    const handleSnapshot = async()=>{
        const res = await axios({
            method:'get',
            url:'http://localhost:5000/testpost',
        })
        if(res.status=== 200){
            console.log(res.data)
        }
    }
    
    // const classes = useStyles()
    return (
        <div>
            <h2></h2>
            <Grid container justifyContent={"center"}>
                <Grid item xs={6}>
                    {!props.results && <CircularProgress />}
                </Grid>
                <Grid item xs={3}>
                    <Button onClick={handleSnapshot}>Show</Button>
                </Grid>
                <Grid item xs={6}>
                    <div></div>
                    <Card>
                        <CardContent>
                            
                        </CardContent>
                    </Card>

                </Grid>

            </Grid>
        </div>
    )
}