'use client'
import Link from 'next/link';
import { Sidebar } from "../_components/Sidebar"
import Image from 'next/image'
import { useState } from 'react'

export default function CursoPage() {
  const [tabAtiva, setTabAtiva] = useState<'info' | 'conteudo' | 'estudantes'>('info')
  const [progresso, setProgresso] = useState(58) // Dinamicamente controlado

  return (
    <div className="flex bg-[#fefaf2] min-h-screen">
      <Sidebar activePage="Meus cursos" />

      <main className="flex-1 p-6 ml-[60px] md:ml-[180px] transition-all duration-300">
        <div className="text-sm text-gray-500 mb-4">
          <Link href="/meus-cursos" className="hover:underline text-gray-500">
            Meus cursos
          </Link>
          {' '} / <span className="text-gray-900 font-semibold">Curso de Design</span>
        </div>

        <div className="bg-white rounded-2xl shadow p-6 mb-6">
          <div className="relative w-full h-64 rounded-xl overflow-hidden mb-4">
            <Image src="/cursos.svg" alt="Curso" fill className="object-cover" />
            <div className="absolute bottom-2 left-2 bg-black bg-opacity-50 text-white text-xs px-2 py-1 rounded">
              ▶ 35
            </div>
          </div>

          <h1 className="text-2xl font-bold">Curso de design</h1>
          <p className="text-gray-600 mb-4">Por Professor, ilustrador e design de interiores</p>

          <div className="flex gap-4 mb-4">
            {['info', 'conteudo', 'estudantes'].map((tab) => (
              <button
                key={tab}
                className={`px-4 py-2 rounded-t-md text-sm font-medium ${
                  tabAtiva === tab ? 'bg-red-700 text-white' : 'bg-gray-100'
                }`}
                onClick={() => setTabAtiva(tab as typeof tabAtiva)}
              >
                {tab.charAt(0).toUpperCase() + tab.slice(1)}
              </button>
            ))}
          </div>

          {tabAtiva === 'info' && (
            <div className="text-gray-700 leading-relaxed">
              <p className="mb-2">
                Curso de Design: Fundamentos e Práticas Criativas
              </p>
              <p>
                Descubra o universo do design e aprenda a transformar ideias em projetos visuais incríveis!...
              </p>
            </div>
          )}
        </div>

        {/* Progresso do curso */}
        <aside className="bg-white rounded-2xl shadow p-6 mb-6">
          <div className="flex items-center justify-between mb-4">
            <span className="font-medium text-gray-800">Acompanhe seu progresso:</span>
            <span className="text-red-600 font-semibold">{progresso}%</span>
          </div>
          <div className="w-full bg-gray-200 h-3 rounded-full mb-4">
            <div
              className="bg-red-600 h-3 rounded-full transition-all duration-300"
              style={{ width: `${progresso}%` }}
            ></div>
          </div>
          <button
            className="bg-red-600 text-white w-full py-2 rounded-md font-semibold mb-4"
            onClick={() => setProgresso((prev) => Math.min(prev + 10, 100))}
          >
            Continue assistindo.
          </button>

          <div className="text-sm mb-4">
            <p className="font-semibold mb-2">O que você vai aprender:</p>
            <ul className="list-disc ml-5 space-y-1 text-gray-700">
              <li>Aplicação do design na construção civil</li>
              <li>Criação de plantas, fachadas e ambientes</li>
              <li>Uso de AutoCAD, SketchUp e Revit</li>
            </ul>
          </div>

          <div className="text-sm space-y-2 mb-4 text-gray-700">
            <p><strong>80%</strong> de avaliações positivas</p>
            <p><strong>35</strong> estudantes</p>
            <p><strong>9</strong> vídeo aulas (9h 11m)</p>
            <p><strong>10</strong> Atividades</p>
            <p><strong>Certificação</strong></p>
            <p><strong>Acompanhamento do professor</strong></p>
            <p><strong>Legendas</strong></p>
            <p><strong>Recompensa de:</strong> <span className="text-orange-500 font-bold">20 Points</span></p>
          </div>

          <div className="text-sm text-gray-700">
            <p className="font-semibold mb-2">Tags:</p>
            <div className="flex flex-wrap gap-2">
              <span className="bg-gray-100 px-2 py-1 rounded-full">Sketch</span>
              <span className="bg-gray-100 px-2 py-1 rounded-full">Product Design</span>
              <span className="bg-gray-100 px-2 py-1 rounded-full">Tuts X</span>
              <span className="bg-gray-100 px-2 py-1 rounded-full">UI/UX</span>
            </div>
          </div>
        </aside>

        {/* Comentários */}
        <section className="bg-white rounded-2xl shadow p-6">
          <h2 className="text-lg font-semibold mb-4">Comentários.</h2>
          <div className="space-y-4 mb-4">
            <div>
              <p className="font-semibold">Pablo Nunes</p>
              <p className="text-sm text-gray-500">Uma hora atrás.</p>
              <p>Muito show!</p>
            </div>
            <div>
              <p className="font-semibold">Natalhy Gomes</p>
              <p className="text-sm text-gray-500">Três horas atrás.</p>
              <p>Curso muito completo e cheio de conhecimento!</p>
            </div>
          </div>

          <h3 className="font-medium mb-2">Dê sua opinião.</h3>
          <textarea
            placeholder="Escreva seu comentário aqui."
            className="w-full border border-gray-300 rounded-xl p-4 mb-2"
            rows={4}
          />
          <button className="bg-red-700 text-white px-4 py-2 rounded-md">
            Deixe seu comentário
          </button>
        </section>
      </main>
    </div>
  )
}
