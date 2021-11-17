import React, { useEffect, useState } from "react";
import { AppBar, Box, Paper, Toolbar, Typography } from '@mui/material';
import SettingsModal from "./SettingsModal";


const Mainbar = () => {

    const [alarmInfo, setAlarmInfo] = useState({ status: '', start_time: '', end_time: '' })

    const getAlarmInfo = () => {
        const requestOptions = {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' },
        };
        fetch('/api/get_alarm_info', requestOptions)
            .then(response => response.json())
            .then(data => setAlarmInfo(data));
    };

    const setAlarmState = (alarmState) => {
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(alarmState)
        };
        fetch('/api/set_alarm_info', requestOptions)
            .then(response => getAlarmInfo())
    };

    useEffect(() => {
        getAlarmInfo();
    }, []);

    return (
        <AppBar>
            <Toolbar>
                <Typography variant="h4" color="inherit" noWrap>
                    SURVEILLANCE SYSTEM
                </Typography>
                <Box sx={{
                    display: 'flex',
                    flexDirection: 'row',
                    alignItems: 'center'
                }}>
                    <Paper sx={{
                        marginLeft: 1,
                        marginRight: 5,
                        padding: '5px 20px',
                        border: 1,
                        borderColor: alarmInfo.status === 'armed' ? 'red' : 'green',
                        backgroundColor: alarmInfo.status === 'armed' ? 'red' : 'green',
                        color: 'white',
                    }}>
                        <b>{alarmInfo.status.toUpperCase()}</b>
                    </Paper>
                    <Box sx={{
                        display: 'flex',
                        flexDirection: 'column',
                        padding: '5px 20px',
                        border: 1,
                        borderColor: 'white',
                    }}>
                        <Typography sx={{ textAlign: 'center' }}><i>ACTIVE TIME</i></Typography>
                        <Typography sx={{ textAlign: 'center' }} variant="h6" color="inherit">{alarmInfo.start_time} - {alarmInfo.end_time}</Typography>
                    </Box>
                </Box>
                <Box style={{ flexGrow: 1 }} />
                <Box sx={{
                    display: 'flex',
                    flexDirection: 'row',
                    alignItems: 'center'
                }}>
                    <SettingsModal sx={{
                        display: 'flex',
                        flexDirection: 'column',
                        padding: '5px 20px',
                    }} alarmState={alarmInfo} setAlarmState={setAlarmState}/>
                </Box>
            </Toolbar>
        </AppBar>
    );
};

export default Mainbar;