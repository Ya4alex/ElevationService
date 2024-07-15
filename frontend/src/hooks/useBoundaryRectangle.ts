import { useEffect } from 'react'
import { Feature } from 'ol'
import { Polygon } from 'ol/geom'
import { Style, Stroke, Fill } from 'ol/style'
import VectorSource from 'ol/source/Vector'

const useBoundaryRectangle = (source: VectorSource) => {
  useEffect(() => {
    // Координаты прямоугольника
    const rectangleCoords = [
      [160, 55],
      [161, 55],
      [161, 56],
      [160, 56],
    ]

    // Координаты для инвертированного многоугольника (вся карта)
    const outerCoords = [
      [-180, -90],
      [180, -90],
      [180, 90],
      [-180, 90],
    ]

    const invertedRectangleCoords = [outerCoords, rectangleCoords]
    const invertedRectangle = new Polygon(invertedRectangleCoords)
    const invertedRectangleFeature = new Feature(invertedRectangle)

    // Применение стиля к инвертированному прямоугольнику
    invertedRectangleFeature.setStyle(
      new Style({
        stroke: new Stroke({
          color: 'blue',
          width: 1,
        }),
        fill: new Fill({
          color: 'rgba(0, 0, 255, 0.05)',
        }),
      }),
    )
    source.addFeature(invertedRectangleFeature)

    return () => {
      source.removeFeature(invertedRectangleFeature)
    }
  }, [source])
}

export default useBoundaryRectangle
