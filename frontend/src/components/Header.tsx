import { Button } from "@mantine/core";
import logo from "../assets/logo.svg";

const Header: React.FC = () => {
  return (
    <header className="mx-4 md:mx-auto my-4 px-8 py-4 w-full max-w-6xl shadow-lg rounded-lg text-2xl font-bold flex bg-[#fefefe]">
      <a href="/" className="mr-auto">
        <div className="cursor-pointer flex gap-2 items-center w-fit text-red-900">
          <img src={logo} alt="Logo" className="h-8" />
          <div className="mr-auto w-fit">ATG Visualizer</div>
        </div>
      </a>

      <Button
        variant="subtle"
        component="a"
        href="/about"
        disabled
        data-disabled
        onClick={(event) => event.preventDefault()}
      >
        About
      </Button>
    </header>
  );
};

export default Header;
