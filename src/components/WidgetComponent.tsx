import React, { useState } from 'react';
import Lottie from 'react-lottie';
import animationData from '../assets/GreenCheck.json';

type WidgetProps = {
    id: number;
    x: number;
    y: number;
    rowSpan: number;
    columnSpan: number;
    image?: string;
    onClick?: () => void;
};

export const WidgetComponent: React.FC<WidgetProps> = ({
    id, x, y, rowSpan, columnSpan, image, onClick
}) => {
    const [showLottie, setShowLottie] = useState(false);

    const gridRow = `${y} / span ${rowSpan}`;
    const gridColumn = `${x} / span ${columnSpan}`;

    const defaultOptions = {
        loop: false,
        animationData: animationData,
        rendererSettings: {
            preserveAspectRatio: 'xMidYMid meet',
        }
    };
    const handleClick = () => {
        if (!onClick) return;
        setShowLottie(true);
        onClick();
    };

    return (
        <div
            style={{
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                gridRow: gridRow,
                gridColumn: gridColumn,
                backgroundColor: 'black',
                borderColor: 'lightgrey',
                borderWidth: '1px',
                borderStyle: 'solid',
                borderRadius: '5px',
                color: 'white',
                position: 'relative',
                overflow: 'hidden',
            }}
            onClick={handleClick}
        >
            {showLottie ? (
                <Lottie options={defaultOptions} eventListeners={[{ eventName: "complete", callback: () => setShowLottie(false) }]} isClickToPauseDisabled={true} />
            ) : (
                image && (
                    <img src={image} alt="placeholder" style={{
                        width: '100%',
                        height: '100%',
                        objectFit: 'cover',
                        display: showLottie ? 'none' : 'block',
                    }} />
                )
            )}
        </div>
    );
};
