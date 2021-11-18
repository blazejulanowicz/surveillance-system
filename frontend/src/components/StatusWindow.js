import React from "react";
import { Box, Paper, Typography, Divider } from '@mui/material'

const StatusWindow = ({ alarmInfo }) => {

    return (
        <Paper sx={{
            position: 'fixed',
            bottom: 20,
            right: 20,
            display: 'flex',
            flexDirection: 'column',
            padding: 3
        }} elevation={4}>
            <Typography variant="h4" color="inherit">ALARM STATUS</Typography>
            <Divider />
            <Box sx={{
                paddingTop: 2,
                textAlign: 'center'
            }}>
                <Paper sx={{
                    padding: '5px 0',
                    marginBottom: 2,
                    border: 1,
                    borderColor: alarmInfo.status === 'armed' ? 'red' : 'green',
                    backgroundColor: alarmInfo.status === 'armed' ? 'red' : 'green',
                    color: 'white',
                }}>
                    <b>{alarmInfo.status.toUpperCase()}</b>
                </Paper>
                <Typography><i>Active between:</i></Typography>
                <Typography sx={{ textAlign: 'center' }} variant="h5" color="inherit"><b>{alarmInfo.start_time} - {alarmInfo.end_time}</b></Typography>
            </Box>
        </Paper>
    );

};

export default StatusWindow;