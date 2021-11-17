import './App.css';
import { createTheme, CssBaseline, ThemeProvider } from '@mui/material';
import Mainbar from './components/Mainbar';
import ThumbnailList from './components/ThumbnailList';
import { useEffect, useState } from 'react';

function App() {

  const theme = createTheme();
  const [videoData, setVideoData] = useState([]);

  const getVideoData = () => {
    const requestOptions = {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
    };
    fetch('/api/get_video_data', requestOptions)
        .then(response => response.json())
        .then(data => {setVideoData(data); console.log(data)})
  };

  useEffect(() => {
    getVideoData();
  }, []);

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
        <Mainbar />
        <ThumbnailList itemData={videoData}/>
    </ThemeProvider>  
  );
}

export default App;
