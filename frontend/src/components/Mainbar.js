import React from "react";
import { AppBar, Box, Toolbar, Typography } from '@mui/material';
import SettingsModal from "./SettingsModal";


const Mainbar = ({ alarmInfo, setAlarmState }) => {

    return (
        <AppBar>
            <Toolbar>
                <Typography variant="h4" color="inherit" noWrap>
                    <b>SURVEILLANCE SYSTEM</b>
                </Typography>
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
                    }} alarmState={alarmInfo} setAlarmState={setAlarmState} />
                </Box>
            </Toolbar>
        </AppBar>
    );
};

export default Mainbar;