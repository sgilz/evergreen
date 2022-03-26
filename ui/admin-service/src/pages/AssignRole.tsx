import ky from 'ky';
import { FunctionalComponent } from 'preact';
import { useEffect, useState } from 'preact/hooks';
import { Link, useNavigate } from 'react-router-dom';

const AssignRole: FunctionalComponent = () => {
  const [show, setShow] = useState(false);
  const [roles, setRoles] = useState<any[]>([]);
  const [currentRole, setCurrentRole] = useState('');
  const navigate = useNavigate();
  const queryString = window.location.search;
  const query = new URLSearchParams(queryString);

  async function fetchRoles() {
    try {
      const res: { roles: any[] } = await ky
        .get(`${import.meta.env['VITE_API_URL'] as string}/roles`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token') as string}`,
          },
        })
        .json();
      setRoles(res.roles);
    } catch (error) {}
  }

  useEffect(() => {
    if (!localStorage.getItem('token')) {
      window.location.href = `${
        import.meta.env['VITE_LOGIN_APP'] as string
      }?origin=signout`;
    } else {
      setShow(true);
      fetchRoles();
    }
  }, []);

  async function assignRole(e: Event) {
    e.preventDefault();
    try {
      await ky.patch(
        `${import.meta.env['VITE_API_URL'] as string}/users/assign`,
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token') as string}`,
          },
          json: {
            username: query.get('username'),
            role_name: currentRole,
          },
        }
      );
      navigate('/');
    } catch (error) {
      navigate('/');
    }
  }

  return (
    <>
      {show ? (
        <div className="flex-grow self-center pt-24">
          <form onSubmit={assignRole}>
            <div className="mb-6 w-full">
              <label
                for="roles"
                className="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-400"
              >
                Selecciona un rol
              </label>
              <select
                id="roles"
                className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                onChange={(e: any) => {
                  setCurrentRole(e.target.value);
                }}
                value={currentRole}
                required
              >
                {roles.map((role) => (
                  <option value={role.name}>{role.name}</option>
                ))}
              </select>
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
              Asignar role
            </button>
          </form>
        </div>
      ) : (
        <></>
      )}
    </>
  );
};

export default AssignRole;
