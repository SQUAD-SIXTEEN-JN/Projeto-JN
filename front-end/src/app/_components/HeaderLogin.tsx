import Image from "next/image"
import logo  from "../../../public/LogoPreta.svg"
export function HeaderLogin(){
    return (
        <header className="bg-[#FFFFFF] drop-shadow-lg flex justify-star mb-[100px]">
            <Image
            src={logo}
            alt="Logo JotaNunes"
            width={166}
            height={45}
            className="py-[13px] pl-[24px]"
            />

        </header>
    )

    
}