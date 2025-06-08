"use client"
import { useEffect } from "react"

declare global {
  interface Window {
    chatbase?: any & {
      q?: any[]
      (command: string, ...args: any[]): void
      getState?: () => string
    }
  }
}

export default function Chatbot() {
  useEffect(() => {
    if (!window.chatbase || window.chatbase("getState") !== "initialized") {
      window.chatbase = ((...args: any[]) => {
        if (!window.chatbase!.q) window.chatbase!.q = []
        window.chatbase!.q.push(args)
      }) as typeof window.chatbase

      window.chatbase = new Proxy(window.chatbase, {
        get(target, prop) {
          if (prop === "q") return target.q
          return (...args: any[]) => (target as any)(prop, ...args)
        },
      })

      const onLoad = () => {
        const script = document.createElement("script")
        script.src = "https://www.chatbase.co/embed.min.js"
        script.id = "QRXEyDBpz9GT_P0efKbnw"
        script.setAttribute("domain", "www.chatbase.co")
        document.body.appendChild(script)
      }

      if (document.readyState === "complete") {
        onLoad()
      } else {
        window.addEventListener("load", onLoad)
      }
    }
  }, [])

  return <div id="chatbase-chatbot-container" />
}