import { useEffect, useRef } from 'react'
import Draw, { DrawEvent } from 'ol/interaction/Draw'
import VectorSource from 'ol/source/Vector'
import { Feature } from 'ol'
import { Point, LineString, Polygon, Geometry } from 'ol/geom'
import { Map as OlMap } from 'ol'
import WKT from 'ol/format/WKT'
import { Style, Text, Fill, Stroke } from 'ol/style'

export type GeometryT = 'Point' | 'LineString' | 'Polygon'

const apiUrlBase = import.meta.env.VITE_API_URL_BASE || ''
const apiPathGetElevation = import.meta.env.VITE_API_PATH_GET_ELEVATION || ''
if (!apiUrlBase || !apiPathGetElevation) {
  alert('API URL base or path for elevation is not defined')
  throw new Error('API URL base or path for elevation is not defined')
}
const urlElevation = new URL(apiPathGetElevation, apiUrlBase)

const getCoordinates = (geometry: Geometry): number[][] => {
  if (geometry instanceof Point) {
    return [geometry.getCoordinates()]
  } else if (geometry instanceof LineString) {
    return geometry.getCoordinates()
  } else if (geometry instanceof Polygon) {
    return geometry.getCoordinates().flat()
  } else {
    throw new Error('Unsupported geometry type')
  }
}

// Создание стиля текста для высоты
const textStyle = new Text({
  textAlign: 'center',
  textBaseline: 'top',
  font: '12px Arial',
  fill: new Fill({ color: 'black' }),
  stroke: new Stroke({ color: 'white', width: 2 }),
  text: '',
})

interface UseDrawProps {
  map: OlMap | null
  geometry: GeometryT
  source: React.MutableRefObject<VectorSource>
}

interface FeatureInfo {
  feature: Feature
  elevations: Feature[]
}

const wktFormat = new WKT()

const useDraw = ({ map, geometry, source }: UseDrawProps) => {
  const draw = useRef<Draw | null>(null)
  const curFeature = useRef<Feature | null>(null)
  const features = useRef<FeatureInfo[]>([])

  useEffect(() => {
    if (map) {
      if (draw.current) map.removeInteraction(draw.current)

      const newDraw = new Draw({
        source: source.current,
        type: geometry,
      })
      newDraw.on('drawstart', startGeometry)
      newDraw.on('drawend', endGeometry)

      map.addInteraction(newDraw)
      draw.current = newDraw

      return () => {
        map.removeInteraction(newDraw)
      }
    }
  }, [geometry, map])

  const startGeometry = (event: DrawEvent) => {
    curFeature.current = event.feature
  }

  const endGeometry = async (event: DrawEvent) => {
    try {
      const feature = event.feature
      const newFeatureInfo: FeatureInfo = { feature: feature, elevations: [] }
      curFeature.current = null

      const geometry = feature.getGeometry()
      if (!geometry) return

      urlElevation.searchParams.set('wkt', wktFormat.writeGeometry(geometry))
      const response = await fetch(urlElevation.toString())
      if (!response.ok) throw new Error('Failed to fetch elevation data')
      const data = await response.json()
      if (!data.wkt) throw new Error('Invalid response from server')

      const returnedCoordinates = getCoordinates(wktFormat.readGeometry(data.wkt) as Geometry)
      if (!Array.isArray(returnedCoordinates)) throw new Error('Invalid coordinates format')

      // Применение стиля к каждой точке
      returnedCoordinates.forEach((coordinate) => {
        if (!Array.isArray(coordinate) || coordinate.length < 3) {
          throw new Error('Invalid coordinate format')
        }
        const [x, y, z] = coordinate
        const text = z.toString()
        textStyle.setText(text)
        const pointFeature = new Feature(new Point([x, y]))
        pointFeature.setStyle(new Style({ text: textStyle.clone(), zIndex: 1 }))
        source.current.addFeature(pointFeature)

        newFeatureInfo.elevations.push(pointFeature)
      })
      features.current.push(newFeatureInfo)
    } catch (error) {
      console.error('Error handling draw end:', error)
    }
  }

  const handleEndGeometry = () => {
    draw.current?.finishDrawing()
  }

  const handleUndo = () => {
    if (!draw.current) return
    if (curFeature.current) {
      draw.current.removeLastPoint()
      if ((curFeature.current.getGeometry() as LineString).getCoordinates().length == 1) {
        curFeature.current = null
      }
    } else {
      const delFeature = features.current.pop()
      if (delFeature) {
        source.current.removeFeature(delFeature.feature)
        delFeature.elevations.forEach((elevation) => source.current.removeFeature(elevation))
      }
    }
  }

  const handleClear = () => {
    source.current.clear()
    features.current = []
  }

  return {
    handleEndGeometry,
    handleUndo,
    handleClear,
  }
}

export default useDraw
