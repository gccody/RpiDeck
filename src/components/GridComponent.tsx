import React, { useEffect, useState } from 'react';

type GridProps = {
    columns: number;
    rows: number;
    children: React.ReactNode;
};

export const GridComponent: React.FC<GridProps> = ({ columns, rows, children }) => {
    const [baseUnit, setBaseUnit] = useState('100px'); // Initial base unit size
    const gapSize = 10; // Gap size between grid items
    const paddingSize = 20; // Padding size for the grid container

    useEffect(() => {
        const updateLayout = () => {
            // Calculate the base unit based on the viewport width
            const screenWidth = window.innerWidth;
            // Accounting for gaps between columns and padding
            const totalGapSizeWidth = gapSize * (columns - 1) + paddingSize * 2;
            const availableWidth = screenWidth - totalGapSizeWidth;
            // Calculate the width of each unit based on the available width and number of columns
            const unitSizeWidth = availableWidth / columns;

            const screenHeight = window.innerHeight;
            const totalGapSizeHeight = gapSize * (rows - 1) + paddingSize * 2;
            const availableHeight = screenHeight - totalGapSizeHeight;
            const unitSizeHeight = availableHeight / rows;

            // Adjust baseUnit to adjust for slight viewport width variations (.5vw for some breathing room)
            setBaseUnit(`calc(${Math.min(unitSizeHeight, unitSizeWidth)}px - .5vw)`);
        };

        // Update layout on window resize and initially
        window.addEventListener('resize', updateLayout);
        updateLayout(); // Initial call to set layout

        // Clean up event listener on component unmount
        return () => window.removeEventListener('resize', updateLayout);
    }, [columns]); // Dependency on columns only since rows are now static

    return (
        <div 
            style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                height: '100vh',
                width: '100vw',
                boxSizing: 'border-box',
                userSelect: 'none' 
            }}
        >
            <div
                style={{
                    display: 'grid',
                    gridTemplateColumns: `repeat(${columns}, ${baseUnit})`,
                    gridTemplateRows: `repeat(${rows}, ${baseUnit})`, // Use the calculated number of rows
                    gap: '10px',
                }}
            >
                {children}
            </div>
        </div>
    );
};
