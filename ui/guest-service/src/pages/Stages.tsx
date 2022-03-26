import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import StagesTable from '../components/StagesTable';

const Stages: React.FC = () => {
  const [show, setShow] = useState(false);
  const queryString = window.location.search;
  const query = new URLSearchParams(queryString);
  const navigate = useNavigate();

  useEffect(() => {
    if (!localStorage.getItem('token')) {
      window.location.href = `${
        import.meta.env['VITE_LOGIN_APP'] as string
      }?origin=signout`;
    } else {
      if (query.get('chain')) {
        setShow(true);
      } else {
        navigate('/');
      }
    }
  }, []);

  return (
    <>
      {show ? (
        <div className="flex-grow self-center pt-24">
          <p className="text-3xl dark:text-white pb-4 mb-6 border-b-2 border-green-400 rounded-b">
            Gestión de etapas
          </p>
          <StagesTable chain={query.get('chain') as string} />
        </div>
      ) : (
        <></>
      )}
    </>
  );
};

export default Stages;
