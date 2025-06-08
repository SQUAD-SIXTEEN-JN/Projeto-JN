import type React from "react"
import type { Metadata } from "next"
import { Geist, Geist_Mono, Roboto, Montserrat, Inter } from "next/font/google"
import "./globals.css"

// Configuração das fontes
const inter = Inter({
  subsets: ["latin"],
  variable: "--font-sans",
})

const roboto = Roboto({
  subsets: ["latin"],
  weight: ["400", "500", "700"],
  variable: "--font-roboto",
})

const montserrat = Montserrat({
  subsets: ["latin"],
  variable: "--font-montserrat",
})

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
})

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
})

// Metadados da página
export const metadata: Metadata = {
  title: "Jotanunes - Plataforma de Aprendizado",
  description: "Plataforma educacional da Jotanunes Construtora",
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html
      lang="pt-BR"
      className={`${inter.variable} ${geistSans.variable} ${geistMono.variable} ${roboto.variable} ${montserrat.variable}`}
    >
      <body className="font-sans antialiased">{children}</body>
    </html>
  )
}
