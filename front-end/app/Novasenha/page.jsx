"use client";
import { useState, useEffect } from "react";
import { HeaderLogin }from "../_components/HeaderLogin";
import { Lock, CheckCircle, ArrowRight } from 'lucide-react';
import { useRouter } from "next/navigation";
import { updatePassword } from "@/services/auth"; // Você pode criar essa função no authService.js
import Image from "next/image";

export default function NovaSenha() {
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handlePasswordUpdate = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    // Verifica se as senhas são iguais
    if (newPassword !== confirmPassword) {
      setError("As senhas não coincidem. Tente novamente.");
      setLoading(false);
      return;
    }

    try {
      const response = await updatePassword(newPassword);

      if (response.success) {
        router.push("/Home"); // Redireciona para o dashboard após a alteração da senha
      } else {
        setError("Ocorreu um erro ao atualizar a senha. Tente novamente.");
      }
    } catch (error) {
      console.error("Erro ao atualizar a senha:", error);
      setError("Ocorreu um erro inesperado. Tente novamente mais tarde.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <HeaderLogin />
      <main className="grid grid-cols-1 md:grid-cols-2 justify-items-center p-4">
        <div className="justify-items-center text-[39px] md:text-4xl p-4">
          <Image
            src="/photocard2.svg"
            alt="Foto do mascote em Card"
            width={470}
            height={318}
            priority
            className="mb-8 md:mb-12 w-full md:w-auto max-w-full"
          />
          <h1 className="text-center text-2xl md:text-3xl font-black text-[#010101]">
          Seja Bem-Vindo à <br />
          sua nova jornada!
          </h1>
        </div>

        <div className="mt-8 md:mt-[50px] text-xl md:text-2xl text-center p-6 md:mr-10">
          <h1 className="mb-6 md:mb-[25px] leading-[44px]">
            Seja bem- vindo!
          </h1>
          <p className="mb-3 text-[16px] md:mb-[16px] leading-[44px]">Redefina sua senha para uma de sua preferência.</p>

          <form onSubmit={handlePasswordUpdate}>
            <div className="relative">
              <input
                type="password"
                id="newPassword"
                required
                placeholder="Nova Senha"
                className="pl-10 pr-20 py-3 md:py-[24px] border w-full border-[#757575] mb-[18px]"
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
              />
              <Lock className="w-5 h-5 text-gray-500 absolute left-3 top-[40px] transform -translate-y-1/2" />
            </div>
            <div className="relative">
              <input
                type="password"
                id="confirmPassword"
                required
                placeholder="Confirmar Senha"
                className="pl-10 pr-20 py-3 md:py-[24px] border w-full border-[#757575] mb-[18px]"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
              />
              <Lock className="w-5 h-5 text-gray-500 absolute left-3 top-[40px] transform -translate-y-1/2" />
            </div>
            {error && <p className="text-red-500 text-sm mb-4">{error}</p>}
            <div className="mb-[25px]">
              <button
                type="submit"
                disabled={loading}
                className="w-full md:w-[450px] max-w-full bg-[#D1484C] text-white cursor-pointer py-[22px] px-[35px] flex justify-between items-center font-medium"
              >
               <span>{loading ? "Alterando..." : "Continuar"}</span>
               {loading ? (
                    <span className="animate-spin">⟳</span>
                    ) : (
              <ArrowRight size={20} />
              )}
              </button>
            </div>
          </form>
        </div>
      </main>
    </div>
  );
}
