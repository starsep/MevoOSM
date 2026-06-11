from typing import Dict, List, Tuple, cast

import overpy
from diskcache import Cache

from configuration import OVERPASS_URL, cacheDirectory
from urllib.request import Request

cacheOverpass = Cache(str(cacheDirectory / "overpass"))


# Workaround from https://github.com/DinoTools/python-overpy/issues/134#issuecomment-4604161798
def createOverpy(url: str | None = None) -> overpy.Overpass:
    if url is None:
        url = 'https://overpass-api.de/api/interpreter'
    req = Request(url)
    req.add_header('Referer', 'https://overpass-api.eu/')
    req.add_header('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
    req.add_header('Origin', 'https://overpass-turbo.eu')
    req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.3')
    return overpy.Overpass(url=req)  # type: ignore  # openurl() accepts Request

overpassApi = createOverpy(OVERPASS_URL)

@cacheOverpass.memoize()
def fetchOverpassData(
    placeName: str, bbox: Tuple[float, float, float, float]
) -> overpy.Result:
    (minLat, minLon, maxLat, maxLon) = bbox
    query = f"""
    [out:xml][timeout:250];
    area[admin_level=4][name="{placeName}"]->.searchArea;
    (
        nwr[amenity=bicycle_rental](area.searchArea);
        nwr[amenity=bicycle_rental]({minLat}, {minLon}, {maxLat}, {maxLon});
        nwr[amenity=bicycle_parking]["disused:amenity"=bicycle_rental](area.searchArea);
        nwr[amenity=bicycle_parking]["disused:amenity"=bicycle_rental]({minLat}, {minLon}, {maxLat}, {maxLon});
    );
    (._;>;);
    out body;
    """
    return overpassApi.query(query)


class OverpassParser:
    def __init__(self):
        self.ways: Dict[int, overpy.Way] = {}
        self.nodes: Dict[int, overpy.Node] = {}
        self.elements: List[overpy.Element] = []

    def fetchData(self, placeName: str, bbox: Tuple[float, float, float, float]):
        data: overpy.Result = fetchOverpassData(placeName, bbox)
        self.ways = {way.id: way for way in data.ways}
        self.nodes: Dict[int, overpy.Node] = {node.id: node for node in data.nodes}
        self.elements: List[overpy.Element] = cast(
            List[overpy.Element], list(self.nodes.values())
        ) + list(self.ways.values())

    def find(self, iD: int, mode: str = "n"):
        if mode == "n":
            return self.nodes.get(iD)
        elif mode == "w":
            return self.ways.get(iD)
        return None
