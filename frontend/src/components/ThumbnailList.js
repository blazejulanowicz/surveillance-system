import React from "react";
import { ImageList, ImageListItem, ImageListItemBar, IconButton, Tooltip } from '@mui/material';
import DownloadIcon from '@mui/icons-material/Download';

const ThumbnailList = ({ itemData }) => {

    return (
        <ImageList sx={{ margin: 10 }}>
            {itemData.map((item) => (
                <ImageListItem key={item.detection_id} sx={{ height: 250 }}>
                    <img
                        src={`/api/get_thumbnail/${item.detection_id}?w=248&fit=crop&auto=format`}
                        srcSet={`/api/get_thumbnail/${item.detection_id}?w=248&fit=crop&auto=format&dpr=2 2x`}
                        alt={item.detection_id}
                        loading="lazy"
                        onClick={() => window.open(`/api/get_thumbnail/${item.detection_id}`)}
                        style={{ cursor: 'pointer', height: 400 }}
                    />
                    <ImageListItemBar
                        title={item.creation_date}
                        actionIcon={
                            <Tooltip title="Download video">
                                <IconButton
                                    sx={{ color: 'rgba(255, 255, 255, 0.54)' }}
                                    aria-label={`info about ${item.creation_date}`}
                                    onClick={() => window.open(`/api/download_video/${item.detection_id}`)}
                                >
                                    <DownloadIcon />
                                </IconButton>
                            </Tooltip>
                        }
                    />
                </ImageListItem>
            ))}
        </ImageList>
    );
};

export default ThumbnailList;