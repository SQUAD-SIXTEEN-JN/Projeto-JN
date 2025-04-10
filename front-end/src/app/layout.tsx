  import type { Metadata } from "next";
  import { Geist, Geist_Mono, Roboto, Montserrat } from "next/font/google";
  import "./globals.css";

  const roboto = Roboto({
    subsets: ['latin'],
    variable: '--font-roboto',
  });

  const montserrat = Montserrat({
    subsets: ['latin'],
    variable: '--font-montserrat',
  });

  const geistSans = Geist({
    variable: "--font-geist-sans",
    subsets: ["latin"],
  });

  const geistMono = Geist_Mono({
    variable: "--font-geist-mono",
    subsets: ["latin"],
  });

  export const metadata: Metadata = {
    title: "Jotanunes Construtora",
    description: "Construtora Civil",
  };

  export default function RootLayout({
    children,
  }: Readonly<{
    children: React.ReactNode;
  }>) {
    return (
      <html lang="en" className={`${geistSans.variable} ${geistMono.variable} ${roboto.variable} ${montserrat.variable} `}>
        <body
          className={` antialiased`}
        >
          {children}
        </body>
      </html>
    );
  }
