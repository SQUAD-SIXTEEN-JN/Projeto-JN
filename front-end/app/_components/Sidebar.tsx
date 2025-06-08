'use client'

import type React from "react"
import {
  Home,
  Search,
  BookOpen,
  FileText,
  ShoppingCart,
  MessageCircle,
  Settings,
  LogOut,
} from "lucide-react"
import Image from "next/image"
import { useState } from "react"
import clsx from "clsx"
import { useRouter } from "next/navigation"

const nomeUsuario = typeof window !== "undefined" ? localStorage.getItem('nomeUsuario') : null;

export function Sidebar({ activePage }: { activePage?: string }) {
  const [open, setOpen] = useState(false)
  const router = useRouter()

  return (
    <>
      {/* Sidebar */}
      <aside
        onMouseEnter={() => setOpen(true)}
        onMouseLeave={() => setOpen(false)}
        className={clsx(
          "fixed top-0 left-0 h-screen bg-[#D9D9D9] transition-all duration-300 z-50 flex flex-col justify-between shadow-md",
          open ? "w-[180px]" : "w-[60px]"
        )}
      >
        {/* TOPO */}
        <div>
          <div className={clsx("flex flex-col items-center")}>
            <div className="flex items-center justify-center py-4 mb-[25px]">
              {open ? (
                <Image
                  src="/logo-preta.svg"
                  alt="Logo Jotanunes"
                  width={130}
                  height={30}
                />
              ) : (
                <Image
                  src="/logo-jotanunes.svg"
                  alt="Logo Icon"
                  width={30}
                  height={30}
                />
              )}
            </div>

            {/* Avatar + Saudações */}
            <div
              className={clsx(
                "px-3 flex items-center mb-[28px]",
                open ? "justify-start gap-2" : "justify-center"
              )}
            >
              <Image
                src="/icon-23.svg"
                alt="Avatar do usuário"
                width={32}
                height={32}
                className="rounded-full"
              />
              {open && (
                <span className="text-xs text-gray-700">
                  Bem Vindo, {nomeUsuario || "Usuário"}
                </span>
              )}
            </div>
          </div>

          {/* Navegação */}
          <nav className={clsx("flex flex-col gap-2 px-2", open ? "items-start" : "items-center")}>
            <SidebarIcon
              icon={<Home size={16} />}
              label="Home"
              open={open}
              active={activePage === "Home"}
              onClick={() => router.push('/Home')}
            />
            <SidebarIcon
              icon={<Search size={16} />}
              label="Explorar"
              open={open}
              active={activePage === "Explorar"}
              onClick={() => router.push('/explorar-cursos')}
            />
            <SidebarIcon
              icon={<BookOpen size={16} />}
              label="Meus cursos"
              open={open}
              active={activePage === "Meus cursos"}
              onClick={() => router.push('/meus-cursos')}
            />
            <SidebarIcon
              icon={<FileText size={16} />}
              label="Certificados"
              open={open}
              active={activePage === "Certificados"}
              onClick={() => router.push('/certificados')}
            />
            <SidebarIcon
              icon={<ShoppingCart size={16} />}
              label="Nunes Shop"
              open={open}
              active={activePage === "Nunes Shop"}
              onClick={() => router.push('/loading')}
            />
            <SidebarIcon
              icon={<MessageCircle size={16} />}
              label="Chat"
              open={open}
              active={activePage === "Chat"}
              onClick={() => router.push('/chatbot')}
            />
            <SidebarIcon
              icon={<Settings size={16} />}
              label="Configurações"
              open={open}
              active={activePage === "Configurações"}
              onClick={() => router.push('/curso')}
            />
          </nav>
        </div>

        {/* LOGOUT */}
        <div className="px-2 pb-3">
          <SidebarIcon
            icon={<LogOut size={16} />}
            label="Log out"
            open={open}
            onClick={() => router.push('/')}
          />
        </div>
      </aside>

      {/* Push da tela */}
      <div className={clsx("transition-all duration-300", open ? "ml-[180px]" : "ml-[60px]")}></div>
    </>
  )
}

function SidebarIcon({
  icon,
  label,
  open,
  active = false,
  onClick,
}: {
  icon: React.ReactNode
  label: string
  open: boolean
  active?: boolean
  onClick?: () => void
}) {
  return (
    <button
      onClick={onClick}
      className={clsx(
        "flex py-1.5 px-2 rounded-md text-sm transition-all duration-200 w-full cursor-pointer", // <-- Aqui está o cursor pointer
        open ? "items-center gap-3" : "justify-center",
        active ? "bg-red-500 text-white font-semibold" : "bg-white hover:bg-gray-100 text-gray-700"
      )}
    >
      <span className={clsx(!open && "mx-auto")}>{icon}</span>
      {open && <span className="whitespace-nowrap">{label}</span>}
    </button>
  )
}
