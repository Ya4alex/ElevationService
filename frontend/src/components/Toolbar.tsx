import { GeometryT } from '../hooks/useDraw'
import './Tollbar.css'
import React from 'react'

interface ToolbarProps {
  geometry: GeometryT
  setGeometry: (geometry: GeometryT) => void
  handleUndo: () => void
  handleEndGeometry?: () => void
  handleClear?: () => void
}

const Toolbar: React.FC<ToolbarProps> = ({ geometry, setGeometry, handleUndo, handleEndGeometry, handleClear }) => {
  return (
    <div id='toolbar'>
      <label>
        <span>Geometry:</span>
        <select
          style={{ boxSizing: 'content-box' }}
          onChange={(e: React.ChangeEvent<HTMLSelectElement>) => setGeometry(e.target.value as GeometryT)}
          value={geometry}>
          <option value='Point'>Point</option>
          <option value='LineString'>LineString</option>
          <option value='Polygon'>Polygon</option>
        </select>
      </label>
      <button onClick={handleClear}>Clear</button>
      <button onClick={handleUndo}>Undo</button>
      <button onClick={handleEndGeometry} className='highlight'>
        End geometry
      </button>
    </div>
  )
}

export default Toolbar
