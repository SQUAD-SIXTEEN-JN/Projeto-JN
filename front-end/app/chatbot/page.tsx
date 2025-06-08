import { Sidebar } from "../_components/Sidebar"
import ChatbotIframe from "../_components/Chatbotframe"
import Image from "next/image"

export default function ChatbotPage() {
  return (
    <div className="flex min-h-screen">
      {/* Sidebar fixa */}
      <Sidebar />

      {/* Área principal com o chatbot */}
      <main className="flex-1 p-4 bg-[#FCF8ED]">
        <div className="flex justify-end mb-[30px]">
            <Image
            src="logo-preta.svg"
            alt="Jotanunes Construtora"
            width={200}
            height={54}
            className="h-auto"
            />
        </div>
        <h1 className="mb-10 text-[40px] font-bold">Converse, tire dúvidas e etc..</h1>
        <ChatbotIframe />
      </main>
    </div>
  )
}