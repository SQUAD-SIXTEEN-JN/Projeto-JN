import Image from "next/image";

export function HeaderLogin() {
  return (
    <header className="bg-[#FFFFFF] drop-shadow-lg flex justify-end mb-[100px]">
      <Image
        src="/LogoPreta.svg" // Caminho direto a partir da pasta `public`
        alt="Logo JotaNunes"
        width={166}
        height={45}
        className="py-[13px] pr-[37px]"
      />
    </header>
  );
}
