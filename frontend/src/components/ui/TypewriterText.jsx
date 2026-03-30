import { useState, useEffect } from 'react'

export default function TypewriterText({ text, speed = 50, onComplete }) {
  const [displayed, setDisplayed] = useState('')
  const [done, setDone] = useState(false)

  useEffect(() => {
    let i = 0
    setDisplayed('')
    setDone(false)

    const timer = setInterval(() => {
      if (i < text.length) {
        setDisplayed(text.slice(0, i + 1))
        i++
      } else {
        clearInterval(timer)
        setDone(true)
        onComplete?.()
      }
    }, speed)

    return () => clearInterval(timer)
  }, [text, speed])

  return (
    <span>
      {displayed}
      {!done && (
        <span className="inline-block w-0.5 h-[1em] bg-[#00FFFF] ml-1 animate-pulse" />
      )}
    </span>
  )
}
