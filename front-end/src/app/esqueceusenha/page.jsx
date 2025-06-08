"use client";
import { useState } from "react";
import Image from "next/image";
import { HeaderLogin } from "../_components/HeaderLogin";
import { Mail, LogIn, CheckCircle } from 'lucide-react';
import photocard1 from "../../../public/photocard1.svg";
import { auth } from "../../../firebase";
import { sendPasswordResetEmail } from "firebase/auth";
import check from "../../../public/check.svg";

export default function EsqueceuSenha() {
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState({ type: "", text: "" });
  const [resetSent, setResetSent] = useState(false);

  const handleResetPassword = async (e) => {
    e.preventDefault();

    if (!email) {
      setMessage({ type: "error", text: "Por favor, insira seu e-mail." });
      return;
    }

    setLoading(true);
    setMessage({ type: "", text: "" });

    try {
      await sendPasswordResetEmail(auth, email);
      setResetSent(true);
    } catch (error) {
      console.error("Erro ao enviar e-mail de recuperação:", error);

      let errorMessage = "Ocorreu um erro ao enviar o e-mail de recuperação.";

      if (error.code === 'auth/invalid-email') {
        errorMessage = "E-mail inválido. Verifique e tente novamente.";
      } else if (error.code === 'auth/user-not-found') {
        errorMessage = "Não encontramos uma conta com este e-mail.";
      } else if (error.code === 'auth/too-many-requests') {
        errorMessage = "Muitas tentativas. Tente novamente mais tarde.";
      }

      setMessage({ type: "error", text: errorMessage });
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <HeaderLogin />
      <main className="grid grid-cols-1 md:grid-cols-2 justify-items-center p-4">
        <div className="justify-items-center text-[39px] md:text-4xl p-4">
          <Image
            src={photocard1 || "/placeholder.svg"}
            alt="Foto do mascote em Card"
            layout="responsive"
            width={470}
            height={318}
            priority
            className="mb-8 md:mb-12 w-full md:w-auto max-w-full"
          />
          <h1 className="text-center text-2xl md:text-3xl font-[--font-roboto] font-black text-[#010101]">
            Te ajudando de forma <br /> simples e rápida!
          </h1>
        </div>

        <div className="mt-8 md:mt-[50px] text-xl md:text-2xl text-center p-6 md:mr-10">
          {!resetSent ? (
            <>
              <h1 className="mb-6 md:mb-[12px] font-[--font-montserrat] leading-[44px]">
                Recuperação de Senha
              </h1>
              <p className="font-[--font-montserrat] text-[16px] leading-[44px] mb-[40px]">
                Insira abaixo o e-mail da conta que deseja recuperar a senha.
              </p>

              {message.text && (
                <div
                  className={`mb-4 p-3 rounded-md text-sm ${message.type === "success" ? "bg-green-100 text-green-800" : "bg-red-100 text-red-800"}`}
                >
                  {message.text}
                </div>
              )}

              <form onSubmit={handleResetPassword}>
                <div className="relative font-[--font-roboto]">
                  <input
                    type="email"
                    id="email"
                    required
                    placeholder="E-mail"
                    className="pl-10 pr-20 py-3 md:py-[24px] border w-full border-[#757575] mb-[18px]"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                  />
                  <Mail className="w-5 h-5 text-gray-500 absolute left-3 top-[40px] transform -translate-y-1/2" />
                </div>
                <div className="mb-[30px]">
                  <button
                    type="submit"
                    disabled={loading}
                    className="w-full md:w-[450px] max-w-full bg-[#D1484C] text-white cursor-pointer py-[22px] px-[35px] flex justify-between items-center font-[--font-roboto] font-medium"
                  >
                    <span>{loading ? "Enviando..." : "Continuar"}</span>
                    {loading ? <span className="animate-spin">⟳</span> : <LogIn size={24} />}
                  </button>
                </div>
              </form>
            </>
          ) : (
            <div className="text-center mt-20">
              <div className="flex justify-center mb-6">
                <Image
                  src={check || "/placeholder.svg"}
                  alt="Foto checkin"
                />
              </div>
              <h2 className="text-[40px] font-[--font-montserrat] mb-4">
                Solicitação de Redefinição <br/> de Senha enviada!
              </h2>
              <p className="text-[20px] font-[--font-montserrat] text-gray-700 mb-8">
                Verifique o link de redefinição enviado para seu e-mail para prosseguir.
              </p>
              <p className="text-[16px] text-gray-500">
                Não recebeu o email? Verifique sua pasta de spam ou{" "}
                <button onClick={() => setResetSent(false)} className="text-[#D1484C] underline cursor-pointer">
                  tente novamente
                </button>.
              </p>
            </div>
          )}
        </div>
      </main>
    </>
  );
}