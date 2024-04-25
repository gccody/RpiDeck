import React, { useEffect, useState } from 'react';
import { GridComponent } from './components/GridComponent';
import { WidgetComponent } from './components/WidgetComponent';
import { GridData } from './types';
import * as api from './utils/api';
import { createRoot } from 'react-dom/client';

function App() {
    const [data, setData] = useState<GridData | null>(null);
    const [page, setPage] = useState(0);
    const [loading, setLoading] = useState(true);
    const [widgets, setWidgets] = useState<JSX.Element[]>([]);
    const [noData, setNoData] = useState(false);

    useEffect(() => {
        api.getGridData().then((response) => {
            setData(response.data);
        }).catch((error) => {
            const data = localStorage.getItem('data');
            if (!data) {
                return setNoData(true);
            }
            setData(JSON.parse(data));
        });
    }, []);

    useEffect(() => {
        if (data) {
            localStorage.clear();
            localStorage.setItem('data', JSON.stringify(data));
            const widgetComponents = data.widgets[page].map((widget, i) => {
                return (
                    <WidgetComponent
                        id={widget.id}
                        key={i}
                        rowSpan={widget.rowSpan}
                        columnSpan={widget.columnSpan}
                        x={widget.x}
                        y={widget.y}
                        image={widget.image}
                        onClick={ undefined }
                    />
                );
            });
            
            const grid: Array<Array<number>> = [];
            
            for (let i = 0; i < data?.rows ?? 0; i++) {
                grid.push(new Array(data?.columns ?? 0).fill(-1));
            }
            
            data.widgets[page].forEach((widget) => {
                for (let i = widget.y; i < widget.y + widget.rowSpan; i++) {
                    for (let j = widget.x; j < widget.x + widget.columnSpan; j++) {
                        grid[i-1][j-1] = widget.id;
                    }
                }
            });
            

            for (let i = 0; i < data.rows; i++) {
                for (let j = 0; j < data.columns; j++) {
                    if (grid[i][j] === -1) {
                        widgetComponents.push(
                            <WidgetComponent
                                id={0}
                                key={`placeholder-${i}-${j}`}
                                rowSpan={1}
                                columnSpan={1}
                                x={j+1}
                                y={i+1}
                            />
                        );
                    }
                }
            }
            setLoading(false);
            setWidgets(widgetComponents);
        }

        
    }, [data, page]);

    useEffect(() => {
        if (noData) {
            const interval = setInterval(() => {
                api.getGridData().then((response) => {
                    setData(response.data);
                    setNoData(false);
                    clearInterval(interval);
                }).catch((error) => {
                    return;
                });
            }, 5000);
        }

    }, [noData]);

    if (noData) {
        return (
            <div
            style={{
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                height: '100vh',
                userSelect: 'none'
            }}>
                <h1 style={{
                    color: 'white',
                }}>
                    No Data Found
                </h1>
            </div>
        );
    }

  return (
    <div>
        {loading ? (
            <div
            style={{
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                height: '100vh',
                userSelect: 'none'
            }}>
                <h1 style={{
                    color: 'white',
                }}>
                    Loading...
                </h1>
            </div>
        ) : (
            <GridComponent columns={data?.columns ?? 0} rows={data?.rows ?? 0}>
                {widgets}
            </GridComponent>
        )}
    </div>
  );
}

const root = createRoot(document.body);
root.render(
    <div className="app">
      <App />
    </div>
);



