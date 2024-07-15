import 'ol/ol.css'

import React, { useRef, useEffect, useState } from 'react'

import { Map, View } from 'ol'
import OSM from 'ol/source/OSM'
import VectorSource from 'ol/source/Vector'
import TileLayer from 'ol/layer/Tile'
import VectorLayer from 'ol/layer/Vector'
import Toolbar from './Toolbar'
import useDraw, { GeometryT } from '../hooks/useDraw'
import useBoundaryRectangle from '../hooks/useBoundaryRectangle'

interface MapComponentProps {}

const MapComponent: React.FC<MapComponentProps> = ({}) => {
  const mapElement = useRef<HTMLDivElement | null>(null)
  const [map, setMap] = useState<Map | null>(null)

  const source = useRef<VectorSource>(new VectorSource({ wrapX: false }))
  const [geometry, setGeometry] = useState<GeometryT>('Point')

  const { handleEndGeometry, handleUndo, handleClear } = useDraw({ map, geometry, source })

  // Использование хука для добавления прямоугольника на карту
  const sourceBoundary = useRef<VectorSource>(new VectorSource({ wrapX: false }))
  useBoundaryRectangle(sourceBoundary.current)

  useEffect(() => {
    if (mapElement.current) {
      const view = new View({
        projection: 'EPSG:4326',
        center: [160.5, 55.5],
        zoom: 9.8,
      })

      const raster = new TileLayer({ source: new OSM() })
      const vector = new VectorLayer({ source: source.current })
      const vectorBoundary = new VectorLayer({ source: sourceBoundary.current })

      const newMap = new Map({
        layers: [raster, vectorBoundary, vector],
        target: mapElement.current,
        view: view,
      })
      console.log('bind map')
      setMap(newMap)
      return () => {
        console.log('unbind map')
        newMap.setTarget(undefined)
      }
    }
  }, [])

  return (
    <>
      <div style={{ width: '100%', position: 'relative' }}>
        <Toolbar
          geometry={geometry}
          setGeometry={setGeometry}
          handleUndo={handleUndo}
          handleEndGeometry={handleEndGeometry}
          handleClear={handleClear}
        />
        <div ref={mapElement} style={{ width: '100%', height: '95vh' }}></div>
      </div>
    </>
  )
}

export default MapComponent
