import { Link } from 'react-router-dom';

const Navbar: React.FC = () => {
  const signOut = () => {
    if (localStorage.getItem('token')) {
      localStorage.removeItem('token');
    }
    window.location.href = `${
      import.meta.env['VITE_LOGIN_APP'] as string
    }?origin=signout`;
  };

  return (
    <nav className="bg-white border-gray-200 px-2 sm:px-4 py-2.5 rounded dark:bg-gray-800">
      <div className="container flex flex-wrap justify-between items-center mx-auto">
        <Link to="/" className="flex items-center">
          <img
            src="/src/assets/evergreen.png"
            className="mr-3 h-6 sm:h-9"
            alt="Logo Evergreen"
          />
        </Link>
        <div id="mobile-menu">
          <ul className="flex flex-col mt-4 md:flex-row md:space-x-8 md:mt-0 md:text-sm md:font-medium">
            <li>
              <Link
                to="/create-chain"
                className="block py-2 pr-4 pl-3 rounded md:bg-transparent text-blue-700 p-0 dark:text-white"
              >
                Crear agrocadena
              </Link>
            </li>
            <li>
              <Link
                to="/create-stage"
                className="block py-2 pr-4 pl-3 rounded md:bg-transparent text-blue-700 p-0 dark:text-white"
              >
                Crear etapa
              </Link>
            </li>
            <li>
              <button
                type="button"
                className="focus:outline-none text-white bg-green-700 hover:bg-green-800 focus:ring-4 focus:ring-green-300 font-medium rounded-lg text-sm px-5 py-2.5 mr-2 mb-2 dark:bg-green-600 dark:hover:bg-green-700 dark:focus:ring-green-800"
                onClick={signOut}
              >
                Cerrar sesión
              </button>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
