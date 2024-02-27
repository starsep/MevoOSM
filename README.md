Compares data of Meveo and OpenStreetMap.

Code based on [RooveeOSM](https://github.com/starsep/RooveeOSM)

Website at https://starsep.com/MevoOSM/

## Docker
```
docker build -t mevoosm .
docker run --rm \
    -v "$(pwd)/cache:/app/cache" \
    --env GITHUB_USERNAME=example \
    --env GITHUB_TOKEN=12345 \
    --env TZ=Europe/Warsaw \
    -t mevoosm
```
