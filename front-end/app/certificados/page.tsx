
'use client';
import { useState, useEffect } from 'react';
import Image from 'next/image';
import { Sidebar } from '../_components/Sidebar'; // ajuste o caminho se necessário

interface Certificate {
  id: string;
  courseName: string;
  imageUrl: string;
  tag?: string;
}

export default function CertificadosPage() {
  const [certificates, setCertificates] = useState<Certificate[]>([]);
  const [selectedImage, setSelectedImage] = useState<string | null>(null);

  const mockCertificates: Certificate[] = [
    { id: '1', courseName: 'Técnicas de Fundação e Estruturas', imageUrl: '/certificado.png', tag: 'Estruturas' },
    { id: '2', courseName: 'Leitura e Interpretação de Projetos', imageUrl: '/certificado.png', tag: 'Projetos' },
    { id: '3', courseName: 'Segurança do Trabalho na Construção', imageUrl: '/certificado.png', tag: 'Segurança' },
    { id: '4', courseName: 'Materiais de Construção Civil', imageUrl: '/certificado.png', tag: 'Materiais' },
    { id: '5', courseName: 'Instalações Hidráulicas e Elétricas', imageUrl: '/certificado.png', tag: 'Instalações' },
    { id: '6', courseName: 'Orçamento e Planejamento de Obras', imageUrl: '/certificado.png', tag: 'Orçamento' },
  ];

  useEffect(() => {
    const fetchCertificates = async () => {
      try {
        const response = await fetch('/api/certificados');
        if (!response.ok) throw new Error('Falha ao buscar certificados');
        const data: Certificate[] = await response.json();
        setCertificates(data);
      } catch (error) {
        console.warn('Usando dados mock por falta de backend.');
        setCertificates(mockCertificates);
      }
    };

    fetchCertificates();
  }, []);

  return (
    <div className="flex min-h-screen bg-[#FCF8ED]">
      {/* Sidebar fixa à esquerda */}
      <Sidebar />
      
      {/* Conteúdo principal com margem esquerda */}
      <main className="flex-1 p-8 bg-[#FCF8ED]">
        
        <div className="flex justify-end mb-[30px]">
          <Image
            src="logo-preta.svg"
            alt="Jotanunes Construtora"
            width={200}
            height={54}
            className="h-auto"
          />
        </div>
        
        <h1 className="text-[48px] font-bold mb-6">Certificados</h1>
        
        <input
          type="text"
          placeholder="🔍 Pesquisar certificado"
          className="mb-6 px-4 py-2 border rounded w-full max-w-sm bg-white"
        />
        
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
          {certificates.map((cert) => (
            <div
              key={cert.id}
              className="bg-white rounded-lg shadow cursor-pointer hover:shadow-lg transition"
              onClick={() => setSelectedImage(cert.imageUrl)}
            >
              <div className="relative w-full h-48">
                <Image
                  src={cert.imageUrl}
                  alt={cert.courseName}
                  fill
                  style={{ objectFit: 'cover' }}
                  className="rounded-t-lg"
                />
              </div>
              <div className="p-4 bg-white rounded-b-lg">
                <p className="text-sm font-medium text-gray-700">📜 {cert.courseName}</p>
              </div>
            </div>
          ))}
        </div>
        
        {selectedImage && (
          <div
            className="fixed inset-0 bg-black bg-opacity-70 flex justify-center items-center z-50"
            onClick={() => setSelectedImage(null)}
          >
            <div className="bg-white p-4 rounded-lg max-w-4xl">
              <Image
                src={selectedImage}
                alt="Certificado Ampliado"
                width={1000}
                height={700}
                className="rounded"
              />
            </div>
          </div>
        )}
      </main>
    </div>
  );
}