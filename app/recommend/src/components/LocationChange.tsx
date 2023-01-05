import { useEffect, useRef } from 'react'
import { useLocation } from 'react-router-dom'

const useLocationChange = (callback: () => void) => {
  const refCallback = useRef<undefined | ((location: Location) => void)>()
  const location = useLocation()

  useEffect(() => {
    refCallback.current = callback
  }, [callback])

  // ロケーションに変更があったときに処理実行
  useEffect(() => {
    if (refCallback.current) {
      refCallback.current(location)
    }
  }, [location])
}

export default useLocationChange