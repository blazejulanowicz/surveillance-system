import React, { useEffect, useState } from "react";
import SettingsApplicationsIcon from '@mui/icons-material/SettingsApplications';
import { Modal, Switch, Typography, Box, IconButton, TextField, Button } from "@mui/material";
import AdapterDateFns from '@mui/lab/AdapterDateFns';
import LocalizationProvider from '@mui/lab/LocalizationProvider';
import TimePicker from '@mui/lab/TimePicker';

const SettingsModal = ({ sx, alarmState, setAlarmState}) => {

    const [isOpen, setIsOpen] = useState(false);
    const [isArmed, setIsArmed] = useState(alarmState.status === 'armed')
    const [startTime, setStartTime] = useState();
    const [endTime, setEndTime] = useState();

    useEffect(() => {
        setIsArmed(alarmState.status === 'armed')

        let d = new Date();
        let [hours, minutes] = alarmState.start_time.split(':');
        d.setHours(+hours);
        d.setMinutes(minutes);
        setStartTime(d)

        let d2 = new Date();
        let [hours2, minutes2] = alarmState.end_time.split(':');
        d2.setHours(+hours2);
        d2.setMinutes(minutes2);
        setEndTime(d2)
    }, [alarmState]);

    const style = {
        position: 'absolute',
        top: '50%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        width: 400,
        bgcolor: 'background.paper',
        boxShadow: 24,
        p: 4,
    };

    const setNewAlarm = () => {
        setAlarmState({
            'status': isArmed ? 'armed' : 'disarmed',
            'start_time': startTime.toLocaleTimeString(),
            'end_time': endTime.toLocaleTimeString()
        });
        setIsOpen(false);
    };

    return (
        <Box sx={sx}>
            <IconButton onClick={() => setIsOpen(true)}>
                <SettingsApplicationsIcon />
            </IconButton>
            <Modal open={isOpen} onClose={() => setIsOpen(false)}>
                <Box sx={style}>
                    <Typography id="modal-modal-title" variant="h6" component="h2">
                        ALARM SETTINGS
                    </Typography>
                    <Box>
                        <Typography>Alarm ARMED</Typography>
                        <Switch checked={isArmed} onChange={(event) => setIsArmed(event.target.checked)}/>
                    </Box>
                    <LocalizationProvider dateAdapter={AdapterDateFns}>
                        <TimePicker
                            label="Start time"
                            value={startTime}
                            onChange={(newValue) => {
                                setStartTime(newValue);
                            }}
                            renderInput={(params) => <TextField {...params} />}
                        />
                    </LocalizationProvider>
                    <LocalizationProvider dateAdapter={AdapterDateFns}>
                        <TimePicker
                            label="End time"
                            value={endTime}
                            onChange={(newValue) => {
                                console.log(newValue);
                                setEndTime(newValue);
                            }}
                            renderInput={(params) => <TextField {...params} />}
                        />
                    </LocalizationProvider>
                    <Button onClick={setNewAlarm}>OK</Button>
                </Box>
            </Modal>
        </Box>
    );
};

export default SettingsModal;