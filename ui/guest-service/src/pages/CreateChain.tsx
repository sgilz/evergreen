import ky from 'ky';
import { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';

const CreateChain: React.FC = () => {
  const [show, setShow] = useState(false);
  const [name, setName] = useState('');

  const navigate = useNavigate();

  async function createChain(e: Event) {
    e.preventDefault();
    try {
      await ky.post(
        `${import.meta.env['VITE_API_URL'] as string}/farmchains/create`,
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token') as string}`,
          },
          json: {
            name,
          },
        }
      );
      navigate('/');
    } catch (error) {
      navigate('/');
    }
  }

  useEffect(() => {
    if (!localStorage.getItem('token')) {
      window.location.href = `${
        import.meta.env['VITE_LOGIN_APP'] as string
      }?origin=signout`;
    } else {
      setShow(true);
    }
  }, []);

  return (
    <>
      {show ? (
        <div className="flex-grow self-center pt-24">
          <div className="p-6 max-w-sm bg-white rounded-lg border border-gray-200 shadow-md dark:bg-gray-800 dark:border-gray-700">
            <form
              onSubmit={(e: any) => {
                createChain(e);
              }}
            >
              <div className="mb-6 w-full">
                <label
                  htmlFor="name"
                  className="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-400"
                >
                  Nombre
                </label>
                <input
                  type="text"
                  id="name"
                  className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                  required
                  value={name}
                  onChange={(e: any) => {
                    setName(e.target.value);
                  }}
                />
              </div>
              <Link
                to="/"
                className="text-red-700 hover:text-white border border-red-700 hover:bg-red-800 focus:ring-4 focus:outline-none focus:ring-red-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center mr-2 mb-2 dark:border-red-500 dark:text-red-500 dark:hover:text-white dark:hover:bg-red-600 dark:focus:ring-red-900"
              >
                Cancelar
              </Link>
              <button
                type="submit"
                className="focus:outline-none text-white bg-green-700 hover:bg-green-800 focus:ring-4 focus:ring-green-300 font-medium rounded-lg text-sm px-5 py-2.5 mr-2 mb-2 dark:bg-green-600 dark:hover:bg-green-700 dark:focus:ring-green-800"
              >
                Crear agrocadena
              </button>
            </form>
          </div>
        </div>
      ) : (
        <></>
      )}
    </>
  );
};

export default CreateChain;
