import { FunctionalComponent } from 'preact';

const Navbar: FunctionalComponent = () => {
  return (
    <nav class="bg-white border-gray-200 px-2 sm:px-4 py-2.5 rounded dark:bg-gray-800">
      <div class="container flex flex-wrap justify-between items-center mx-auto">
        <a href="https://flowbite.com" class="flex items-center">
          <img
            src="/src/assets/evergreen.png"
            class="mr-3 h-6 sm:h-9"
            alt="Logo Evergreen"
          />
        </a>
        <div id="mobile-menu">
          <ul class="flex flex-col mt-4 md:flex-row md:space-x-8 md:mt-0 md:text-sm md:font-medium">
            <li>
              <span class="block py-2 pr-4 pl-3 rounded md:bg-transparent text-blue-700 p-0 dark:text-white">
                Administrador
              </span>
            </li>
            <li>
              <button
                type="button"
                class="focus:outline-none text-white bg-green-700 hover:bg-green-800 focus:ring-4 focus:ring-green-300 font-medium rounded-lg text-sm px-5 py-2.5 mr-2 mb-2 dark:bg-green-600 dark:hover:bg-green-700 dark:focus:ring-green-800"
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
