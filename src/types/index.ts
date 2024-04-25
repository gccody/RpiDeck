export interface Widget {
    id: number,
    rowSpan: number,
    columnSpan: number,
    x: number,
    y: number,
    image?: string
}

export interface GridData {
    columns: number,
    rows: number,
    widgets: Array<Array<Widget>>
}