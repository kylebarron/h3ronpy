import geopandas as gpd
import pandas as pd
import pyarrow as pa
import shapely

from h3ronpy import DEFAULT_CELL_COLUMN_NAME, H3_CRS, ContainmentMode
from h3ronpy import util as _arrow_util
from h3ronpy import vector as _av
from h3ronpy.vector import cells_to_wkb_polygons


def cells_dataframe_to_geodataframe(
    df: pd.DataFrame, cell_column_name: str = DEFAULT_CELL_COLUMN_NAME
) -> gpd.GeoDataFrame:
    """
    Convert a dataframe with a column containing cells to a geodataframe

    :param df: input dataframe
    :param cell_column_name: name of the column containing the h3 indexes
    :return: GeoDataFrame
    """
    wkb_polygons = cells_to_wkb_polygons(df[cell_column_name])
    geometry = shapely.from_wkb(wkb_polygons)
    return gpd.GeoDataFrame(df, geometry=geometry, crs=H3_CRS)


def geodataframe_to_cells(
    gdf: gpd.GeoDataFrame,
    resolution: int,
    containment_mode: ContainmentMode = ContainmentMode.ContainsCentroid,
    compact: bool = False,
    cell_column_name: str = DEFAULT_CELL_COLUMN_NAME,
) -> pd.DataFrame:
    """
    Convert a `GeoDataFrame` to H3 cells while exploding all other columns according to the number of cells derived
    from the rows geometry.

    The conversion of GeoDataFrames is parallelized using the available CPUs.

    The duplication of all non-cell columns leads to increased memory requirements. Depending on the use-case
    some of the more low-level conversion functions should be preferred.

    :param gdf:
    :param resolution: H3 resolution
    :param containment_mode: Containment mode used to decide if a cell is contained in a polygon or not.
            See the ContainmentMode class.
    :param compact: Compact the returned cells by replacing cells with their parent cells when all children
            of that cell are part of the set.
    :param cell_column_name:
    :return:
    """
    cells = _av.wkb_to_cells(
        gdf.geometry.to_wkb(),
        resolution,
        containment_mode=containment_mode,
        compact=compact,
        flatten=False,
    )
    table = pa.Table.from_pandas(pd.DataFrame(gdf.drop(columns=gdf.geometry.name))).append_column(
        cell_column_name, cells
    )
    return _arrow_util.explode_table_include_null(table, cell_column_name).to_pandas().reset_index(drop=True)


__all__ = [
    cells_dataframe_to_geodataframe.__name__,
    geodataframe_to_cells.__name__,
]
