import './App.css';
import { createTheme, CssBaseline, ThemeProvider } from '@mui/material';
import Mainbar from './components/Mainbar';
import ThumbnailList from './components/ThumbnailList';
import { useEffect, useState } from 'react';
import StatusWindow from './components/StatusWindow';

function App() {

  const theme = createTheme();
  const [videoData, setVideoData] = useState([]);
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

  const getVideoData = () => {
    const requestOptions = {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    };
    fetch('/api/get_video_data', requestOptions)
      .then(response => response.json())
      .then(data => { setVideoData(data); console.log(data) })
  };

  useEffect(() => {
    getVideoData();
    getAlarmInfo();
  }, []);

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Mainbar alarmInfo={alarmInfo} setAlarmState={setAlarmState} />
      <ThumbnailList itemData={videoData} />
      <StatusWindow alarmInfo={alarmInfo} />
    </ThemeProvider>
  );
}

export default App;
