#[derive(Debug, thiserror::Error)]
pub enum Error {
    #[error(transparent)]
    InvalidCellIndex(#[from] h3o::error::InvalidCellIndex),

    #[error(transparent)]
    InvalidVertexIndex(#[from] h3o::error::InvalidVertexIndex),

    #[error(transparent)]
    InvalidDirectedEdgeIndex(#[from] h3o::error::InvalidDirectedEdgeIndex),

    #[error(transparent)]
    InvalidResolution(#[from] h3o::error::InvalidResolution),

    #[error(transparent)]
    InvalidLatLng(#[from] h3o::error::InvalidLatLng),

    #[error(transparent)]
    InvalidGeometry(#[from] h3o::error::InvalidGeometry),

    #[error(transparent)]
    CompactionError(#[from] h3o::error::CompactionError),

    #[error(transparent)]
    OutlinerError(#[from] h3o::error::OutlinerError),

    #[error(transparent)]
    Arrow2(#[from] arrow::error::ArrowError),

    #[error("not a UintArray")]
    NotAUint64Array,

    #[error("non-parsable CellIndex")]
    NonParsableCellIndex,

    #[error("non-parsable VertexIndex")]
    NonParsableVertexIndex,

    #[error("non-parsable DirectedEdgeIndex")]
    NonParsableDirectedEdgeIndex,

    #[error("Invalid WKB encountered")]
    InvalidWKB,

    #[error(transparent)]
    IO(#[from] std::io::Error),
}
